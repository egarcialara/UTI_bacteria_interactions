#TODO
# fix import of util files (one directory back)

######
import pandas as pd
import pylab


import os
import glob
import csv
import re
import sys
import seaborn as sns
import matplotlib.pyplot as plt
# import urllib2
import math
import numpy as np
import requests

# from bioservices.kegg import KEGG
# s = KEGG()

from load_data.util.KEGG_pathways import get_list_ko
from load_data.util.strains_names import change_names
from load_data.util.create_KO_matrices import create_binary_matrix

KO_lists_directory = "../../data/KO_lists/"
all_dir = glob.glob(KO_lists_directory + "*_KO.txt")
len_dir_name = len(KO_lists_directory)

saving_dir = "../../created/KO_binary_matrices/"


''' Give a folder containing files .txt that contain
 1) identifier of bacteria strain and protein and
 2) KO id (if present)

 Return a csv file with KO in rows and strain in column, with
    binary -- 1/0 if pathway reaction is present/absent in strain
    counts -- number of reactions of a pathway present in strain
 plus a heatmap representing binary or counts of these KO in a particular KEGG pathway
'''




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

    # Create dataframe where to concatenate kos
    df_general = pd.DataFrame()

    #request the pathway KO list from KEGG
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
        abundance_list = []
        df_abundance = pd.DataFrame()
        for strain in all_dir:
            name_strain = strain[len_dir_name:-4] # append only strain name, not full dir
            df_kos_binary_temp = create_binary_matrix(strain, name_strain, df_kos_binary_temp, pwname) #add strains as columns, one col still KOs
            # df_all_kos, df_kos_binary = creating_matrix_abundances(ko_in_path, pwname, False, 'matrix_binary_AllKos')

        # Save matrix
        df_kos_binary = df_kos_binary_temp.set_index("ko").transpose()
        pwname_save = pwname.replace("/", "-")
        df_kos_binary.to_csv(saving_dir+pwname_save+".csv", header=True, index=True)





# def sum_pathways(df, counts, div):
#     # for all the strains sum the df_kos_binary
#     temp_df = pd.DataFrame()
#     df = df.T
#     name_temp = 0
#     # print df.shape
#     for column1 in df:
#         for column2 in df:
#             name_temp += 1
#             temp_df[name_temp] = df[column1] + df[column2]
#     if counts == False:
#         temp_df[temp_df>0] = 1
#     temp_df.loc['Total']= temp_df.sum()

#     n = len(temp_df.columns)
#     m = int(math.sqrt(n))

#     new_df = pd.DataFrame()
#     index = temp_df.columns.tolist()
#     for iterat in range(0, m):
#         for i in range(0, m):
#             j = (iterat)*m + i
#             new_df.loc[iterat, i] = temp_df.loc["Total", index[j]]

#     # A+B/A - 1
#     # compl >= 0
#     if div == True:
#         # new_df.sort_index()
#         i = 0
#         for column in df:
#             new_df[i] = new_df[i]/df[column].sum()
#             i += 1
#         # the rows are A, columns B
#     new_df = new_df - 1



#     # Change names from 1-x to real name
#     # Sort to make sure they get their name
#     list_names = list(df)
#     new_df = change_names(new_df,list_names, rows=True, cols=True)
#     new_df.sort_index(axis=0)
#     new_df.sort_index(axis=1)

#     return new_df


# if __name__ == "__main__":
#     matrix_abundances_per_pathway()
