import pandas as pd
import numpy as np
import glob
import os


source_directory_ranked_pathways = '../../created/pathway_selection/ranked/'
all_dir = glob.glob(source_directory_ranked_pathways+ "*.csv" )

saving_directory_ranked_pathways = '../../created/pathway_selection/ranked/'
saving_directory_selected_pathways = '../../created/pathway_selection/selected/'

all_dir.remove(source_directory_ranked_pathways+'ranked_ensemble.csv') #just in case

def call_ensemble():

    # For every selection method
    first=True
    for file_path in sorted(all_dir):
        name_selection = file_path[len(source_directory_ranked_pathways):-4] 

    # Check files are there
        try:
            df_temp = pd.read_csv(file_path, index_col=0)
        except:
            pass

    # read files
        if not first:
            df_temp = pd.concat([df_temp], keys=[name_selection], names=['Firstlevel'])
            df_ranked_emsemble = pd.concat([df_ranked_emsemble, df_temp])

        else:
            df_ranked_emsemble = pd.concat([df_temp], keys=[name_selection], names=['Firstlevel'])
            first=False


    # Merge
    df_ranked_emsemble = df_ranked_emsemble.groupby(level=1).sum()

    # Save
    df_ranked_emsemble = df_ranked_emsemble.sort_values(by=df_ranked_emsemble.columns[0])
    df_selected_emsemble = pd.DataFrame(
        np.sort(df_ranked_emsemble.values, axis=0),
        index=df_ranked_emsemble.index, columns=df_ranked_emsemble.columns)

    if not os.path.exists(saving_directory_ranked_pathways):
        os.makedirs(saving_directory_ranked_pathways)
    if not os.path.exists(saving_directory_selected_pathways):
        os.makedirs(saving_directory_selected_pathways)

    df_ranked_emsemble.to_csv(saving_directory_ranked_pathways+'ranked_ensemble.csv',
                            header=True, index=True)
    df_selected_emsemble.to_csv(saving_directory_selected_pathways+'selected_ensemble.csv',
                            header=True, index=True)
