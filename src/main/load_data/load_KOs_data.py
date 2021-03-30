import pandas as pd
import glob
import requests
import os
from load_data.util.KEGG_pathways import get_list_ko
from load_data.util.create_KO_matrices import create_binary_matrix

KO_lists_directory = "../../data/KO_lists/"
all_dir = glob.glob(KO_lists_directory + "*_KO.txt")
len_dir_name = len(KO_lists_directory)

saving_dir = "../../created/KO_binary_matrices/"

def create_KOs_binary_matrix():
    ''' 
    Go through all pathways
    Create a matrix MxN per pathway (and one overall), containing 1 or 0
        depending of whether a strain (N) has a certain KO (M)

    INPUT:
        - None
    OUTPUT:
        - df_binary: matrix MxN with 0 or 1
    '''

    # Remove old files
    for x in glob.glob(saving_dir + "*.csv"): os.remove(x)

    # Request the pathway KO list from KEGG
    kegg_pathway_request = requests.get('http://rest.kegg.jp/list/pathway')
    kegg_pathway_list = kegg_pathway_request.text


    # Open all the files in the directory
    rep=0
    for line in kegg_pathway_list.split('\n')[:-1]:
        rep+=1
        print(f"Pathway n. {rep}:")

        # Get list of KOs
        ko_in_path, pwname = get_list_ko(line)
        print(pwname)
        df_kos_binary_temp = pd.DataFrame(ko_in_path,columns=['ko'])

        # Get matrices
        for strain in all_dir:
            name_strain = strain[len_dir_name:-4]
            df_kos_binary_temp = create_binary_matrix(
                strain, name_strain, df_kos_binary_temp, pwname) #add strains as columns, one col still KOs

        # Save matrix
        df_kos_binary = df_kos_binary_temp.set_index("ko").transpose()
        pwname_save = pwname.replace("/", "-")

        if not os.path.exists(saving_dir): os.makedirs(saving_dir)
        df_kos_binary.to_csv(saving_dir+pwname_save+".csv", header=True, index=True)
