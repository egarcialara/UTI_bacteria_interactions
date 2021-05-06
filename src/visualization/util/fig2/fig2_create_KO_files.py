import pandas as pd
import glob
import os
from KO_matrices import get_list_ko, create_binary_matrix

KO_lists_directory = "../../data/KO_lists/"
all_dir = glob.glob(KO_lists_directory + "*.txt")
len_dir_name = len(KO_lists_directory)

saving_dir = "temp/KO_binary_matrices/"

def create_KOs_binary_matrix_module():
    '''
    create KOs binary matrix for module
    '''

    # Get list of KOs
    module_name = "Glutathone biosynthesis, gutamate => glutathione"
    module_ID = "md:M00118"
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

    if not os.path.exists(saving_dir): os.makedirs(saving_dir)
    df_kos_binary.to_csv(saving_dir+module_name_save+".csv", header=True, index=True)

def create_KOs_binary_matrix_all():

    # Get list of KOs
    set_kos = set()
    for strain in all_dir:
        df_strain_kos = pd.read_csv(strain, names=['pid', 'ko'], sep='\t', header=None)
        set_kos = set_kos.union(set(df_strain_kos['ko']))
        break
    set_kos = {x for x in set_kos if pd.notna(x)}
    df_kos_binary_temp = pd.DataFrame(set_kos,columns=['ko'])

    # Get matrices
    for strain in all_dir:
        name_strain = strain[len_dir_name:-4]
        df_kos_binary_temp = create_binary_matrix(
            strain, name_strain, df_kos_binary_temp, "all") #add strains as columns, one col still KOs

    # Save matrix
    df_kos_binary = df_kos_binary_temp.set_index("ko").transpose()

    if not os.path.exists(saving_dir): os.makedirs(saving_dir)
    df_kos_binary.to_csv(saving_dir+"all"+".csv", header=True, index=True)
