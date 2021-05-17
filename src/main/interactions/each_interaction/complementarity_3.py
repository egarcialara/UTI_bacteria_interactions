import glob
import pandas as pd
import numpy as np
import os

files_dir = "../../created/KO_binary_matrices"
files_binary = glob.glob(files_dir+"/*.csv")
saving_dir_general = "../../created/interaction_matrices"
saving_dir = saving_dir_general + "/complementarity_3"

def create_complementarity_3():

    '''
    complementarity 3
     ((D union A) - (D intersection A)) / A
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
            # j = acceptor
            for j, set2 in enumerate(df_KOs["<lambda>"]):
                
                # calculate actual index
                try:
                    df_interaction.iloc[i,j] = len(set1 ^ set2) / len(set2)
                except:
                    df_interaction.iloc[i,j] = len(set1 ^ set2) # avoid division by 0                    

        # Normalize by pathway length
        df_interaction = df_interaction / KO_binary_matrix.shape[1]
 
        # Save table
        if not os.path.exists(saving_dir): os.makedirs(saving_dir)
        name_pw = f[(len(files_dir)+1):-4]
        df_interaction.to_csv(saving_dir + "/"+name_pw+".csv", header=True, index=True)