from pathway_selection.pw_selection_scripts.SVM_selection import call_SVM
from pathway_selection.pw_selection_scripts.Boruta_selection import call_Boruta
from pathway_selection.pw_selection_scripts.WMW_selection import call_WMW
from pathway_selection.pw_selection_scripts.ensemble_selection import call_ensemble


def call_selections():
    print(1)
    call_SVM()
    # exit()
    print(2)
    call_Boruta()
    print(3)
    call_WMW()
    print(4)
    # call_ensemble()
