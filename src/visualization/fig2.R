source("src/visualization/fig2_function.R")
source("src/visualization/fig_2d.R")
library(gridExtra)
library(cowplot)
library(ComplexHeatmap)


# Fig 2a - module
source_dir_2a = "~/Documents/GitHub/UTI_bacteria_interactions/src/visualization/util/fig2/temp/complementarity_3/"
file_2a = "Glutathione biosynthesis, gutamate => glutathione.csv"
title_2a = "Glutathione biosynthesis, \n gutamate => glutathione"
results_fig2a <- make_fig2(file_2a, source_dir_2a, title_2a)
h2a <- results_fig2a$hm
funct2a <- results_fig2a$func
#
grid.newpage()
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
draw(h2a)
funct2a()
popViewport()
grab2a <- grid.grab()

# Fig 2b - pathway
source_dir_2b = "~/Documents/GitHub/UTI_bacteria_interactions/created/interaction_matrices/complementarity_3/"
file_2b = "Glutathione metabolism.csv"
title_2b = "\nGlutathione metabolism"
results_fig2b <- make_fig2(file_2b, source_dir_2b, title_2b)
h2b <- results_fig2b$hm
funct2b <- results_fig2b$func
#
grid.newpage()
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
ComplexHeatmap::draw(h2b)
funct2b()
popViewport()
grab2b <- grid.grab()


# Fig 2c - all pathways
source_dir_2c = "~/Documents/GitHub/UTI_bacteria_interactions/src/visualization/util/fig2/temp/complementarity_3/"
file_2c = "all.csv"
title_2c = "\nAll KOs"
results_fig2c <- make_fig2(file_2c, source_dir_2c, title_2c)
h2c <- results_fig2c$hm
funct2c <- results_fig2c$func
#
grid.newpage()
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
draw(h2c)
funct2c()
popViewport()
grab2c <- grid.grab()


# Fig 2d - density plot
growth_dir <- paste(getwd(), "/created/growth/", sep="")
growth_yield_file <- paste(growth_dir, "MaxOD_3.csv", sep="")
index_pathways = paste(getwd(), "/created/interaction_matrices/complementarity_3/", sep="")
index_modules = paste(getwd(), "/src/visualization/util/fig2/temp/complementarity_3/", sep="")
index_all = paste(getwd(), "/src/visualization/util/fig2/temp/complementarity_3/all/", sep="")
h2d <- run_together(growth_dir, growth_yield_file, index_pathways, index_modules, index_all)

h2d <- h2d + theme(
        legend.title=element_text(size=8.5), 
        legend.text=element_text(size=8.5))

h2d<-h2d + theme(plot.margin = margin(2.6,.8,1.4,.8, "cm"))


# All together
# Save 7.9x7
cowplot::plot_grid(
                grab2a,
                grab2b,
                grab2c,
                h2d,
                labels = c("A", "B", "C", "D"),
                scale=c(.9, .9, .9, 1.2),
                align = "hv")

