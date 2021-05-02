library(dplyr)
library(RColorBrewer)
library(tidyr)
library(stringr)
library(ComplexHeatmap)
library(circlize)



make_fig2 <- function(file, source_dir, title){
  
  # Data
  df = read.csv(paste(source_dir,file,sep=""), header=TRUE, row.names=1)

  # Colour
  col_fun = colorRamp2(c(min(df), max(df)), c("white", "black"))
  
  # Groups 
  df2 <- df %>%
    mutate(labels = rownames(df)) %>%
    separate(labels, c("Name"), sep="[.]", remove=TRUE, extra="drop")

  # Order
  h_order <- Heatmap(as.matrix(df), 
                     row_split = df2$Name,
                     column_split = df2$Name)
  order_rows <- row_order(h_order)
  list_order_rows = c()
  for(group in c("Ent", "St", "Ps", "Pm", "KECS", "Ecoli")){
    list_order_rows = c(list_order_rows, unlist(order_rows[group]))
  }
  
  # Annotations
  # (rows)
  text_list = list(
    text1 = "Ecoli", text2="KECS", text3="Pm",
    text4="Ps", text5="St", text6="Ent")
  ha = rowAnnotation(
    foo = anno_empty(border = FALSE, 
                     width = max_text_width(unlist(text_list)) + unit(3, "mm")))
  
  # (columns)
  text_list_2 = list(
    text1 = "Ent", text2="St", text3="Ps",
    text4="Pm", text5="KECS", text6="Ecoli")
  ha2 = columnAnnotation(
    foo2 = anno_empty(border = FALSE, 
                     width = max_text_width(unlist(text_list_2)) + unit(3, "mm"))) 
  
  # Plot
  hh <- Heatmap(as.matrix(df),
          row_split = factor(df2$Name, levels = rev(c("Ent", "St", "Ps", "Pm", "KECS", "Ecoli"))),
          column_split = factor(df2$Name, levels = c("Ent", "St", "Ps", "Pm", "KECS", "Ecoli")),
          row_gap = unit(0,"mm"), column_gap=unit(0,"mm"),
          right_annotation = ha,
          bottom_annotation = ha2,
          col=col_fun,
          row_order = rev(list_order_rows),
          column_order = list_order_rows,
          show_row_names = FALSE, show_column_names = FALSE,
          show_row_dend = FALSE, show_column_dend = FALSE,
          column_title = title, row_title=NULL,
          show_heatmap_legend=FALSE,
          column_title_gp = gpar(fontsize = 11)
          )
  
  # Annotations of groups
  add_annotations_fig2 <- function(){
    col2 <- c(brewer.pal(n = 6, name = "Dark2")) # remove white
    col2 = col2[c(6,1,5,4,3,2)]
    col3 = rev(col2)
    for(i in 1:6) {
      # (rows)
      decorate_annotation("foo", slice = i, {
        grid.rect(x = 0, width = unit(1.5, "mm"), 
                  gp = gpar(fill = col2[i], col = NA),
                  just = "left")
        grid.text(paste(text_list[[i]], collapse = "\n"), 
                  x = unit(2, "mm"), just = "left",
                  gp=gpar(fontsize=9))
      })
      # (columns)
      decorate_annotation("foo2", slice = i, {
        grid.rect(x = 0, y=1, height = unit(1.5, "mm"), 
                  gp = gpar(fill = col3[i], col = NA),
                  just = "left")
        grid.text(paste(text_list_2[[i]]), 
                  y = unit(5, "mm"), just = "centre",
                  gp=gpar(fontsize=9))
      })
      }
  }
  
    # Plot + add annotations in the plot  
    hhh <- draw(hh, row_title="Donor", column_title = "Acceptor",
         column_title_side="bottom", row_title_side="right",
         column_title_gp = gpar(fontsize = 10),
         row_title_gp = gpar(fontsize = 10))

    return_list = list(hm = hhh, func=add_annotations_fig2)
    return(return_list)
}
  
# # To run  
# source_dir = "~/Documents/GitHub/UTI_bacteria_interactions/created/interaction_matrices/complementarity_3/"
# file = "Glutathione metabolism.csv"
# results_fig2 <- make_fig2(file, source_dir)
# h1 <- results_fig2$hm
# h1 <- grid.grabExpr(draw(h1))
# funct <- results_fig2$func
# funct()



