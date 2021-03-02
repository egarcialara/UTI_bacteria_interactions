#TODO
# check how main.py is called in proper scripts/programs
# check how to import other programs in another folder properly :)
# add imports to requierements
# other?
#############################################################################

# Import packages
import pandas as pd
import subprocess
import os
# Import external scripts
import scatterplot
import SVM_FS
import create_csv_heatmap
import ensemble
import create_bigMatrix


def main():
    ''' Call the different functions '''

    # Create csv and heatplot
    print 'Creating interactions csv file and heatmap'
    create_csv_heatmap.main()

    #Scatter plot
    print 'Creating scatter plot'
    scatterplot.main()

    # Big matrix
    print 'Creating big_matrix'
    create_bigMatrix.main()

    # SVM_FS
    print 'Perform SVM FS'
    SVM_FS.main()

    # In parallel: R boruta, R ttest
    print 'Perform Boruta and statistics test'
    command = 'Rscript'
    path2script1 = 'boruta.R'
    cmd1 = [command, path2script1]
    subprocess.check_output(cmd1, universal_newlines=True)

    path2script2 = 'sttest.R'
    cmd2 = [command, path2script2]
    subprocess.check_output(cmd2, universal_newlines=True)

    # Ensemble at the end
    print 'Perform ensemble of results'
    # raw_input("Press [enter] to continue (when the results from before are finished)")
    ensemble.main()


if __name__=="__main__":
    main()