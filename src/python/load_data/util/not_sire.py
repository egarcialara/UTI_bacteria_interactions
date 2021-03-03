
def df_pwID_pwNAME():
    ''' Creates a dataframe matching the names with the IDs
    of the pathways that have higher std
    It is enough to call once, it saves a csv file'''
    #request the pathway KO list from KEGG
    # try:
    #     with open('high_std_pw_new.csv', 'rb') as f:
    #         reader = csv.reader(f)
    #         list_paths = list(reader)[0]
    # except IOError:
    #     print 'File does not exist'

    df_pws = pd.read_csv('high_std_pw_new.csv', header=0, names=['name', 'std'])
    list_paths = df_pws['name'].tolist()

    # Map names with ids
    kegg_pathway_list = requests.get('http://rest.kegg.jp/list/pathway')
    kegg_pathway_id_name = kegg_pathway_list.content.split('\t')
    df = pd.DataFrame()
    # First reaction, glycolisis, will always be there
    df.loc[0, 'id'] = kegg_pathway_id_name[0][5:]
    df.loc[0, 'name'] = kegg_pathway_id_name[1].split('\n')[0]
    # select the kegg pathways that are in the list_paths and put them in a df
    for n in range(1, len(kegg_pathway_id_name)-1):
        if kegg_pathway_id_name[n+1].split('\n')[0] in list_paths:
            df.loc[n, 'id'] = kegg_pathway_id_name[n].split('\n')[1][5:]
            df.loc[n, 'name'] = kegg_pathway_id_name[n+1].split('\n')[0]
    df.to_csv('results/id_and_name_pws_highStd.csv', index=True)
    print 'Saved pw_ID/pwNAME csv'




def matrix_per_HighStdPw(function):
    ''' Creates a dataframe with KOs per pathway
    and calls the function to create the matrix using only one pw at a time
    Saves the heatmap of each pathway'''

    # Get the df created (once) before (pwID/pwNAMES with high std)
    df = pd.read_csv('results/id_and_name_pws_highStd.csv', names=['id', 'name'], sep=',', header=0)

    # for every pw (highStd), calculate matrix strains/KOs
    # for i in range(0, len(df['id'].tolist())):
    for i in df.index:
        # Create df where to concatenate KOs
        df_abundance = pd.DataFrame()
        pwid = df.loc[i, 'id'][3:]
        pwname = df.loc[i, 'name']
        # get the KOs of the pw
        url = str("http://rest.kegg.jp/link/ko/map" + pwid)
        try:
            data = urllib2.urlopen(url, timeout=20).read()
        except ValueError:
            print "Error retrieving pathway IDs"
            pass
        data = data.split('\n')
        ko_in_path = []
        for row in data[:-1]:
            ko_in_path.append(row[-6:])

        df_kos_binary = creating_matrix_abundances(ko_in_path, pwname, False, 'df_abundance')

        if function == 'ko_binary_perPW':
            name = 'ko_matrix_' +str(pwname[:10])+  '.png'

        elif function == 'ko_complementarity_perPW':
            # function ko_pair_comparison(df_kos_binary)
            matrix = sum_pathways(df_kos_binary, False, True)
            pwname = pwname.replace('/', '_')
            # name = 'complementarity_' +pwname +  '_ordered.png'

        matrix = matrix.fillna(0) #fill NaN
        matrix = matrix.replace(np.inf, np.nan) #inf to NaN
        matrix.fillna(matrix.max().max()) #fill Inf (new NaN)

        # Sort the genera in the same order as Marjoen:
        # Ent, St, Ps, Pm, KECS, Ecoli (from down-up/left-right)
        # rows
        a = matrix[matrix.columns=='Ent']
        b = matrix[matrix.columns=='St']
        c = matrix[matrix.columns=='Ps']
        d = matrix[matrix.columns=='Pm']
        e = matrix[matrix.columns=='KECS']
        f = matrix[matrix.columns=='Ecoli']
        concate = pd.concat([f, e, d, c, b, a])
        # columns
        g = concate['Ent']
        h = concate['St']
        i = concate['Ps']
        j = concate['Pm']
        k = concate['KECS']
        l = concate['Ecoli']
        concat2 = pd.concat([g, h, i, j, k, l], axis=1)

        D = pd.DataFrame()
        for i in [g, h, i, j, k, l]:
            #for group Ent, St, ... cluster strains
            # column-blocks
            clustergrid = sns.clustermap(i, col_cluster=True, row_cluster=False)
            plt.close()
            ord_ind = clustergrid.dendrogram_col.reordered_ind
            i.loc['order'] = ord_ind
            i = i.sort_values(by='order', axis=1)
            i = i.drop('order', axis=0)
            D = pd.concat([D, i], axis=1)

        a = D[D.index=='Ent']
        b = D[D.index=='St']
        c = D[D.index=='Ps']
        d = D[D.index=='Pm']
        e = D[D.index=='KECS']
        f = D[D.index=='Ecoli']
        E = pd.DataFrame()
        for i in [a, b, c, d, e, f]:
            #for group Ent, St, ... cluster strains
            #row - blocks
            clustergrid = sns.clustermap(i, col_cluster=False, row_cluster=True)
            plt.close()
            ord_ind = clustergrid.dendrogram_row.reordered_ind
            i['order'] = ord_ind
            i = i.sort_values(by='order', axis=0)
            i = i.drop('order', axis=1)
            E = pd.concat([i, E], axis=0)

        E = E.fillna(0) #fill NaN
        E = E.replace(np.inf, np.nan) #inf to NaN
        E.fillna(E.max().max()) #fill Inf (new NaN)

        # matrix.to_csv('../fig compl_growth/compl/compl_'+pwname+'.csv', index=True)
        # print 'matrix of' + pwname + 'created'
        name = 'compl_ordered'
        name_pw = pwname
        plt.figure()
        am = sns.heatmap(E, cmap='Greys')
        plt.title(pwname)
        plt.show(am)
        # exit()
        # plt.savefig('plots_tuesday/compl_order_'+pwname+'_new.png')
        print pwname, 'matrix saved'
    # exit()