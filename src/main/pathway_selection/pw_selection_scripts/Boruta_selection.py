# import subprocess
# import pandas as pd
# import os
import pandas as pd
import glob
from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy

# R_install_file = "pathway_selection/pw_selection_scripts/util/install_R_packages.R"

# R_script_file = "pathway_selection/pw_selection_scripts/util/boruta.R"

bigmatrices_directory =  '../../created/big_matrices/'
all_dir = glob.glob(bigmatrices_directory+ "*.csv" )
saving_directory_selected_pathways = '../../FS_Selected/'
saving_directory_ranked_pathways = '../../FS_Ranked/'


def call_Boruta():


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

        # define random forest classifier, with utilising all cores and
        # sampling in proportion to y labels
        rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
        # define Boruta feature selection method
        feat_selector = BorutaPy(rf, n_estimators='auto', verbose=0, random_state=1)
        # find all relevant features - 5 features should be selected
        feat_selector.fit(df_X.values, df_y.values)
        # check selected features - first 5 features are selected
        # feat_selector.support_
        # check ranking of features

        # call transform() on X to filter it down to selected features
        # X_filtered = feat_selector.transform(X)


    # process1 = subprocess.Popen(R_script_file)#,shell=True)
    # process1.wait()

    # subprocess.call(R_script_file,shell=True)

    # POSSIBLE TROUBLESHOOTING:
    # if this doesnt' work, make sure the file has executable rights
    # more info in 