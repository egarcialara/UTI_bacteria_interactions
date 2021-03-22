## NEEDS filling
## ????
## split complementarity and competition in 2 files -or more-
# import pandas as pd
# import glob
# import math
# import numpy as np


from interactions.each_interaction.complementarity_1 import create_complementarity_1
from interactions.each_interaction.complementarity_2 import create_complementarity_2
from interactions.each_interaction.complementarity_3 import create_complementarity_3
from interactions.each_interaction.complementarity_4 import create_complementarity_4

from interactions.each_interaction.similarity_1 import create_similarity_1
from interactions.each_interaction.similarity_2 import create_similarity_2




# files_dir = "../../created/KO_binary_matrices"
# files_binary = glob.glob(files_dir+"/*.csv")


def create_interaction_matrices():

    # Complementarities
    create_complementarity_1()
    create_complementarity_2()
    create_complementarity_3()
    create_complementarity_4()

    # Similarities
    create_similarity_1()
    create_similarity_2()