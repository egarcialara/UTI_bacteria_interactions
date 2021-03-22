
import pandas as pd
import os
import glob
import numpy as np


saving_directory = '../../created/big_matrices/'
growth_matrix_directory = '../../created/growth/MaxOD_3.mat.csv'
interaction_matrix_directory = '../../created/interaction_matrices/'


# Choose how to split the labels
# e.g. '1000': a=1, b=c=d=0: two class classification
# a = if n>0.22             (positive effect of the donor on acceptor's growth)
# b = if 0.22>n>-0.22       (neutral effect)
# c = if -0.22>n>-0.51      (negative effect due to competition)
# d = if n<-0.6             (negative effect due to inhibition)
label_combinations = ['1000']#, '0010']
growth_threshold = 0.22

# Where to save the resulting big matrices.
# BigMat_dir = saving_directory + 'NxN/'
# if not os.path.exists(BigMat_dir):
#     os.makedirs(BigMat_dir)

if not os.path.exists(saving_directory):
    os.makedirs(saving_directory)

def big_matrix_create():
    ''' Creates the big matrix containing
    rows: N*N (strain * strain)
    columns: p pathways
    The value of each cell will be the complementarity/competition/other
        between the strains, in pathway p'''


    # For every interaction table
    for item in ['complementarity_1', 'complementarity_2']:#, 'sim4']:
                                #, 'compl3', 'sim1', 'sim2', 'sim3']:
        all_dir = glob.glob(interaction_matrix_directory+item+"/*.csv")
        print(item)
        big_matrix = pd.DataFrame()

        first=True

        # For every pathway 
        for path in all_dir:

            # Read interactions
            df_complPathway = pd.read_csv(path, index_col=0)
            df_complPathway.index = df_complPathway.columns
            name_dist = len(interaction_matrix_directory)+len(item) + 1
            pwname = path[name_dist:-4]

            # Read growth
            df_growth = pd.read_csv(growth_matrix_directory, index_col=0)
            df_labels = df_growth.copy()
            df_labels[df_growth > growth_threshold] = 1
            df_labels[df_growth <= growth_threshold] = 0 #check less or equal!


            # TODO remove!!
            df_labels = df_labels.iloc[0:66, 0:66]
            df_labels.index = df_complPathway.columns.tolist()
            df_labels.columns = df_complPathway.columns.tolist()

            # For every row (i = donor)
            for i in df_complPathway.index:
                # For every column (j = acceptor)
                for j in df_complPathway.columns:
                    name_row = str(i)+'x'+str(j)
                    # big_matrix KECS(donor) x Ent(acceptor)
                    big_matrix.loc[name_row, pwname] = (
                                                    df_complPathway.loc[i, j])

                    if first:
                        big_matrix.loc[name_row, "y"] = (
                                                    df_labels.loc[i, j])
            first = False

        big_matrix = big_matrix.replace(np.inf, np.nan)
        big_matrix = big_matrix.replace(-np.inf, np.nan)

        big_matrix.to_csv(saving_directory +item+ '.csv')
    return


def label_matrix(a, b, c, d, comb):
    ''' Creates the Y matrix for the corresponding matrix above,
    but instead of having GrowthYield MaxOD value, there will be a label:
    if n>0.22
    if 0.22>n>-0.22
    if -0.22>n>-0.51
    if n<-0.6 (usually np.nan because it is outside of our scope)'''

    BigMat_withlabel_directory = saving_directory + 'NxN+y_label('+comb+')/'

    # Read data of growth rate or yield.
    df = pd.read_csv(growth_matrix_directory, index_col=0)
    df = df.drop('MM', axis = 0)
    df = df.drop('MM', axis = 1)
    list_names = ['Ecoli', 'Ent', 'KECS', 'Pm', 'Ps', 'St']

    # Give labels to the MaxOD matrix.
    df[df>0.22] = a
    df[(df<=0.22) & (df>-0.22)] = b
    df[(df<=-0.22) & (df>=-0.51)] = c
    df[df<-0.51] = d

    # Matrix to store the labels by Group (Ent, KECS, ...)
    df_labels = pd.DataFrame()

    # Majority voting for the group
    for item1 in list_names: # donor
        for item2 in list_names: # acceptor
        # Temporal df to calculate majority per Donor and Acceptor (Ent x St).
            df_temp = df.loc[df.index.str.contains(item1), (
                                        df.columns.str.contains(item2))]
            list_all = []
            for col in df_temp:
                list_all.extend(df_temp[col])
            counter = {}
            for i in list_all:
                if i in counter:
                    counter[i] += 1
                else:
                    counter[i] = 1

            # Choose the majority vote.
            popular_nums = sorted(counter, key = counter.get, reverse = True)
            top = popular_nums[0]
            # Give this label value to the df.
            df_labels.loc[item1, item2] = top


    # Read big matrix NxN in rows, all pathways in columns
    # combination of names in index (e.g. Ecoli3 x Ecoli19)
    path_list = glob.glob(saving_directory + 'NxN/*.csv')
    for path in path_list:
        df_X = pd.read_csv(path, index_col=0)
        name_measure = path[20:-4]

        # Create columns to localize the strains in index name.
        df_X['name1'] = df_X.index.str.split('x').str[0]
        df_X['name2'] = df_X.index.str.split('x').str[1]
        # For every combination of e.g. EcolixEcoli give them the same label.
        for i in df_labels.index:
            for j in df_labels.columns:
                i2 = i[0:2]
                j2 = j[0:2]
                df_X.loc[((df_X.name1.str.contains(i2)) &
                            (df_X.name2.str.contains(j2))), 'y'] = (
                            df_labels.loc[i, j])

        df_X = df_X.drop(['name1', 'name2'], axis=1)
        df_X = df_X.dropna()
        if not os.path.exists(BigMat_withlabel_directory):
            os.makedirs(BigMat_withlabel_directory)
        df_X.to_csv(BigMat_withlabel_directory + name_measure + '.csv')
    return

def main():
    # Create a big_matrix
    big_matrix_create()
    # Add labels to big_matrix
    for i in range(0, len(label_combinations)):
        a = int(label_combinations[i][0])
        b = int(label_combinations[i][1])
        c = int(label_combinations[i][2])
        d = int(label_combinations[i][3])
        combination = str(label_combinations[i])
        print(combination)
        label_matrix(a, b, c, d, combination)


# if __name__=="__main__":
    # main()