from load_data.load_KOs_data import create_KOs_binary_matrix
from load_data.load_growth_data import mat_to_pandas
from interactions.interaction_matrices import create_interaction_matrices
from pathway_selection.create_big_matrix import big_matrix_create
from pathway_selection.pathway_selection import call_selections


def main():
    ''' Call the different functions '''

    # Load data
    print("--------------------------------------")
    print("(1/5) Creating KO binary matrices  ...", "\n")
    create_KOs_binary_matrix()
    print("--------------------------------------")
    print("(2/5) Reding the growth data       ...", "\n")
    mat_to_pandas()

    # Interaction tables
    print("--------------------------------------")
    print("(3/5) Creating interaction matrices...", "\n")
    create_interaction_matrices()

    # Pathway selection
    print("--------------------------------------")
    print("(4/5) Pathway selection tables     ...", "\n")
    big_matrix_create()
    print("(5/5) Pathway selection            ...", "\n")
    call_selections()


if __name__=="__main__":
    main()
