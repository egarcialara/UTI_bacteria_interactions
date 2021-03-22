import pandas as pd
import glob
from scipy.stats import mannwhitneyu
import numpy as np


bigmatrices_directory =  '../../created/big_matrices/'
all_dir = glob.glob(bigmatrices_directory+ "*.csv" )
saving_directory_selected_pathways = '../../FS_Selected/'
saving_directory_ranked_pathways = '../../FS_Ranked/'


def call_WMW():


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
        # df_y = df_Xy.iloc[:, 1]


        results = df_X.apply(lambda d: mannwhitneyu(d[df_Xy.y==0], d[df_Xy.y==1]), axis=0)
        print(results)
        exit()
        # test, pvalues = mannwhitneyu(df_X.values, df_y.values, use_continuity=True, alternative=None)

        # index = pd.MultiIndex.from_product([
        #     ['school{0}'.format(n) for n in range(3)],
        #     ['class{0}'.format(n) for n in range(3)],
        #     ['student{0}'.format(n) for n in range(10)]
        # ])
        # d = pd.DataFrame({'course1': np.random.randint(0, 10, 90), 'course2': np.random.randint(0, 10, 90)},
        #              index=index)
        # print(d)
        # d2=d.groupby(level=0).apply(lambda t: mannwhitneyu(t.course1, t.course2))
        # print(d2)


        # d3=d.groupby(level=[0, 1]).apply(lambda t: mannwhitneyu(t.course1, t.course2))
        # print(d3)
        # exit()
        # print(pvalues)