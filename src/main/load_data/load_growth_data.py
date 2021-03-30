import pandas as pd
import glob
import numpy as np
import scipy.io as sio


growth_matrices_directory = "../../data/growth_matrices/"
all_dir = glob.glob(growth_matrices_directory + "*.mat")

order_file_directory = "../../data/growth_matrices/"
names_file_directory = "../../data/growth_matrices/"

saving_dir = "../../created/growth/"


def mat_to_pandas():

    # Two files: growth rate and MaxOD
    for mat_name in all_dir:

        mat = sio.loadmat(mat_name)
        mat = {k:v for k, v in mat.items() if k[0] != '_'} # save only entry with data, not __version__, etc
        key_list = [x for x in mat.keys()]
        if len(key_list) >= 2: exit("Can't read .mat file")

        n = len(mat[key_list[0]])
        df = pd.DataFrame()
        for i in range(0, n):
            data = pd.DataFrame({k: pd.Series(v[i]) for k, v in mat.items()})
            df[i] = data[key_list[0]].tolist()

        # Order rows
        df2 = pd.read_csv(order_file_directory+'order_matrices.csv', sep=' ', header=None)
        df.index = df2.loc[0].tolist()

        # Put the names of species instead of numbers
        df = give_names(df)

        # transpose & put rows up-down to mimic figures
        df= df.T
        df = df.iloc[::-1]
        df = np.log(df)

        mat_name_short = mat_name[len(growth_matrices_directory):-4]
        df.to_csv(saving_dir+mat_name_short+".csv",header=True, index=True)

def give_names(df):

    # Open excel file
    name_df = pd.read_excel(names_file_directory + 'UTI_bacteria_names.xlsx', usecols="A:C")

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
        df = df.drop([2], axis=1) # only for GR

    df.index = list_names
    df.columns = list_names

    return df