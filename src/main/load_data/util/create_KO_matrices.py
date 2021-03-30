import pandas as pd

def create_binary_matrix(strain, strain_name, ko_in_path, pwname):
    '''
    Creates a MxN matrix with
    M KOs belonging to a pathway
    N strains of interest

    INPUT:
    - ko_in_path: list of KOs present in strain S in pathway P
    - pwname:     text name of the pathway

    OUTPUT
    - df_kos_binary
    '''

    try:
        inp = open(strain, 'r')

    except IOError:
        print(f'File for {strain_name} does not exist')

    # read the strain-KO table and assign names to columns
    df_strain_kos = pd.read_csv(inp, names=['pid', 'ko'], sep='\t', header=None)
    df_strain_kos.dropna(inplace=True)
    df_strain_kos.drop_duplicates(subset ="ko", keep = 'first', inplace = True) 

    # add to matrix, keeping indices from KOs in pathway
    df_kos_binary = df_strain_kos.join(ko_in_path.set_index("ko"), how="right", on="ko").reset_index(drop=True)
    # if ko was there, 1, otherwise, 0
    df_kos_binary.loc[pd.notna(df_kos_binary["pid"]), "count"] = 1
    df_kos_binary.loc[pd.isna(df_kos_binary["pid"]), "count"] = 0
    # cleanup
    df_kos_binary = df_kos_binary.drop(["pid"], axis=1)
    df_kos_binary.rename(columns={'count':strain_name}, inplace=True)

    return(df_kos_binary)