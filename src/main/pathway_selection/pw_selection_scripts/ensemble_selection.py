import pandas as pd
import numpy as np
import glob
import os

name_measure = "complementarity_3"

source_directory = '../../created/pathway_selection/' + name_measure + "/"
all_dir = glob.glob(source_directory+ "*.csv" )

# saving_directory_ranked_pathways = '../../created/pathway_selection/ranked_highStd/'
saving_directory = '../../created/pathway_selection/' + name_measure + "/"

# all_dir.remove(source_directory_ranked_pathways+'ranked_ensemble.csv') #just in case

def call_ensemble():

    # For every selection method
    first = True
    for file_path in sorted(all_dir):
        name_selection = file_path[len(source_directory):-4]
        if name_selection == "ensemble": continue

        # Read files
        try:
            df_temp = pd.read_csv(file_path, index_col=0)
        except:
            continue

        # Merge
        if first:
            df_ensemble = df_temp
            first = False
        else:
            df_ensemble = df_ensemble.join(df_temp, how='outer')

    # Add ensemble information (i.e. sum + rank)
    df_ensemble["Ensemble_sum"] = df_ensemble.SVM_rank + df_ensemble.Boruta_rank + df_ensemble.WMW_rank
    df_ensemble = df_ensemble.sort_values(by='Ensemble_sum')

    # Make pretty
    df_ensemble['pathways'] = df_ensemble.index # keep pathways
    cols = list(df_ensemble)
    cols.insert(0, cols.pop(cols.index('pathways')))
    df_ensemble = df_ensemble.loc[:, cols]
    df_ensemble = df_ensemble.reset_index(drop=True)
    df_ensemble['Ensemble_rank'] = np.arange(1, len(df_temp) + 1)

    # Save
    if not os.path.exists(saving_directory):
        os.makedirs(saving_directory)
    df_ensemble.to_csv(saving_directory+'ensemble.csv', header=True, index=False)
