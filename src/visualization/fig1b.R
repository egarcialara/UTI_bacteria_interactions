# x-axis: annotation ratio
# y-axis: absolute genes
# Group in the 6 grups. Add sd for both axis.
# same legend as heatmap Fig.1a

# libraries
library(ggplot2)
library(RColorBrewer)

# directories
source_dir = ""


# group

mock_annotations_perc <- c(45, 23, 56, 45, 34, 56)
mock_genes_absolute <- c(234, 645, 234, 345, 237, 532)

sd_annotations_perc <- c(34, 23, 45, 65, 23, 54)/10
sd_genes_absolute <- c(35, 54, 43, 76, 34, 62)/10

df <- data.frame("x" = mock_annotations_perc, "y" = mock_genes_absolute,
                 "groups" = c("KECS", "Ecoli", "St", "Ps", "Ent", "Pm"))

col <- c(RColorBrewer::brewer.pal(n = 7, name = "Dark2"))[-7]

# plot
ggplot(df)+
  geom_errorbar(aes(x=x, y=y, ymin=y-sd_annotations_perc/2, ymax=y+sd_annotations_perc/2,
                    ), colour="blue", width=1)+
  geom_errorbar(aes(x=x, y=y, 
                    xmin=x-sd_genes_absolute, xmax=x+sd_genes_absolute
  ), colour="red", width=2)+
  geom_point(aes(x, y, colour=groups), size=3)+
  theme_classic()+
  labs(x="Annotation ratio", y="Absolute number of genes")+
  scale_fill_manual(values=col)+
  theme(legend.position = "none") 
  
plot(x=mock_annotations_perc, y=mock_genes_absolute)
