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



def creating_matrix_abundances(ko_in_path, pwname, first, funct):
    ''' This function compares a given list of ko_in_path
    with the list of kos for every strain

    INPUT: 
    - ko_in_path: list of KOs present in strain S in pathway P
    - pwname:     text name of the pathway
    - first:      first strain to be computed?
    - funct:      ???
    '''

    # abundance_list = []
    # if first:
    #     list_strains = []
    # df_all_kos = pd.DataFrame()

    # Open all the files in the directory
    # n = 1
    # df_abundance = pd.DataFrame()

    # for strain in all_dir:
        
        # if first:
        #     list_strains.append(name_strain)
        # n += 1
        # try:
        #     inp = open(strain, 'r')

        # except IOError:
        #     print('File does not exist')

        # read the strain-KO table and assign names to columns
        # df_temp = pd.read_csv(inp, names=['pid', 'ko'], sep='\t', header=None)

        # # get rid of NAs
        # df_temp.dropna(inplace=True)

        # # keep only KOs present in pathway
        # if funct != 'matrix_binary_AllKos': #???
        #     df_temp = df_temp[df_temp['ko'].isin(ko_in_path)]

        # if funct != 'std':
        # count occurrences of KOs
        # ser_counts = df_temp['ko'].value_counts()
        # create new data frame with counts
    df_trans = pd.DataFrame(ser_counts).rename(columns={'ko': strain.rsplit('/', 2)[-1][:-7]}).transpose()
    # concatenate dataframes; if KOs are not present, NAs will be introduced
    df_all_kos = pd.concat([df_all_kos, df_trans], axis=0,sort=True) ## sort=True for now as old behaviour, not sure other behaviour rn

    if funct=='std' or funct=='unique_counts_change':
        # count occurrences of KOs (per pathway per strain)
        ser_counts = len(df_temp["ko"].unique())

        # ### If total counts without considering pathway:
        # # create new data frame with counts
        # df_trans = pd.DataFrame(ser_counts).rename(columns={'ko': strain.rsplit('/', 2)[-1][:-7]}).transpose()
        # # concatenate dataframes; if KOs are not present, NAs will be introduced
        # df_abundance = pd.concat([df_abundance, df_trans], axis=0)

        # dont include empty pathways
        if len(ko_in_path)==0:
            pass#break
        if ser_counts==0:
            abund_in_pw = 0
            # print "Take this out next time"
        elif len(ko_in_path)>0:
            abund_in_pw = float(ser_counts)/len(ko_in_path)
            # abund_in_pw = float(ser_counts.sum())/len(ko_in_path)
        if abund_in_pw > 1:
            print(abund_in_pw)
            abund_in_pw = 1
        abundance_list.append(abund_in_pw)
        df_abundance.loc[name_strain, pwname] = abund_in_pw

    # concat will lead to NAs if an organism does not have certain KOs; replace them by 0
    df_all_kos.fillna(0, inplace=True)
    df_kos_binary = df_all_kos.copy()
    df_kos_binary[df_kos_binary > 0] = 1  # possible to reate other matrix without this for other uses
    # df_all_kos.T.to_csv('results/ko_counts_aa1.csv', index=True)
    # df_kos_binary.to_csv('results/ko_binary_aa1.csv', index=True)

    # change for the needs of the function ???
    if funct == 'matrix_binary_AllKos':
        return df_all_kos, df_kos_binary
    elif funct == 'std':
        return df_abundance, abundance_list
    else:
        return df_kos_binary






def matrix_abundances_per_pathway(std=None):
    ''' counts KO per pathway per species normalized
    std True/False if you want to select rows above threshold std'''
    # Create dataframe where to concatenate kos
    df_general = pd.DataFrame()
    #request the pathway KO list from KEGG
    kegg_pathway_request = requests.get('http://rest.kegg.jp/list/pathway')
    kegg_pathway_list = kegg_pathway_request.text

    # Open all the files in the directory
    list_std = []
    df_abundance_all = pd.DataFrame()
    rep = 1
    for line in kegg_pathway_list.split('\n')[:-1]:
        print(f"Pathway n. {rep}")
        # if rep >5:
        #     break
        ko_in_path, pwname = get_list_ko(line)


        ## If in ko_sum_in_pw_matrix were using the Alternative
        ## to use only pws with high std, then un-comment these lines
        # df_pws = pd.read_csv('high_std_pw_new.csv', header=0, names=['name', 'std'])
        # list_paths = df_pws['name'].tolist()
        # if pwname not in list_paths:
        #     pass

        df_abundance, abundance_list = creating_matrix_abundances(ko_in_path, pwname, False, 'std')

        df_all_kos, df_kos_binary = creating_matrix_abundances(ko_in_path, pwname, False, 'matrix_binary_AllKos')
  
        list_std.append(df_abundance[pwname].std())
        df_abundance_all[pwname] = df_abundance[pwname]

        # if all the numbers are the same, drop, otherwise problems in python
        if all(x == abundance_list[0] for x in abundance_list):
            df_abundance = df_abundance.drop(pwname, axis=1)

        # Make df to store pws and their std
        m = df_abundance.std()
        if rep==1:
            df_general['std'] = m
        else:
            try:
                df_general.loc[pwname, 'std'] = float(m)
            except:
                rep+=1
                continue
        rep +=1
            # df_general['std'].append(m, ignore_index=True)


    # If the standard deviation of the values for strains, for a pathway
    # is below threshold, then delete row
    # I chose 10% median STD (of non-zero pathways) as threshold, can be changed
    if std:
        threshold = np.median(list_std)/5
        df_result = df_general.loc[df_general['std'] >= threshold]
        # Save a list of the pathways kept
        pw_kept = df_result.columns.tolist()
        df_result.to_csv('high_std_pw_new.csv')
        print('File high_std_pw_new.csv created')
        return

    list_names = df_abundance_all.index.tolist()
    df_abundance_all = change_names(df_abundance_all, list_names, rows=True, cols=False)

    # print(df_abundance_all)

    return df_abundance_all
