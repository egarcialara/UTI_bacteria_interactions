source("src/visualization/fig3_function.R")
library(ggplot2)

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
# (1 - Glutathione metabolism)
file = paste(index_dir, "Glutathione metabolism.csv",sep="")
fig3a <- plot_vs_growth(file, list_growth$yield$value, 
                                        "Complementarity 3", "Growth (Max OD)", 
                                        "Glutathione metabolism", rows=1)

# (2- Fatty acid metabolism)
file = paste(index_dir, "Fatty acid metabolism.csv",sep="")
fig3b <- plot_vs_growth(file, list_growth$yield$value, 
                                        "Complementarity 3", "Growth (Max OD)", 
                                        "Fatty acid metabolism", rows=1)

file = paste(index_dir, "Arginine biosynthesis.csv",sep="")
fig3c <- plot_vs_growth(file, list_growth$yield$value, 
                                      "Complementarity 3", "Growth (Max OD)", 
                                      "Arginine biosynthesis", rows=1)

file = paste(index_dir, "Histidine metabolism.csv",sep="")
fig3d <- plot_vs_growth(file, list_growth$yield$value, 
                                      "Complementarity 3", "Growth (Max OD)", 
                                      "Histidine metabolism", rows=1)


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
  fig3a + theme(axis.title.x = element_text(colour="white") ,
                plot.title = element_text(hjust = 0.5)),
  fig3b + theme(axis.text.y = element_blank(),
                axis.ticks.y = element_blank(),
                axis.title.y = element_blank() ,
                axis.title.x = element_text(colour="white") ,
                plot.title = element_text(hjust = 0.5)), 
  fig3c + theme(plot.title = element_text(hjust = 0.5)), 
  fig3d+ theme(axis.text.y = element_blank(),
                axis.ticks.y = element_blank(),
                axis.title.y = element_blank() ,
                plot.title = element_text(hjust = 0.5)),
  labels = c("A", "B", "C", "D"),
  scale=c(.9,.9,.9,.9),
  ncol = 2, nrow = 2)

plot_grid(prow, legend, rel_widths = c(4, 1))
# save 
