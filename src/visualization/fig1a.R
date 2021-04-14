# Required packages
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("ComplexHeatmap")
# BiocManager::install("ClassDiscovery")

library(ComplexHeatmap)
library(ClassDiscovery)
library(dplyr)
library(tibble)
library("RColorBrewer")
library(tidyr)
library(stringr)

# Global variables
source_dir = "~/Documents/GitHub/UTI_bacteria_interactions/created/KO_binary_matrices/"
source_files = list.files(source_dir, pattern=".csv$")
saving_dir = "~/Documents/GitHub/UTI_bacteria_interactions/figures/KO_binary/"
saving_format = ".pdf" # if different, change function at the end of the script


pathways_nope <- c("Carbapenem biosynthesis", "Fatty acid elongation", "Penicillin and cephalosporin biosynthesis",
                   "Primary bile acid biosynthesis", "Steroid biosynthesis", "Steroid hormone biosynthesis",
                   "Synthesis and degradation of ketone bodies", "Tetracycline biosynthesis"
)

# ----------------------------------------------------------------------------
# Main function
# Call it at the end of the script
make_KO_binary_plots_colourized <- function(){
  
  # Read files
  for (file in source_files){
    df = read.csv(paste(source_dir,file,sep=""), header=TRUE, row.names=1)
    pathway_name = substr(file, 1, (nchar(file)-4))
    print(pathway_name)
    
    if (pathway_name %in% pathways_nope){
      print("Pass. Error with pathway.")
      next
    }
    
    if (sum(df!=0)==0) {
      print("Pass. No KOs present.")
      next
    }
    
    # df <- df %>% mutate(original_index=2:(n()+1))
    
    # Split groups and make different values for 'KO present' in each
    group1 = df[str_detect(rownames(df), "KECS"), ]
    group2 = df[str_detect(rownames(df), "Ecoli"), ]
    group3 = df[str_detect(rownames(df), "St"), ]
    group4 = df[str_detect(rownames(df), "Ps"), ]
    group5 = df[str_detect(rownames(df), "Ent"),]
    group6 = df[str_detect(rownames(df), "Pm"), ]

    group1[group1==1]="KECS"
    group2[group2==1]="Ecoli"
    group3[group3==1]="St"
    group4[group4==1]="Ps"
    group5[group5==1]="Ent"
    group6[group6==1]="Pm"
    
    
    # Put groups again
    df2 = rbind(group1, group2, group3, group4, group5, group6)
    # df2 <- df2 %>%
      # mutate(grouped_index = 1:n()) %>%
      # arrange(as.integer(original_index)) %>%
      # select(-original_index)
    # order
    hm_order <- ComplexHeatmap::Heatmap(as.matrix(df), cluster_rows=TRUE, cluster_columns = TRUE)
    # ro_1 <- ComplexHeatmap::row_order(hm_order)
    co_1 <- ComplexHeatmap::column_order(hm_order)
    # Order 2
    order <- c()
    n <- 0
    list_groups <- list(group1, group2, group3, group4, group5, group6)
    for(group in list_groups){
      group[group!=0]=1
      hm_temp <- ComplexHeatmap::Heatmap(as.matrix(group%>%select), cluster_rows=TRUE, cluster_columns = TRUE)
      ro_temp <- ComplexHeatmap::row_order(hm_temp)
      order <- c(order, (ro_temp+n))
      n <- n + length(ro_temp)
    }
    
    # Use RColorBrewer color palette names
    col <- c(brewer.pal(n = 7, name = "Dark2"))

    # Heatmap
    df2[df2==0] = NA # to make background of heatmap white :)
    hm_main <- ComplexHeatmap::Heatmap(as.matrix(df2),
            cluster_rows = TRUE, cluster_columns = TRUE,
            column_order = co_1,
            row_order = order, # try put also order by groups
            na_col = "white", # easy way to colour all 0's in white (see line 58)
            col=col,
            name = pathway_name,
            show_row_names = FALSE, show_column_names = FALSE,
            column_title = "KOs", row_title = "Genera",
            column_title_side='bottom',
            width = 5,
            show_heatmap_legend=FALSE
    )
    
    df_names <- data.frame(groups=as.factor(rownames(df2)), order=order) %>%
      arrange(order) %>%
      tidyr::separate(col='groups', into=c('genera', 'extra'))%>%
      select(genera)
    hm_names <- ComplexHeatmap::Heatmap(as.matrix(df_names),
                              cluster_rows=FALSE,
                              show_column_names = FALSE, 
                              col=col[-length(col)],
                              width = 0.125,
                              show_heatmap_legend=FALSE
                              )


    hm <- hm_main + hm_names
    draw(hm, column_title = pathway_name)
    
    # Save
    dir.create(file.path(saving_dir), showWarnings = FALSE)
    pdf(paste(saving_dir, pathway_name, saving_format, sep="")) 
    draw(hm, column_title = pathway_name)
    dev.off() 
  }
}

make_KO_binary_plots_colourized()
