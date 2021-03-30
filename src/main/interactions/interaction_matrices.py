from interactions.each_interaction.complementarity_1 import create_complementarity_1
from interactions.each_interaction.complementarity_2 import create_complementarity_2
from interactions.each_interaction.complementarity_3 import create_complementarity_3
from interactions.each_interaction.complementarity_4 import create_complementarity_4

from interactions.each_interaction.similarity_1 import create_similarity_1
from interactions.each_interaction.similarity_2 import create_similarity_2

def create_interaction_matrices():

    # Complementarities
    create_complementarity_1()
    create_complementarity_2()
    create_complementarity_3()
    create_complementarity_4()

    # Similarities
    create_similarity_1()
    create_similarity_2()