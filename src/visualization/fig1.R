source("src/visualization/fig1a.R")
source("src/visualization/fig1b.R")
source("src/visualization/fig1c.R")
library(gridExtra)
library(cowplot)

# Fig1a
file_1a = "Glycolysis - Gluconeogenesis.csv"
source_1a = "~/Documents/GitHub/UTI_bacteria_interactions/created/KO_binary_matrices/"
hm_1a <- make_KO_binary_plots_colourized(file_1a, source_1a)
fig1a <-  grid.grabExpr(draw(hm_1a)) 

# Fig1b
dir_1b = paste(getwd(), "/extra/excel_UTI_strains/", sep="")
file_1b <- paste(dir_1b, "List_bacteria_UTI.xls", sep="")
fig_1b <- make_fig1b(file_1b, legend=FALSE)
# lgd_1b <- cowplot::get_legend(make_fig1b(file_1b, legend=TRUE))



# Fig1c
index_dir = paste(getwd(), "/created/interaction_matrices/complementarity_3/", sep="")
growth_dir <- paste(getwd(), "/created/growth/", sep="")
growth_rate_file <- paste(growth_dir, "GR_3.csv", sep="")
growth_yield_file <- paste(growth_dir, "MaxOD_3.csv", sep="")
fig_1c <- make_fig1c(growth_rate_file, growth_yield_file, legend=FALSE)
# lgd_1c <- cowplot::get_legend(make_fig1c(growth_rate_file, growth_yield_file, legend=TRUE))

# Legend
# lgd1 = Legend(labels = c("Ent", "St", "Ps", "Pm", "KECS", "Ecoli"),
#              legend_gp = gpar(fill=c(brewer.pal(n = 6, name = "Dark2"))),#, 
#              title = "Group")#, ncol = 3)
# lgd1 <- grid.grabExpr(draw(lgd1)) 
df_lgd <- data.frame(
  Group = c("Ent", "St", "Ps", "Pm", "KECS", "Ecoli"),
  Gram = c("Gram +", "Gram +", "Gram -", "Gram -", "Gram -", "Gram -"),
  pval = c(0,0.2,0.2,0.1,0.3,0.1) #random
)

col <- c(RColorBrewer::brewer.pal(n = 6, name = "Dark2"))
col = col[c(6,1,5,4,3,2)] # same order Ent, St, Ps, Pm, KECS, Ecoli
plot_lgd <- df_lgd %>% ggplot()+
  geom_point(aes(x=Group, y=Gram,
             colour=Group,
             shape=Gram,
             fill= pval))+
  scale_fill_gradientn(colours=c("blue", "red"), breaks=c(0.05, 0.25,0.50,0.75),
              limits=c(0.05,max(df_plot$pval)), oob = scales::censor, na.value="darkblue")+
  scale_colour_manual(values=col)+
  theme_minimal()+theme(legend.box='horizontal')
lgd <- cowplot::get_legend(plot_lgd)

  # df_plot %>%
  # ggplot()+
  # geom_point(aes(x=values_rate, y=values_yield, colour=pval))+
  # geom_abline(colour="gray", linetype = "dashed")+
  # lims(x=c(-0.7, 0.7), y=c(-0.7, 0.7))+
  scale_colour_gradientn(colours=c("blue", "red"), breaks=c(0.05, 0.25,0.50,0.75),
                         limits=c(0.05,max(df_plot$pval)), oob = scales::censor, na.value="darkblue")


# All together

# Saving
saving_dir = "~/Documents/GitHub/UTI_bacteria_interactions/figures/"
saving_format = ".pdf"
# pdf(paste(saving_dir,"fig1", saving_format, sep=""))
png(paste(saving_dir,"fig1", ".png", sep=""))

plot_grid(fig1a,fig_1b,fig_1c, lgd,
          labels = c("A", "B", "C", NA))

# Save (part 2)
dev.off()
