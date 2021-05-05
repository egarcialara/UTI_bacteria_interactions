source("src/visualization/fig1a.R")
source("src/visualization/fig1b.R")
source("src/visualization/fig1c.R")
library(gridExtra)
library(cowplot)
library(tidyverse)
library(ggplot2)

# Fig1a
file_1a = "all.csv"
source_1a = "~/Documents/GitHub/UTI_bacteria_interactions/src/visualization/util/fig2/temp/KO_binary_matrices/"
return_1a <- make_KO_binary_plots_colourized(file_1a, source_1a)
hm_1a <- return_1a$hh
func_1a <- return_1a$function_add_annotations
# fig_1a <-  grid.grabExpr(draw(hm_1a))
#
grid.newpage()
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
draw(hm_1a)
func_1a()
popViewport()
grab1a <- grid.grab()


# Fig1b
dir_1b = paste(getwd(), "/extra/excel_UTI_strains/", sep="")
file_1b <- paste(dir_1b, "List_bacteria_UTI.xls", sep="")
fig_1b <- make_fig1b(file_1b, legend=FALSE)


# Fig1c
index_dir = paste(getwd(), "/created/interaction_matrices/complementarity_3/", sep="")
growth_dir <- paste(getwd(), "/created/growth/", sep="")
growth_rate_file <- paste(growth_dir, "GR_3.csv", sep="")
growth_yield_file <- paste(growth_dir, "MaxOD_3.csv", sep="")
list_1c <- make_fig1c(growth_rate_file, growth_yield_file, legend=FALSE)
fig_1c <- list_1c$plot


# Legend
df_lgd <- data.frame(
  Group = rep(c("Ent", "St", "Ps", "Pm", "KECS", "Ecoli"),9),
  Category = rep(c("Gram +", "Gram +", "Gram -", "Gram -", "Gram -", "Gram -"),9),
  pval = rep(c(0,0.2,0.2,0.1,0.3,0.1),9) #random
)

col <- c(RColorBrewer::brewer.pal(n = 6, name = "Dark2"))
col = col[c(6,1,5,4,3,2)] # same order Ent, St, Ps, Pm, KECS, Ecoli
plot_lgd <- df_lgd %>% ggplot()+
  geom_point(aes(x=Group, y=Category,
             colour=Group),
              shape=15, size=6)+
  geom_point(aes(x=Group, y=Category,
             shape=Category,
             fill= pval), size=3)+
  scale_fill_gradientn(colours=c("blue", "red"), breaks=c(0.05, 0.25,0.50,0.75),
              limits=c(0.05,max(list_1c$df_plot$pval)), 
              oob = scales::censor, na.value="darkblue")+
  scale_colour_manual(values=col)+
  theme_minimal()+
  theme(legend.box='horizontal',legend.position="right")+
  guides(colour = guide_legend(title.position="top", title.hjust = 0, order=1),
         fill = guide_colourbar(title.position="top",
                                title.hjust = 0, order=3, title="p-value"),
         shape = guide_legend(title.position="top", title.hjust = 0, order=2))

lgd <- cowplot::get_legend(plot_lgd)


# All together
# Saving
# Save 9x7 (inches, portrait) X0.7 = 630x490
saving_dir = "~/Documents/GitHub/UTI_bacteria_interactions/figures/"
saving_format = ".pdf"
# pdf(paste(saving_dir,"fig1", saving_format, sep=""))
# png(paste(saving_dir,"fig1", ".png", sep=""))
cowplot::plot_grid(grab1a, fig1b, fig_1c, lgd,
          labels = c("A", "B", "C", NA),
          scale=c(0.9, 0.8, 0.9, 0.5), # not
          align = "v")
# func_1a() # - if you want annotations, please modify fig1a script too!

# Save (part 2)
# dev.off()
