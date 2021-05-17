from load_data.load_KOs_data import create_KOs_binary_matrix
from load_data.load_growth_data import mat_to_pandas
from interactions.interaction_matrices import create_interaction_matrices
from pathway_selection.create_big_matrix import big_matrix_create
from pathway_selection.pathway_selection import call_selections


def main():
    ''' Call the different functions '''

    # Load data
    print("--------------------------------")
    print("Creating KO binary matrices  ...", "\n")
    create_KOs_binary_matrix()
    mat_to_pandas()

    # Interaction tables
    print("--------------------------------")
    print("Creating interaction matrices...", "\n")
    create_interaction_matrices()

    # Pathway selection
    print("--------------------------------")
    print("Pathway selection            ...", "\n")
    big_matrix_create()
    call_selections()


if __name__=="__main__":
    main()
