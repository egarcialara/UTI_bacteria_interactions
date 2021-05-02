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
# (1 - folate biosynthesis)
file = paste(index_dir, "Folate biosynthesis.csv",sep="")
p_compl3_folate_yield <- plot_vs_growth(file, list_growth$yield$value, 
                                        "Complementarity 3", "Growth (Max OD)", 
                                        "", rows=1)

# (2- histidine metabolism)
file = paste(index_dir, "Histidine metabolism.csv",sep="")
p_compl3_hist_yield <- plot_vs_growth(file, list_growth$yield$value, 
                                        "Complementarity 3", "Growth (Max OD)", 
                                        "", rows=1)


# Legend
p_legend <- plot_vs_growth(file, list_growth$rate$value,
                     "", "", "", legend=TRUE, rows=1)

## PUT IT ALL TOGETHER
legend <- get_legend(
  # create some space to the left of the legend
  p_legend + theme(legend.box.margin = margin(0, 0, 0, 12))
)


prow <- plot_grid(p_compl3_folate_yield + theme(axis.text.x = element_blank(),
                                                 axis.ticks.x = element_blank(),
                                                 axis.title.x = element_blank() ),
                  p_compl3_hist_yield + theme(axis.text.y = element_blank(),
                                                 axis.ticks.y = element_blank(),
                                                 axis.title.y = element_blank() ,
                                                axis.text.x = element_blank(),
                                                axis.ticks.x = element_blank(),
                                                axis.title.x = element_blank() ), 
                  p_compl3_folate_yield, 
                  p_compl3_folate_yield+ theme(axis.text.y = element_blank(),
                                               axis.ticks.y = element_blank(),
                                               axis.title.y = element_blank() ),
                  labels = c("A", "B", "C", "D", "E", "F", "G", "H"),
                  ncol = 2, nrow = 2)
plot_grid(prow, legend, rel_widths = c(3, 1))
