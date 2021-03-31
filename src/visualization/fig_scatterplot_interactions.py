import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob

# Source interactions
source_interactions_dir = "../../created/interaction_matrices/"
interaction = "complementarity_2"  # choose interaction!
source_interactions_files = glob.glob(source_interactions_dir +
                                      interaction + "/*.csv")
# Source growth data
source_growth_dir =  "../../created/growth/"
growth = "MaxOD"
source_growth_file = source_growth_dir + growth + "_3.csv"  # or GR_3.csv

# Saving directories
saving_dir = "../../figures/scatterplot/" + interaction + "/"
saving_format = ".pdf"

def make_scatterplot():

    # Read the experimental growth file
    df_mat = pd.read_csv(source_growth_file, index_col = 0)
    # Group the strains by genera, drop MM
    df_mat = df_mat.fillna(0)
    average_mat = df_mat.groupby(lambda col: col[:2], axis=1).mean()
    average_mat = average_mat.groupby(lambda col: col[:2], axis=0).mean()
    average_mat = average_mat.drop('MM', axis = 0)
    average_mat = average_mat.drop('MM', axis = 1)
    order = ['En', 'St', 'Ps', 'Pm', 'KE', 'Ec']
    average_mat = average_mat[order]
    average_mat = average_mat.loc[order]
    average_mat.columns = ['Ent', 'St', 'Ps', 'Pm', 'KECS', 'Ecoli']

    # Read the different interaction matrices
    for file in source_interactions_files:
        lengthname = len(source_interactions_dir)+len(interaction) + 1
        name = file[lengthname:-4]
        try:
            df_pw = pd.read_csv(file, index_col = 0)
        except:
            continue

        # Make smaller df, grouping by each item.
        groupedA = df_pw.groupby(lambda col: col[:2], axis=1)
        averageA = groupedA.mean()
        grouped2A = averageA.groupby(lambda col: col[:2], axis=0)
        average_pw = grouped2A.mean()
        order1 = ['En', 'St', 'Ps', 'Pm', 'KE', 'Ec']
        order = ['Ent', 'St', 'Ps', 'Pm', 'KECS', 'Ecoli']
        average_pw = average_pw[order1]
        average_pw = average_pw.loc[order1]
        average_pw.columns = order

        #########################################################
        # Start building the scatterplot
        fig = plt.figure()
        ax = plt.subplot(111)
        colors = ['b', 'g', 'r', 'c', 'm', 'y']
        shape = ['o', '^', 'v', 's', '*', 'D']
        n = 0
        list_X = []
        list_Y = []
        # Transform matrices into 1D
        for col in average_pw:
            X = average_pw[col].tolist()
            Y = average_mat[col].tolist()
            list_X.extend(X)
            list_Y.extend(Y)

            # Plot each point separately, choosing the shape and colour
            # that corresponds depending on acceptor/donor.
            for i in range(0, len(X)):
                if i == 4:
                    ax.plot(X[i], Y[i], marker=shape[i], color=colors[n],
                            markersize=12, label=col)
                elif i in [0, 1, 2]:
                    ax.plot(X[i], Y[i], marker=shape[i], color=colors[n],
                            markersize=9, label=col)
                else:
                    ax.plot(X[i], Y[i], marker=shape[i], color=colors[n],
                            markersize=8, label=col)
            n +=1

        #Create custom artists.
        col1 = plt.Line2D((0, 1), (0, 0), color='b', marker='o', linestyle='', markersize=6)
        col2 = plt.Line2D((0, 1), (0, 0), color='g', marker='o', linestyle='', markersize=6)
        col3 = plt.Line2D((0, 1), (0, 0), color='r', marker='o', linestyle='', markersize=6)
        col4 = plt.Line2D((0, 1), (0, 0), color='c', marker='o', linestyle='', markersize=6)
        col5 = plt.Line2D((0, 1), (0, 0), color='m', marker='o', linestyle='', markersize=6)
        col6 = plt.Line2D((0, 1), (0, 0), color='y', marker='o', linestyle='', markersize=6)
        sym1 = plt.Line2D((0, 1), (0, 0), color='k', marker='o', linestyle='', markersize=6)
        sym2 = plt.Line2D((0, 1), (0, 0), color='k', marker='^', linestyle='', markersize=6)
        sym3 = plt.Line2D((0, 1), (0, 0), color='k', marker='v', linestyle='', markersize=6)
        sym4 = plt.Line2D((0, 1), (0, 0), color='k', marker='s', linestyle='', markersize=6)
        sym5 = plt.Line2D((0, 1), (0, 0), color='k', marker='*', linestyle='', markersize=8)
        sym6 = plt.Line2D((0, 1), (0, 0), color='k', marker='D', linestyle='', markersize=6)

        size1 = plt.Line2D((0, 1), (0, 0), color='b', marker='o', linestyle='', markersize=6*2)
        size2 = plt.Line2D((0, 1), (0, 0), color='b', marker='o', linestyle='', markersize=6*0.6)

        symbols = [col1, col2, col3, col4, col5, col6, sym1, sym2, sym3, sym4, sym5, sym6]
        words = ['Ent', 'St', 'Ps', 'Pm', 'KECS', 'Ecoli']

        sizes = [size1, size2]
        sizeswords = [r'$\uparrow$'+' KOs don.', r'$\downarrow$'+' KOs acc.']

        # Shrink current axis by 20%.
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis.
        leg1 = plt.legend(symbols[0:6], words, numpoints=1,
                          bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0,
                          title='Acceptor', fontsize=13)
        # Add the legend manually to the current Axes.
        ax = plt.gca().add_artist(leg1)
        leg2 = plt.legend(symbols[6:12], words, numpoints=1,
                          bbox_to_anchor=(1.02, 0.18), loc=3, borderaxespad=0,
                          title='Donor', fontsize=13)

        plt.title(name)
        plt.xlabel('Complementarity in pathway per group')
        plt.ylabel(growth)
        plt.xlim(xmin=0)

        if not os.path.exists(saving_dir): os.makedirs(saving_dir)
        plt.savefig(saving_dir + name + saving_format, dpi=200)
        plt.close()

if __name__ == "__main__" :
    make_scatterplot()