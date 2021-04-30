# Creating the figures

_Note: this text is a draft. Any edits/feedback is welcome._



### How to run it

The working directory is the main folder, e.g. "/home/Projects/UTI_bacteria_interactions/".
The default saving directory is "<working_directory>/figures/".

__Fig. 1__

Combination of three figures: heatmap of the binary KO matrix,
a scatter plot of the annotated genes by KEGG, and
a scatter plot with an overview of the correlation between an interaction index and growth.

- How to: run the scripts `fig1a.R`, `fig1b.R` and `fig1c.R` to create the individual figures.
- Then: run `fig1.R` to merge the 3 figures and the legend.

__Fig. 2__

Heatmaps for the interaction indeces.

- How to: First, run the script `main.py` to create the interaction indeces for modules and all KOs.
- Then: run `fig2.R` to create the actual figures.

__Fig. 3__

Scatter plots for an interaction index and a growth measure.

- How to: run `fig3.R`. It has `fig3_function.R` as source for the main functions.

### Requirements
Common R packages only. The list of packages used are listed at the top of each script.
