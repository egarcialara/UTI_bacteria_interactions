import pandas as pd
# import os
import glob
import csv
# import re
import sys
import seaborn as sns
import matplotlib.pyplot as plt
# import urllib2
# import math
import numpy as np
# import xlrd
# import requests
# import scipy.spatial.distance as ssd
# from bioservices.kegg import KEGG
# s = KEGG()
import scipy.io as sio
# import process_ko_tables as p


growth_matrices_directory = "../../data/growth_matrices/"
all_dir_2 = glob.glob(growth_matrices_directory + "*.mat")

order_file_directory = "../../data/growth_matrices/"
names_file_directory = "../../data/growth_matrices/"

saving_dir = "../../created/growth/"



def mat_to_pandas():


    for mat_name in all_dir_2:

        mat = sio.loadmat(mat_name)


    # for ronda in [1, 2]:
    #     ronda = 2
    #     if ronda==1:
    #         mat = sio.loadmat('GR_3.mat')
    #     if ronda==2:
    #         mat = sio.loadmat('MaxOD_3.mat')
        df = pd.DataFrame()
        mat = {k:v for k, v in mat.items() if k[0] != '_'} # save only entry with data, not __version__, etc
        
        key_list = [x for x in mat.keys()]
        if len(key_list) >= 2: exit("Can't read .mat file")

        n = len(mat[key_list[0]])


        # if ronda ==1:
        #     n = len(mat['GR_Int_spentS_reorder_HR_cleaned_20160514_3']) # for GR
        # if ronda==2:
        #     n = len(mat['MaxOD_Int_spentS_reorder_20160514_3']) # for MaxOD
        for i in range(0, n):
            data = pd.DataFrame({k: pd.Series(v[i]) for k, v in mat.items()})
            # print(data)
            # exit()
            df[i] = data[key_list[0]].tolist()

        df2 = pd.read_csv(order_file_directory+'order_matrices.csv', sep=' ', header=None)
        df.index = df2.loc[0].tolist()

        # Put the names of species instead of numbers
        df = give_names(df)

        # transpose the matrix to mimic figures
        df= df.T
        # put rows up-down to mimic figures
        df = df.iloc[::-1]

        df = np.log(df)   # avoid warning pls, if 0 then idk

        mat_name_short = mat_name[len(growth_matrices_directory):]
        df.to_csv(saving_dir+mat_name_short+".csv",header=True, index=False)
        print(saving_dir+mat_name_short+".csv, created")

        # if ronda == 1:
        #     # df.to_csv('../5. week 5/fig compl_growth/GR2.csv')
        #     # Make values fall from [-2, 2] Only for visualization in heatmap
        #     df[df>2] = 2
        #     df[df<-2] = -2
        #     plt.figure(figsize=(10, 8))
        #     sns.heatmap(df, cmap='bwr')
        #     plt.xlabel('Acceptor')
        #     plt.ylabel('Donor')
        #     plt.savefig('GR_forPPT_feb2021.png',dpi=300)
        #     plt.close()
        #     print('File created')

        # if ronda == 2:
        #     # df.to_csv('../5. week 5/fig compl_growth/MaxOD2.csv')
        #     # df[df>2] = 2
        #     # df[df<-2] = -2
        #     # df.to_csv('../5. week 5/fig compl_growth/MaxOD_means.csv')
        #     # sns.heatmap(df, cmap='bwr')
        #     # df = np.log(df)
        #     plt.figure(figsize=(10, 8))
        #     sns.heatmap(df, cmap='seismic', vmax=2, vmin=-2)
        #     plt.xlabel('Acceptor')
        #     plt.ylabel('Donor')

        #     # df = df.replace(-np.inf, 0)
        #     # df = df.groupby(lambda col: col[:2], axis=1).mean()
        #     # df = df.groupby(lambda col: col[:2], axis=0).mean()
        #     # df[df>0.22] = 1
        #     # df[(df<=0.22) & (df>-0.22)] = 0
        #     # df[(df<=-0.22) & (df>=-0.51)] = -1
        #     # df[df<-0.51] = np.nan

        #     # print df.max().max()
        #     # print df.min().min()
        #     plt.savefig('MaxOD_forPPT_feb2021.png',dpi=300)
        #     plt.close()
        #     print('File created')
        #     exit()



def give_names(df):
    # # replace IDs by actual names

    # Open excel file
    name_df = pd.read_excel(names_file_directory + 'UTI_bacteria_names.xlsx')
    #
    name_df.index = name_df['Number'].tolist()
    name_df['indexlist'] = name_df['Number']
    df['indexlist'] = df.index
    df = pd.merge(df, name_df, on = 'indexlist', how='outer')

    df = df.dropna()
    # Change index in rows/columns by Group or Name of the strains
    list_names = df['Group'].tolist()
    # Drop the columns added before
    df = df.drop(['Number', 'Group', 'indexlist', 'Name'], axis=1)
    if len(list_names) < 72:
    # print df.columns
        df = df.drop([2], axis=1) #ony for GR
    # print df.columns
    df.index = list_names
    df.columns = list_names


    # print df[(df<0.6)].count().sum()# &  (df>-0.51)]
    # exit()

    return df