source("src/visualization/fig3_function.R")
library(ggplot2)

# Global variables
index_dir = paste(getwd(), "/created/interaction_matrices/complementarity_3/", sep="")
growth_dir <- paste(getwd(), "/created/growth/", sep="")
growth_rate_file <- paste(growth_dir, "GR_3.csv", sep="")
growth_yield_file <- paste(growth_dir, "MaxOD_3.csv", sep="")
col <- c(RColorBrewer::brewer.pal(n = 6, name = "Dark2"))
col = col[c(6,1,5,4,3,2)]

# Growth
list_growth <- get_growth_arrays()

# Indeces
# (1 - Glutathione metabolism)
file = paste(index_dir, "Glutathione metabolism.csv",sep="")
p1 <- plot_vs_growth(file, list_growth$yield$value, 
                                        "Complementarity 3", "Growth yield", 
                                        "Glutathione metabolism", rows=1)

# (2- Fatty acid metabolism)
file = paste(index_dir, "Tyrosine metabolism.csv",sep="")
p2 <- plot_vs_growth(file, list_growth$yield$value, 
                                        "Complementarity 3", "Growth yield", 
                                        "Tyrosine metabolism", rows=1)

file = paste(index_dir, "Folate biosynthesis.csv",sep="")
p3 <- plot_vs_growth(file, list_growth$yield$value, 
                                      "Complementarity 3", "Growth yield", 
                                      "Histidine metabolism", rows=1)

file = paste(index_dir, "D-Alanine metabolism.csv",sep="")
p4 <- plot_vs_growth(file, list_growth$yield$value, 
                                      "Complementarity 3", "Growth yield", 
                                      "D-Alanine metabolism", rows=1)


# Legend
p_legend <- plot_vs_growth(file, list_growth$rate$value,
                     "", "", "", legend=TRUE, rows=1)+
  geom_point(shape=15, size=3)+
  guides(shape = guide_legend(override.aes = list(size = 2)))

## PUT IT ALL TOGETHER
legend <- get_legend(
  # create some space to the left of the legend
  p_legend + theme(legend.box.margin = margin(-5, 0, 0, 12),
                   legend.direction='vertical',
                   legend.box='vertical')
)


# 9x7 *0.8 = 7.2x5.6
prow <- plot_grid(
  p1 + theme(
      axis.title.x = element_blank() ,
      plot.title = element_text(hjust = 0.5)),
  p2 + theme(
      axis.text.y = element_blank(),
      axis.ticks.y = element_blank(),
      axis.title.y = element_blank() ,
      axis.title.x = element_blank() ,
      plot.title = element_text(hjust = 0.5)),
  p3 + theme(plot.title = element_text(hjust = 0.5)),
  p4+ theme(
      axis.text.y = element_blank(),
      axis.ticks.y = element_blank(),
      axis.title.y = element_blank() ,
  plot.title = element_text(hjust = 0.5)),
  labels = c("A", "B", "C", "D"),
  ncol = 2, nrow = 2)

plot_grid(prow, legend, rel_widths = c(3, 1))
