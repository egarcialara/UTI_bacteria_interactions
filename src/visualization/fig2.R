# Required packages
# if (!requireNamespace("BiocManager", quietly = TRUE))
#   install.packages("BiocManager")
# BiocManager::install("ComplexHeatmap")
# BiocManager::install("ClassDiscovery")

# library(ClassDiscovery)
library(dplyr)
library(RColorBrewer)
library(tidyr)
library(stringr)
library(ComplexHeatmap)
library(circlize)


# Main function
make_KO_binary_plots_colourized <- function(file, source_dir){
  
  source_files = list.files(source_dir, pattern=".csv$")
  
  
  df = read.csv(paste(source_dir,file,sep=""), header=TRUE, row.names=1)
  pathway_name = substr(file, 1, (nchar(file)-4))
  print(pathway_name)
  
  # get rows in order of ent/st/... so that
  # when ordering by number, they get in proper order
  df2 <- df %>%
    mutate(rows = rownames(df)) %>%
    mutate(order = ifelse(startsWith(rows,"Ent"), 1,
                    ifelse(startsWith(rows,"St"), 2,
                      ifelse(startsWith(rows, "Ps"), 3,
                        ifelse(startsWith(rows, "Pm"), 4,
                          ifelse(startsWith(rows, "KECS"), 5,
                                 6)))))) %>%       # Ecoli
    arrange(., order) %>%
    select(-c(rows,order)) %>%
    relocate(rownames(.))
  
  list_groups <- c("Ent", "St", "Ps", "Pm", "KECS", "Ecoli")
  
  # split per acceptor group
  order_cols = list()
  order_rows = c()
  n_rows_counted = 0
  names_for_rows <- c()
  for(group in list_groups){
    df_group = df2 %>% select(starts_with(group))
    hm_group <- ComplexHeatmap::Heatmap(as.matrix(df_group), 
                                        cluster_rows = TRUE, cluster_columns = TRUE)
    # a) get col order
    order_cols[group] = list(column_order(hm_group))
    # b) get row order
    order_rows <- c(order_rows, 
                    (column_order(hm_group) + n_rows_counted))
    n_rows_counted <- n_rows_counted + length(column_order(hm_group))
    # accumulate names
    names <- c(rep("", as.integer(ncol(df_group)/3)-2),
               group,
               rep("", (ncol(df_group) - as.integer(ncol(df_group)/3))+1))
    names_for_rows <- c(names_for_rows, names)
  }
  
  
  # draw actual heatmaps per acceptor group
  col_list = c(brewer.pal(n = 7, name = "Dark2"))
  i=1
  list_heatmaps = list()
  for(group in list_groups){
    col <- colorRamp2(c(0,max(df)), c("white", col_list[[i]]))
    i <- i+1
    
    df_group = df2 %>% select(starts_with(group))
    # rownames(df_group) <- names_for_rows
    hm_group <- ComplexHeatmap::Heatmap(as.matrix(df_group), 
                                        cluster_rows=FALSE, cluster_columns=FALSE, 
                                        column_order= unlist(order_cols[group]),
                                        row_order = rev(order_rows),
                                        name=group,
                                        col=col,
                                        column_title=group,  column_title_side = "bottom",
                                        show_column_names = FALSE,
                                        show_row_names=FALSE)
                                        # row_labels = names_for_rows,
                                        # row_names_rot=270)
    list_heatmaps[group] <- hm_group
  }
  
  df_donors <- df2 %>%
    mutate(rows = rownames(df2)) %>%
    mutate(donors = ifelse(startsWith(rows,"Ent"), "Ent",
                          ifelse(startsWith(rows,"St"), "St",
                                 ifelse(startsWith(rows, "Ps"), "Ps",
                                        ifelse(startsWith(rows, "Pm"), "Pm",
                                               ifelse(startsWith(rows, "KECS"), "KECS",
                                                      "Ecoli"))))))%>%       # Ecoli
    select(donors) 

    hm_donors <- ComplexHeatmap::Heatmap(
        as.matrix(df_donors),
        cluster_rows=FALSE, cluster_columns=FALSE,
        row_order = rev(order_rows),
        width = 1, 
        col=col_list[c(6, 1, 5, 4, 3, 2)],
        show_heatmap_legend = FALSE,
        show_column_names=FALSE,
        row_labels = names_for_rows,
        # row_names_rot=270,
        row_title_side = "right")

  # merge heatmaps
  hm <- list_heatmaps$Ent + list_heatmaps$St + 
        list_heatmaps$Ps + list_heatmaps$Pm + 
        list_heatmaps$KECS + list_heatmaps$Ecoli + hm_donors

  
  return(hm)
    
  }

# Global variables
source_dir_1 = "~/Documents/GitHub/UTI_bacteria_interactions/created/interaction_matrices/complementarity_3/"
file_1 = "Glutathione metabolism.csv"
source_dir_2 = "~/Documents/GitHub/UTI_bacteria_interactions/src/visualization/temp/complementarity_3/"
file_all = "all.csv"
file_module = "Glutathone biosynthesis, gutamate => glutathione.csv"

# Saving
saving_dir = "~/Documents/GitHub/UTI_bacteria_interactions/figures/interaction_matrices/"
saving_format = ".pdf"


hm1 <- make_KO_binary_plots_colourized(file_1, source_dir_1)
hm2 <- make_KO_binary_plots_colourized(file_all, source_dir_2)
hm3 <- make_KO_binary_plots_colourized(file_module, source_dir_2)


i=1
list_legends = list()
for(group in list_groups){
  col <- colorRamp2(c(0,max(df)), c("white", col_list[[i]]))
  i <- i+1
  list_legends[group] = Legend(col_fun=col, title=group)
}



# Save (part1)
# pdf(paste(saving_dir,"glutathionmetabolism", saving_format, sep=""))
png(paste(saving_dir,"glutathionmetabolism", ".png", sep=""))

grid.newpage()
pushViewport(viewport(layout = grid.layout(nr = 2, nc = 2)))
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
draw(hm2, ht_gap = unit(c(0,0,0,0,0,1), "cm"),
     column_title = substr(file_module, 1, (nchar(file_module)-4)),
     # row_title =  "Donor", row_title_side = "right", 
     show_heatmap_legend = FALSE, newpage = FALSE)
upViewport()

pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 2))
draw(hm1, ht_gap = unit(c(0,0,0,0,0,1), "cm"),
     column_title = substr(file_1, 1, (nchar(file_1)-4)),
     # heatmap_legend_side = "bottom",
     row_title =  "Donor", row_title_side = "right",
     show_heatmap_legend = FALSE, newpage = FALSE)
upViewport()

pushViewport(viewport(layout.pos.row = 2, layout.pos.col = 1))
draw(hm3, ht_gap = unit(c(0,0,0,0,0,1), "cm"),
     column_title = substr(file_all, 1, (nchar(file_all)-4)),
     row_title =  "Donor", row_title_side = "right", 
     show_heatmap_legend = FALSE, newpage = FALSE)
upViewport()


pd = packLegend(list=list_legends, direction = "horizontal",
                max_width = unit(5, "cm"),
                column_gap = unit(4, "mm"),
                row_gap=unit(1,"mm"))

pushViewport(viewport(layout.pos.row = 2, layout.pos.col = 2))
grid.draw(pd)
upViewport()

upViewport()

# Save (part 2)
dev.off()
