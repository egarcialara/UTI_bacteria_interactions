# Creating the figures


### How to run it

The working directory is the main folder, e.g. "/home/Projects/UTI_bacteria_interactions/".
The default saving directory is `<working_directory>/figures/`.

__Fig. 1__

Combination of three figures: heatmap of the binary KO matrix,
a scatter plot of the annotated genes by KEGG, and
a scatter plot with an overview of the correlation between an interaction index and growth.

- How to: Have the scripts `fig1a.R`, `fig1b.R` and `fig1c.R` in the same folder.
- Then: run `fig1.R`. It reads the aforementioned scripts with `source()`, and creates a separate legend.

__Fig. 2__

Heatmaps for the interaction indexes.

- How to: First, run the script `/util/fig2/main.py` to create the interaction indexes for 
the pathways wanted. In this case: a module and all KOs. If you want to add 
more tables in the figure that are already created (e.g. pathways),
make sure to add their directory in `fig2.R`.
- Make sure that the script `fig2_function.R` is in the same folder.
- Then: run `fig2.R` to create the actual figures.

__Fig. 3__

Scatter plots for an interaction index and a growth measure.

- How to: Make sure `fig3_function.R` is in the same folder.
- Then: run `fig3.R`. Edit file names and directories as needed.

__Fig. 4__

Map of a pathway, to visualize the KEGG orthologs in order. It is built for Histidine metabolism, but it can be customized.

- How to: run `fig4.R`. You can find the required files in `/util/fig4/histidine/`.


### Requirements
Common R packages only. The list of packages used are listed at the top of each script.
