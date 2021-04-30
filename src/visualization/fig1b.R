# x-axis: annotation ratio
# y-axis: absolute genes
# Group in the 6 grups. Add sd for both axis.
# same legend as heatmap Fig.1a

# libraries
library(ggplot2)
library(RColorBrewer)
library(readxl)
library(dplyr)
library(tidyverse)


# Get data
source_dir = paste(getwd(), "/extra/excel_UTI_strains/", sep="")
source_file <- paste(source_dir, "List_bacteria_UTI.xls", sep="")
saving_dir <- "~/Documents/GitHub/UTI_bacteria_interactions/figures/exploratory/"
saving_file <- paste(saving_dir, "genes_vs_KO_annotations", sep="")
saving_format = ".pdf"


df_gram <- data.frame(
  Group = c("Ecoli", "Ent", "KECS", "Pm", "Ps", "St"),
  Gram = c("Gram -", "Gram +", "Gram -", "Gram -", "Gram -", "Gram +")
)

make_fig1b <- function(source_file, legend){
  df <- read_excel(source_file,
                   range=cell_cols(c("C", "K", "L")),
                   col_names = TRUE) %>%
    select(Group, "# entries annotated by KO terms", "% entries annotated by KO terms") %>%
    rename(
      n_annotations = `# entries annotated by KO terms`,
      perc_annotations = `% entries annotated by KO terms`
    )
  
  # Group values (mean and st. dev)
  df_summary <- df %>%
    drop_na(n_annotations) %>%
    dplyr::group_by(Group) %>%
    dplyr::summarize(
      perc_annotations_mean = mean(perc_annotations),
      perc_annotations_sd = sd(perc_annotations),
      n_genes_mean = mean(n_annotations),
      n_genes_sd = sd(n_annotations)
    ) %>%
    filter(Group!="MM") %>%
    left_join(df_gram, by="Group") #%>%
    # mutate(order = c(6,1,5,4,3,2)) %>% arrange(order) %>% select(-order)
    
  
  
  # Plot (part 1)
  col <- c(RColorBrewer::brewer.pal(n = 6, name = "Dark2"))
  col = col[c(6,1,5,4,3,2)] # same order Ent, St, Ps, Pm, KECS, Ecoli
  
  # Save (part1)
  dir.create(file.path(saving_dir), showWarnings = FALSE)
  # pdf(paste(saving_file, saving_format, sep=""))
  
  
  # Plot (part 2)
  if(legend==FALSE){
      fig_decoration <- theme(legend.position = "none")
    }else{
      fig_decoration <- theme(legend.box='horizontal')
    }
  
  fig1b <- ggplot(df_summary)+
    geom_errorbar(aes(x=perc_annotations_mean, 
                      y=n_genes_mean,
                      ymin=n_genes_mean-n_genes_sd,
                      ymax=n_genes_mean+n_genes_sd,
                      colour=Group
    ), width=1)+
    geom_errorbarh(aes(x=perc_annotations_mean, y=n_genes_mean,
                       xmin=perc_annotations_mean-perc_annotations_sd,
                       xmax=perc_annotations_mean+perc_annotations_sd,
                       colour=Group
    ), width=1)+
    geom_point(aes(x=perc_annotations_mean, y=n_genes_mean,
                   colour=Group, shape=Gram), size=3)+
    theme_minimal()+
    labs(x="Annotation ratio", y="Absolute number of genes")+
    scale_colour_manual(values=col)+
    lims(x=c(0,100)) + expand_limits(y=0)+
    fig_decoration
  
  return(fig1b)
  # Save (part 2)
  # dev.off()
}
