import pandas as pd
import numpy as np
import os
import glob
from scipy.stats import mannwhitneyu


bigmatrices_directory =  '../../created/big_matrices/'
all_dir = glob.glob(bigmatrices_directory+ "*.csv" )

saving_directory_selected_pathways = '../../created/pathway_selection/selected/'
saving_directory_ranked_pathways = '../../created/pathway_selection/ranked/'


def call_WMW():


    # Perform the process for every interaction index.
    for file_path in sorted(all_dir):

        df_Xy = pd.read_csv(file_path, index_col=0)
        df_Xy = df_Xy.fillna(0)
        name_measure = file_path[len(bigmatrices_directory):-4]

        # Get X (matrix with data) and y (column with labels).
        df_X = df_Xy.loc[:, df_Xy.columns != 'y']

        # Perform the MWU test per column
        results = df_X.apply(lambda d: mannwhitneyu(d[df_Xy.y == 0], d[df_Xy.y == 1]), axis=0)
        df_temp = pd.DataFrame({
            'pathways': df_X.columns.tolist(),
            'pvalues': [x for x in results.values[1]]})
        df_temp = df_temp.sort_values(by='pvalues')
        df_temp = df_temp.reset_index(drop=True)
        df_temp['rank'] = np.arange(1, len(df_temp) + 1)
 
        # Get Ranked+Selected pathways into DataFrames
        if 'df_ranked_WMW' in locals():
            df_ranked_temp = pd.DataFrame({
                'pathways': df_temp['pathways'].tolist(),
                name_measure: df_temp['rank'].tolist()})
            df_ranked_WMW = pd.merge(df_ranked_WMW, df_ranked_temp, how="outer", on="pathways")


            df_selected_WMW = pd.concat([
                df_selected_WMW,
                pd.DataFrame({name_measure: df_temp.iloc[:min(20, len(df_X.columns)), 0]})],
                axis=1)

        else:
            df_ranked_WMW = pd.DataFrame({
                'pathways': df_temp['pathways'].tolist(),
                name_measure: df_temp['rank'].tolist()})

            df_selected_WMW = pd.DataFrame({
                name_measure: df_temp.iloc[:min(20, len(df_X.columns)), 0]})

    # Save
    df_ranked_WMW = df_ranked_WMW.sort_values(by=df_ranked_WMW.columns[1])
    df_selected_WMW = pd.DataFrame(
        np.sort(df_selected_WMW.values, axis=0),
        index=df_selected_WMW.index, columns=df_selected_WMW.columns)


    if not os.path.exists(saving_directory_ranked_pathways):
        os.makedirs(saving_directory_ranked_pathways)
    if not os.path.exists(saving_directory_selected_pathways):
        os.makedirs(saving_directory_selected_pathways)

    df_ranked_WMW.to_csv(saving_directory_ranked_pathways+'ranked_WMW.csv',
                            header=True, index=False)
    df_selected_WMW.to_csv(saving_directory_selected_pathways+'selected_WMW.csv',
                            header=True, index=False)
