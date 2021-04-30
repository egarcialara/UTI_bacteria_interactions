source("src/visualization/fig3_function.R")

# Global variables
index_dir = paste(getwd(), "/created/interaction_matrices/complementarity_3/", sep="")
other_dir = paste(getwd(), "/src/visualization/util/fig3/other_indeces/", sep="")
growth_dir <- paste(getwd(), "/created/growth/", sep="")
growth_rate_file <- paste(growth_dir, "GR_3.csv", sep="")
growth_yield_file <- paste(growth_dir, "MaxOD_3.csv", sep="")
col <- c(RColorBrewer::brewer.pal(n = 7, name = "Dark2"))

# Growth
list_growth <- get_growth_arrays()

# Indeces
# source_files = list.files(source_dir, pattern=".csv$")
file = paste(index_dir, "Folate biosynthesis.csv",sep="")
p_compl3_folate_yield <- plot_vs_growth(file, list_growth$yield$value, 
                                        "Complementarity 3", "Growth (Max OD)", 
                                        "",
                                        1)
p_compl3_folate_rate <- plot_vs_growth(file, list_growth$rate$value, 
                                       "Complementarity 3", "Growth (GR)", 
                                       "",
                                       1)

# RevEcoR Complementarity
file = paste(other_dir, "revecor_compl_csv.csv",sep="")
p_Rev_compl_yield <- plot_vs_growth(file, list_growth$yield$value,
                                    "Complementarity index", "Growth (Max OD)", 
                                    "RevEcoR")
p_Rev_compl_rate <- plot_vs_growth(file, list_growth$rate$value,
                                   "Complementarity index", "Growth (GR)", 
                                   "RevEcoR")

# RevEcoR Competition
file = paste(other_dir, "revecor_compet_csv.csv",sep="")
p_Rev_compet_yield <- plot_vs_growth(file, list_growth$yield$value,
                                     "Competition index", "Growth (Max OD)", 
                                     "RevEcoR")
p_Rev_compet_rate <- plot_vs_growth(file, list_growth$rate$value,
                                    "Competition index", "Growth (GR)", 
                                    "RevEcoR")


# NetCooperate BSS
file = paste(other_dir, "df_BSS_2.csv",sep="")
p_BSS_yield <- plot_vs_growth(file, list_growth$yield$value,
                              "NetCooperate BSS", "Growth (Max OD)", 
                              "NetCooperate")
p_BSS_rate <- plot_vs_growth(file, list_growth$rate$value,
                             "NetCooperate BSS", "Growth (GR)", 
                             "NetCooperate")



## PUT IT ALL TOGETHER
plot_grid(p_Rev_compl_rate, p_Rev_compet_rate, p_BSS_rate, p_compl3_folate_rate,
          p_Rev_compl_yield, p_Rev_compet_yield, p_BSS_yield, p_compl3_folate_yield,
          labels = c("A", "B", "C", "D", "E", "F", "G", "H"),
          ncol = 4, nrow = 2)
