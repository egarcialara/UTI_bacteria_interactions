import pandas as pd
import os
import glob
import numpy as np


saving_directory = '../../created/big_matrices/'
growth_matrix_directory = '../../created/growth/MaxOD_3.csv'
interaction_matrix_directory = '../../created/interaction_matrices/'

# Choose how to split the labels
growth_threshold = 0.22

def big_matrix_create():
    ''' Creates the big matrix containing
    rows: N*N (strain * strain)
    columns: p pathways
    The value of each cell will be the complementarity/competition/other
        between the strains, in pathway p'''


    # For every interaction table
    for item in ["complementarity_3"]:
                # ['complementarity_1', 'complementarity_2', 'complementarity_3',
                # 'complementarity_4', 'similarity_1', 'similarity_2']:
        all_dir = glob.glob(interaction_matrix_directory+item+"/*.csv")
        big_matrix = pd.DataFrame()

        first=True

        # For every pathway 
        for path in all_dir:

            # Read interactions
            df_InteractionPathway = pd.read_csv(path, index_col=0)
            df_InteractionPathway.index = df_InteractionPathway.columns
            name_dist = len(interaction_matrix_directory)+len(item) + 1
            pwname = path[name_dist:-4]

            # Read growth
            df_growth = pd.read_csv(growth_matrix_directory, index_col=0)
            df_labels = df_growth.copy()

            # Group + attach 0/1 depending on threshold
            df_labels.replace([np.inf, -np.inf], np.nan, inplace=True)
            df_labels = df_labels.groupby(df_labels.index).mean()
            df_labels = df_labels.groupby(df_labels.columns.str[0:2], axis=1).mean()
            df_labels.drop('MM').drop('MM', axis=1)
            df_labels[df_labels > growth_threshold] = 1
            df_labels[df_labels <= growth_threshold] = 0
            df_labels.columns = df_labels.index.tolist()

            # For every row (i = donor)
            for i in df_InteractionPathway.index:
                # For every column (j = acceptor)
                for j in df_InteractionPathway.columns:
                    name_row = str(i)+'x'+str(j)
                    # big_matrix KECS(donor) x Ent(acceptor)
                    big_matrix.loc[name_row, pwname] = (
                                    df_InteractionPathway.loc[i, j])

                    if first:
                        big_matrix.loc[name_row, "y"] = (
                            df_labels.loc[i.split('.')[0], j.split('.')[0]])
            first = False

        if not os.path.exists(saving_directory): os.makedirs(saving_directory)
        big_matrix.to_csv(saving_directory +item+ '.csv')

    return
