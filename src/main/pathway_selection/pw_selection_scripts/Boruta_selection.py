import pandas as pd
import numpy as np
import os
import glob
from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy

name_measure = "complementarity_3"

bigmatrices_directory = '../../created/big_matrices/'
all_dir = glob.glob(bigmatrices_directory+name_measure+".csv")

saving_directory = '../../created/pathway_selection/' + name_measure + "/"

# Pathways with information
file = "../../extra/high_std_pw_new.csv"
df_file = pd.read_csv(file, sep=",")
df_file.columns = ["pw", "std"]
list_pws = df_file.pw.tolist()
for i in range(len(list_pws)):
    list_pws[i] = list_pws[i].replace("/", "-")

def call_Boruta():

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

        # define RF classifier + Boruta FS
        rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=3)
        rf = rf.fit(df_X.values, df_y.values)
        feat_imp_X = rf.feature_importances_

        selector = BorutaPy(rf, n_estimators='auto', verbose=0, random_state=1)
        try:
            selector.fit(df_X.values, df_y.values)
        except:
            print('Error in ' + file_path)
            continue
        support_X = selector.support_

        # Put results in data frame
        df_temp = pd.DataFrame({
            'pathways': df_X.columns.tolist(),
            'Boruta_support': [x for x in support_X],
            'Boruta_feat_imp': [x for x in feat_imp_X]})
        df_temp = df_temp.sort_values(by='Boruta_feat_imp', ascending=False)
        df_temp = df_temp.reset_index(drop=True)
        df_temp['Boruta_rank'] = np.arange(1, len(df_temp) + 1)

    # Save
    if not os.path.exists(saving_directory):
        os.makedirs(saving_directory)
    df_temp.to_csv(saving_directory+'Boruta.csv', header=True, index=False)


