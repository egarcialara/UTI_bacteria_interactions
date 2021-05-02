source("src/visualization/fig2_function.R")
library(gridExtra)
library(cowplot)


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
title_2b = "Glutathione metabolism \n"
results_fig2b <- make_fig2(file_2b, source_dir_2b, title_2b)
h2b <- results_fig2b$hm
funct2b <- results_fig2b$func
#
grid.newpage()
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
draw(h2b)
funct2b()
popViewport()
grab2b <- grid.grab()


# Fig 2c - all pathways
source_dir_2c = "~/Documents/GitHub/UTI_bacteria_interactions/src/visualization/util/fig2/temp/complementarity_3/"
file_2c = "all.csv"
title_2c = "All KOs \n"
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


# Fig 2d - pathway 2: Folate biosynthesis
source_dir_2d = "~/Documents/GitHub/UTI_bacteria_interactions/created/interaction_matrices/complementarity_3/"
file_2d = "Folate biosynthesis.csv"
title_2d = "Folate biosynthesis  \n"
results_fig2d <- make_fig2(file_2d, source_dir_2d, title_2d)
h2d <- results_fig2d$hm
funct2d <- results_fig2d$func
#
grid.newpage()
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
draw(h2d)
funct2d()
popViewport()
grab2d <- grid.grab()


# All together
# Save 9x8
cowplot::plot_grid(
                grab2a,
                grab2b,
                grab2c,
                grab2d,
                labels = c("A", "B", "C", "D"),
                scale=c(.85, .85, .85, .85),
                align = "hv")

