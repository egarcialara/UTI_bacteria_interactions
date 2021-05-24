import pandas as pd
import numpy as np
import os
import glob
from sklearn.svm import SVR

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

def call_SVM():

    # Perform the process for every interaction index.
    for file_path in sorted(all_dir):
        df_Xy = pd.read_csv(file_path, index_col=0)
        df_Xy = df_Xy.fillna(0)

        # Only Ent
        df_Xy = df_Xy.loc[df_Xy.index.str.split("x").str[1]!="St",]

        # Get X (matrix with data) and y (column with labels).
        df_X = df_Xy.loc[:, df_Xy.columns != 'y']
        df_X = df_X[list_pws]
        df_y = df_Xy['y']

        # Perform SVM
        estimator = SVR(kernel="linear")
        # selector = RFE(estimator, step=1, verbose=0)
        try:
            estimator = estimator.fit(df_X, df_y)
        except:
            print('Error in ' + file_path)
            continue

        # Put results in data frame
        df_temp = pd.DataFrame({
            'pathways': df_X.columns.tolist(),
            'SVM_coef': [x for x in estimator.coef_[0]]})
        df_temp = df_temp.sort_values(by='SVM_coef', ascending=False)
        df_temp = df_temp.reset_index(drop=True)
        df_temp['SVM_rank'] = np.arange(1, len(df_temp) + 1)

  
    # Save
    if not os.path.exists(saving_directory):
        os.makedirs(saving_directory)
    df_temp.to_csv(saving_directory+'SVM.csv', header=True, index=False)
