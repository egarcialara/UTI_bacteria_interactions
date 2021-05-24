import pandas as pd
import numpy as np
import os
import glob
from scipy.stats import mannwhitneyu

name_measure = "complementarity_3"

bigmatrices_directory = '../../created/big_matrices/'
all_dir = glob.glob(bigmatrices_directory+name_measure+".csv")

saving_directory = '../../created/pathway_selection/' + name_measure + "/"

# Pathways with information
file = "../../data/extra/high_std_pw_new.csv"
df_file = pd.read_csv(file, sep=",")
df_file.columns = ["pw", "std"]
list_pws = df_file.pw.tolist()
for i in range(len(list_pws)):
    list_pws[i] = list_pws[i].replace("/", "-")


def call_WMW():

    # Perform the process for every interaction index.
    for file_path in sorted(all_dir):

        df_Xy = pd.read_csv(file_path, index_col=0)
        df_Xy = df_Xy.fillna(0)

        # only Ent
        df_Xy = df_Xy.loc[df_Xy.index.str.split("x").str[1] != "St", ]
        # group for wmw
        donors = df_Xy.index.str.split('x').str[0].str.split('.').str[0]
        acceptors = df_Xy.index.str.split('x').str[1].str.split('.').str[0]
        pair = ["{}x{}".format(a,b) for a,b in zip(donors, acceptors)]
        df_Xy = df_Xy.groupby(pair).mean()

        # Get X (matrix with data) and y (column with labels).
        df_X = df_Xy.loc[:, df_Xy.columns != 'y']
        df_X = df_X[list_pws]

        # Perform the MWU test per column
        try:
            results = df_X.apply(lambda d: mannwhitneyu(d[df_Xy.y == 0],
                                                        d[df_Xy.y == 1],
                                                        alternative='less'),
                                 axis=0)
        except:
            results = pd.DataFrame(index=range(2), columns=range(df_X.shape[1]))
            results.columns = df_X.columns

        # Put results in data frame
        df_temp = pd.DataFrame({
            'pathways': df_X.columns.tolist(),
            'WMW_pvalues': [x for x in results.values[1]],
            'WMW_statistic': [x for x in results.values[0]]})
        df_temp = df_temp.sort_values(by='WMW_pvalues')
        df_temp = df_temp.reset_index(drop=True)
        df_temp['WMW_rank'] = np.arange(1, len(df_temp) + 1)

    # Save
    if not os.path.exists(saving_directory):
            os.makedirs(saving_directory)
    df_temp.to_csv(saving_directory+'WMW.csv', header=True, index=False)
