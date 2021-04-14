import numpy as np
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


def make_KO_binary_plots_colourized():

    # Read files
    for file in source_files:
        df = pd.read_csv(file, index_col=0)
        pathway_name = file[len(source_dir):-4]


        # df.index = df.index.str.split(".").str[0]
        # # Add second index for each Group

        # Split groups and make different values for 'KO present' in each
        group1 = df.loc[df.index.str.startswith('Ecoli')]
        group2 = df[df.index.str.startswith('Ent')]
        group3 = df[df.index.str.startswith('KECS')]
        group4 = df[df.index.str.startswith('Pm')]
        group5 = df[df.index.str.startswith('Ps')]
        group6 = df[df.index.str.startswith('St')]

        group1[group1!=0]=1
        group2[group2!=0]=2
        group3[group3!=0]=3
        group4[group4!=0]=4
        group5[group5!=0]=5
        group6[group6!=0]=6

        # Put groups again
        df2 = pd.concat([group1, group2, group3, group4, group5, group6])

        # Get order of dendogram
        am = sns.clustermap(df)
        order_rows = am.dendrogram_row.reordered_ind
        order_cols = am.dendrogram_col.reordered_ind

        # reindex
        df2.index = order_rows
        df2 = df2.sort_index(ascending=True)
        df2.columns = order_cols
        df2 = df2.sort_index(ascending=True, axis=1)

        # Make plot
        plt.figure(figsize=(10, 7))
        am = sns.heatmap(df2, cmap='tab10',
                            cbar=False)
        am.show()
        exit()
        # # Nice labels, edit as desired :)
        # am.ax_row_dendrogram.set_visible(False)
        # am.ax_col_dendrogram.set_visible(False)
        # plt.xlabel('Strain')
        # plt.ylabel('KOs')
        # plt.title(pathway_name)

        # df = pd.concat([group1, group2, group3,
        #                  group4, group5, group6],
        #             keys=["Ecoli", "Ent", "KECS", "Pm", "Ps", "St"])

        # https://stackoverflow.com/questions/3280705/how-can-i-display-a-2d-binary-matrix-as-a-black-white-plot

        # # Define colour palettes
        # cm = ['Blues', 'Reds', 'Greens', 'Oranges', 'Purples', 'winter']
        # a, axs = plt.subplots(6, 1, gridspec_kw={'wspace': 0})
        # for i, (s, a, c) in enumerate(zip(df.index.unique(), axs, cm)):
        #     # print(np.array([df.loc[s].values])
        #     # sns.heatmap(np.array([df.loc[s].values]), xticklabels=df.index, yticklabels=[s], annot=True, fmt='.2f', ax=a, cmap=c, cbar=False)
        #     am = sns.clustermap(df.loc[s], yticklabels=df.loc[s].index, xticklabels=df.columns,
        #                    cmap=c, cbar_pos=None)
        #     am.ax_row_dendrogram.set_visible(False)
        #     am.ax_col_dendrogram.set_visible(False)
        #     if i>0:
        #         a.xaxis.set_ticks([])
        #
        # plt.show()
        # exit()

        # Make plot
        # plt.figure(figsize=(10, 7))
        # am = sns.clustermap(df, cmap='tab10',
        #                     cbar_pos=None)
        # # Nice labels, edit as desired :)
        # am.ax_row_dendrogram.set_visible(False)
        # am.ax_col_dendrogram.set_visible(False)
        # plt.xlabel('Strain')
        # plt.ylabel('KOs')
        # plt.title(pathway_name)
        #
        # plt.show()
        exit()

        # Save
        if not os.path.exists(saving_dir): os.makedirs(saving_dir)
        plt.savefig(saving_dir + pathway_name + saving_format)
        plt.close()

if __name__ == "__main__" :
    make_KO_binary_plots_colourized()