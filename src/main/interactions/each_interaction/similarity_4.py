import glob
import pandas as pd
import numpy as np
import os

files_dir = "../../created/KO_binary_matrices"
files_binary = glob.glob(files_dir+"/*.csv")
saving_dir_general = "../../created/interaction_matrices"
saving_dir = saving_dir_general + "/similarity_4"

def create_similarity_4():

    '''
    similarity 2
    Pearson correlation (A, D)
    '''

    # read csv
    for f in files_binary:
        KO_binary_matrix = pd.read_csv(f, index_col=0, header=0)

        # Empty target dataframe
        df_interaction = pd.DataFrame(np.nan, index=KO_binary_matrix.index,
                                      columns=KO_binary_matrix.index)

        # Aggregate the binary table into a set of KOs per row (i.e. per strain)
        df_KOs = KO_binary_matrix.copy()
        for col in df_KOs.columns.tolist():
            df_KOs.loc[df_KOs[col]==1, col] = col
        df_KOs = df_KOs.agg([lambda x: set(x)], axis=1)

        # i = donor
        for i, set1 in enumerate(df_KOs["<lambda>"]):
            set1.remove(0)
            list1 = pd.DataFrame({"index":list(set1), "one":list(set1)})
            # j = acceptor
            for j, set2 in enumerate(df_KOs["<lambda>"]):
                list2 = pd.DataFrame({"index":list(set2), "two":list(set2)})
                try:
                    df_kos = pd.merge(list1, list2, how="outer", on="index")
                except:
                    df_kos = pd.concat([list1, list2])

                # calculate actual index
                try:
                    value = df_kos.corr(method='pearson').loc['one', 'two']
                    df_interaction.iloc[i,j] = max(value, 0)  # avoid nan
                except:
                    df_interaction.iloc[i,j] = 0

        # Normalize by pathway length
        df_interaction = df_interaction / KO_binary_matrix.shape[1]

        # Save table
        if not os.path.exists(saving_dir): os.makedirs(saving_dir)
        name_pw = f[(len(files_dir)+1):-4]
        df_interaction.to_csv(saving_dir + "/"+name_pw+".csv", header=True, index=True)