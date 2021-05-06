from fig2_create_KO_files import create_KOs_binary_matrix_module, create_KOs_binary_matrix_all
from interaction_matrices import create_interaction_matrices

def main():
    ''' Call the different functions '''

    # Load data
    print("--------------------------------")
    print("Creating KO binary matrices  ...", "\n")
    create_KOs_binary_matrix_module()
    create_KOs_binary_matrix_all()

    # Interaction tables
    print("--------------------------------")
    print("Creating interaction matrices...", "\n")
    create_interaction_matrices()
 
 
if __name__=="__main__":
    main()
