import pandas as pd
import os
import glob
from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy


bigmatrices_directory =  '../../created/big_matrices/'
all_dir = glob.glob(bigmatrices_directory+ "*.csv" )

saving_directory_selected_pathways = '../../created/pathway_selection/selected_highStd/'
saving_directory_ranked_pathways = '../../created/pathway_selection/ranked_highStd/'
saving_directory_coef_pathways = '../../created/pathway_selection/estimator_highStd/'

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
        name_measure = file_path[len(bigmatrices_directory):-4] 

        # Get X (matrix with data) and y (column with labels).
        df_X = df_Xy.loc[:, df_Xy.columns != 'y']
        df_X = df_X[list_pws] # NEW!!!


        df_y = df_Xy['y']

        # define RF classifier + Boruta FS
        rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
        selector = BorutaPy(rf, n_estimators='auto', verbose=0, random_state=1)

        try:
            selector.fit(df_X.values, df_y.values)
        except:
            print('Error in ' + file_path)
            continue

        # Get Ranked+Selected pathways into DataFrames
        if 'df_ranked_Boruta' in locals():
            df_ranked_temp = pd.DataFrame({
                'pathways': df_X.columns.tolist(),
                name_measure: selector.ranking_})
            df_ranked_Boruta = pd.merge(df_ranked_Boruta, df_ranked_temp, how="outer", on="pathways")

            df_selected_Boruta = pd.concat([
                df_selected_Boruta,
                pd.DataFrame({name_measure: df_X.columns[selector.support_==True]})],
                axis=1)

            df_coef_Boruta = pd.concat([
                df_coef_Boruta,
                pd.DataFrame({name_measure: rf.fit(df_X, df_y).feature_importances_})],
                axis=1)

        else:
            df_ranked_Boruta = pd.DataFrame({
                'pathways': df_X.columns.tolist(),
                name_measure: selector.ranking_})

            df_selected_Boruta = pd.DataFrame({
                name_measure: df_X.columns[selector.support_==True]})

            df_coef_Boruta = pd.DataFrame({
                "pathway": df_X.columns,
                name_measure: rf.fit(df_X, df_y).feature_importances_})

  
    # Save
    df_ranked_Boruta = df_ranked_Boruta.sort_values(by=df_ranked_Boruta.columns[1])

    if not os.path.exists(saving_directory_ranked_pathways):
        os.makedirs(saving_directory_ranked_pathways)
    if not os.path.exists(saving_directory_selected_pathways):
        os.makedirs(saving_directory_selected_pathways)
    if not os.path.exists(saving_directory_coef_pathways):
        os.makedirs(saving_directory_coef_pathways)

    df_ranked_Boruta.to_csv(saving_directory_ranked_pathways+'ranked_Boruta.csv',
                            header=True, index=False)
    df_selected_Boruta.to_csv(saving_directory_selected_pathways+'selected_Boruta.csv',
                            header=True, index=False)
    df_coef_Boruta.to_csv(saving_directory_coef_pathways+'estimator_Boruta.csv',
                       header=True, index=False)


