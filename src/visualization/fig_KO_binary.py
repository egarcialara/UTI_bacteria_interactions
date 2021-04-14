import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob

source_dir = "../../created/KO_binary_matrices/"
source_files = glob.glob(source_dir + "*.csv")

saving_dir = "../../figures/KO_binary/"
saving_format = ".pdf"


def make_KO_binary_plots():

    # Read files
    for file in source_files:
        df = pd.read_csv(file, index_col=0)
        pathway_name = file[len(source_dir):-4]

        # Make plot
        plt.figure(figsize=(10, 7))
        am = sns.clustermap(df, cmap='Greys',
                         cbar_pos=None)
        # Nice labels, edit as desired :)
        am.ax_row_dendrogram.set_visible(False)
        am.ax_col_dendrogram.set_visible(False)
        plt.xlabel('Strain')
        plt.ylabel('KOs')
        plt.title(pathway_name)

        # Save
        if not os.path.exists(saving_dir): os.makedirs(saving_dir)
        plt.savefig(saving_dir + pathway_name + saving_format)
        plt.close()



if __name__ == "__main__" :
    make_KO_binary_plots()
