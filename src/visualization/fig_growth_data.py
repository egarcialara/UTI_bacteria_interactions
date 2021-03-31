import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

source_dir = "../../created/growth/"
# source_file = source_dir + "GR_3.csv"   # choose one file
source_file = source_dir + "MaxOD_3.csv"  # or another

saving_dir = "../../figures/growth/"
saving_format = ".pdf"

def make_growth_plot():

    # Read file
    df = pd.read_csv(source_file, index_col=0)

    # Make values fall from [-2, 2] Only for visualization in heatmap
    df[df>2] = 2
    df[df<-2] = -2

    # Make plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, cmap='bwr')
    # Nice labels, edit as desired :)
    labels = df.columns.str.split(".").str[0]
    plt.xticks(range(len(labels)), labels)
    plt.xlabel('Acceptor')
    plt.ylabel('Donor')

    # Save
    saving_name = saving_dir + source_file[len(source_dir):-4] + saving_format
    if not os.path.exists(saving_dir): os.makedirs(saving_dir)
    plt.savefig(saving_name, dpi=300)
    plt.close()

if __name__ == "__main__" :
    make_growth_plot()