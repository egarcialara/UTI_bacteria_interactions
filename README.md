# [TITLE?] Using functional annotations to study pairwise interactions in a bacterial community

_Note: this text is a draft. Any edits/feedback is welcome._

### Goal
It is a Python tool for a quick _in silico_ exploratory analysis of metabolic interactions in
microbial communities.

In particular, it performs a series of steps:

- build indices of complementarity and competition, based on metabolic gene annotations
- compare these indices with the actual experimentally-derived growth data (correlation)
- rough selection of pathways that can distinguish the best between no/increase of growth

### Structure
The repository has 2 main initial folders: `src` and `data`. It also includes additional folders
that will contain the resulting tables (`created`) and figures (`figures`).

### How to run it

__To run the pipeline__, call `src/main/main.py`.
It calls several functions, that can be commented out if needed:
    
- `create_KOs_binary_matrix`: from files derived from e.g. BLASTKoala, it creates clean binary tables for each strain.
- `mat_to_pandas`: script customized for our experimental results. Feel free to edit.
- `create_interaction_matrices`: calls a different script for each index.
We included the ones in the text. Feel free to remove/add new ones as desired.
- `big_matrix_create`: creates a "big matrix" for each index, consisting of all pairs in the X-axis,
and all pathways in the Y-axis. The cells contain the relevant interaction value.
- `call_selections`: calls the pathway selection methods. Again, if you feel that
    a different selection strategy would improve your results, it is easy to remove/add a new method.

__To create the figures__, call the different scripts in `src/visualization/`.
Before running most of them, make sure that you have the required tables derived from running certain 
steps from the main pipeline.

### Requirements

The requirements for this repository are listed in `requirements.txt`. 
They can easily be installed using e.g. pip: `pip install -r requirements.txt`.

### Other
The code is part of a publication that can be found here(link).