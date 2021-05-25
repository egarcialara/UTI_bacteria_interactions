from pathway_selection.pw_selection_scripts.SVM_selection import call_SVM
from pathway_selection.pw_selection_scripts.Boruta_selection import call_Boruta
from pathway_selection.pw_selection_scripts.WMW_selection import call_WMW
from pathway_selection.pw_selection_scripts.ensemble_selection import call_ensemble


def call_selections():
    # call_SVM()
    # call_Boruta()
    call_WMW()
    # call_ensemble()  # requires running the three above
