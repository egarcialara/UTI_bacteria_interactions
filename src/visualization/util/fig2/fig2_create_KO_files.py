import pandas as pd
import glob
import os
import requests
from KO_matrices import get_list_ko, create_binary_matrix

KO_lists_directory = "../../../../data/KO_lists/"
all_dir = glob.glob(KO_lists_directory + "*.txt")
len_dir_name = len(KO_lists_directory)

saving_dir_modules = "temp/KO_binary_matrices_modules/"
saving_dir_all = "temp/KO_binary_matrices_all/"

def create_KOs_binary_matrix_module():
    '''
    create KOs binary matrix for module
    '''

    # Remove old files
    for x in glob.glob(saving_dir_modules + "*.csv"): os.remove(x)

    # Request the pathway KO list from KEGG
    kegg_pathway_request = requests.get('http://rest.kegg.jp/list/module')
    kegg_pathway_list = kegg_pathway_request.text

    # Open all the files in the directory
    rep=0
    for line in kegg_pathway_list.split('\n')[:-1]:
        rep+=1
        print(f"Module n. {rep}:")

        # Get list of KOs
        # module_name = "Glutathone biosynthesis, gutamate => glutathione"
        # module_ID = "md:M00118"
        module_name = line.split('\t')[1]
        module_ID = line.split('\t')[0]
        ko_in_path = get_list_ko(module_ID, source="module")
        df_kos_binary_temp = pd.DataFrame(ko_in_path,columns=['ko'])

        # Get matrices
        for strain in all_dir:
            name_strain = strain[len_dir_name:-4]
            df_kos_binary_temp = create_binary_matrix(
                strain, name_strain, df_kos_binary_temp, module_name) #add strains as columns, one col still KOs

        # Save matrix
        df_kos_binary = df_kos_binary_temp.set_index("ko").transpose()
        module_name_save = module_name.replace("/", "-")

        if not os.path.exists(saving_dir_modules): os.makedirs(saving_dir_modules)
        df_kos_binary.to_csv(saving_dir_modules+module_name_save+".csv", header=True, index=True)

def create_KOs_binary_matrix_all():

    # Get list of -all- KOs
    set_kos = set()
    for strain in all_dir:
        df_strain_kos = pd.read_csv(strain, names=['pid', 'ko'], sep='\t', header=None)
        set_kos = set_kos.union(set(df_strain_kos['ko']))
    set_kos = {x for x in set_kos if pd.notna(x)}
    df_kos_binary_temp = pd.DataFrame(set_kos,columns=['ko'])

    # Get matrices
    for strain in all_dir:
        name_strain = strain[len_dir_name:-4]
        df_kos_binary_temp = create_binary_matrix(
            strain, name_strain, df_kos_binary_temp, "all") #add strains as columns, one col still KOs
    # Save matrix
    df_kos_binary = df_kos_binary_temp.set_index("ko").transpose()

    if not os.path.exists(saving_dir_all): os.makedirs(saving_dir_all)
    df_kos_binary.to_csv(saving_dir_all+"all"+".csv", header=True, index=True)
    
