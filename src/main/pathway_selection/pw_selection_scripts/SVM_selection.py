import pandas as pd
# import os
import glob
from sklearn.feature_selection import RFE
from sklearn.svm import SVR


bigmatrices_directory =  '../../created/big_matrices/'
all_dir = glob.glob(bigmatrices_directory+ "*.csv" )

saving_directory_selected_pathways = '../FS_Selected/'
saving_directory_ranked_pathways = '../FS_Ranked/'



def call_SVM():



    list_selected = []
    list_ranked = []
    list_measures = []
    # Perform the process for every interaction index.
    for file_path in all_dir:
        df_Xy = pd.read_csv(file_path, index_col=0)
        df_Xy = df_Xy.fillna(0)
        name_measure = file_path[27:-4] # CHANGE!!!
        list_measures.append(name_measure)
        print(name_measure)
        # Get X (matrix with data) and y (column with labels).
        df_X = df_Xy.iloc[:,[0,2,3,4,5,6,7]] # CHANGE!!!
        df_y = df_Xy.iloc[:, 1]

        # Perform SVM (Support Vector Machine sup.learning).
        estimator = SVR(kernel="linear")

        # Perform RFE (Recursive Feature Elimination).
        selector = RFE(estimator, step=1)
        
        try:
            selector = selector.fit(df_X, df_y)
        except:
            print('Error in ' + file_path)
            continue

        # Get Selected pathways (using default parameters).
        selected_feat = df_X.columns[selector.support_==True].tolist()
        list_selected.append(selected_feat)

        # Get Ranked pathways.
        ranked_feat = selector.ranking_
        df_selectFeat = pd.DataFrame()
        df_selectFeat['pathways'] = df_X.columns.tolist()
        df_selectFeat['ranks'] = ranked_feat
        df_selectFeat = df_selectFeat.sort_values(by='ranks')
        list_ranked.append(df_selectFeat.pathways)
        # list_ranked.append('\n\n')


        print(df_selectFeat)
        exit()

        # Save the results for all the interaction indexes together.
        # with open(saving_directory_selected_pathways+'SelFeat_'
        #                     +labeling+'_SVM.txt', 'w') as file_:
        #     file_.write(str(list_measures) + '\n\n' + str(list_selected))
        # with open(saving_directory_ranked_pathways+'RankFeat_'
        #                     +labeling+'_SVM.txt', 'w') as file_:
        #     file_.write(str(list_measures) + '\n\n' + str(list_ranked))
