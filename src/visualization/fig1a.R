library(ComplexHeatmap)
library(dplyr)
library(RColorBrewer)
library(tidyr)

make_KO_binary_plots_colourized <- function(file, source_dir){
  
  # Data
  df = read.csv(paste(source_dir,file,sep=""), header=TRUE, row.names=1)
  pathway_name = substr(file, 1, (nchar(file)-4))
  
  
  # Groups 
  df2 <- df %>%
    mutate(labels = rownames(df)) %>%
    separate(labels, c("Name"), sep="[.]", remove=TRUE, extra="drop")
  
  
  # Order
  h_order <- Heatmap(as.matrix(df), name = "mat",# right_annotation = rowAnnotation(foo = anno),
                row_split = df2$Name)
  order_rows <- row_order(h_order)
  order_cols <- column_order(h_order)
  
  
  # Colours
  # (each value, one number. Zero remains 0)
  df3 <- df2 %>%
    mutate(across(where(is.numeric), 
        ~ifelse(Name=="Ent", .*1,
        ifelse(Name=="St", .*2,
        ifelse(Name=="Ps", .*3,
        ifelse(Name=="Pm", .*4,
        ifelse(Name=="KECS", .*5,
        ifelse(Name=="Ecoli", .*6, NA_real_)
        )))))))%>%
    mutate_if(is.numeric, as.character) %>%
    select(-Name)
  
  col <- c(brewer.pal(n = 6, name = "Dark2"))
  col <- c("#FFFFFF", col) # add white for 0
  
  # Annotations
  text_list = list(
    text1 = "Ecoli", text2="Ent", text3="KECS",
    text4="Pm", text5="Ps", text6="St")
  ha = rowAnnotation(
    empty = anno_empty(border=FALSE),
    foo = anno_empty(border = FALSE, 
          width = max_text_width(unlist(text_list)) + unit(4, "mm")))

  
  # Heatmap
  hh <- Heatmap(as.matrix(df3), name = "mat", 
          # right_annotation = ha, # !!! un-comment if annotations are added!!!
          row_split = df2$Name,
          row_order = unlist(order_rows),
          column_order = order_cols,
          show_row_names = FALSE, show_column_names = FALSE,
          show_row_dend = FALSE, show_column_dend = FALSE,
          col=col,
          column_title = "KOs",
          column_title_side='bottom',
          row_title="Strains",
          show_heatmap_legend=FALSE,
          column_title_gp = gpar(fontsize = 11),
          row_title_gp = gpar(fontsize = 11)
          )
  
  # Annotations (part 2, add to image created)
  # (If you want them, un-comment the right_annotation above !!! )
  add_annotations <- function(){
  col2 <- c(brewer.pal(n = 6, name = "Dark2")) # remove white
  col2 = col2[c(6,1,5,4,3,2)]
  for(i in 1:6) {
    decorate_annotation("foo", slice = i, {
      grid.rect(x = 0, width = unit(1, "mm"), 
                gp = gpar(fill = col2[i], col = NA),
                just = "left")
      grid.text(paste(text_list[[i]], collapse = "\n"), 
                x = unit(2, "mm"), just = "left",
                gp=gpar(fontsize=9))
    })}
  }
  
  
  return(list(
    hh = hh,
    function_add_annotations= add_annotations
  ))
   
}


# # To run:
# file_1a = "all.csv"
# source_1a = "~/Documents/GitHub/UTI_bacteria_interactions/src/visualization/util/fig2/temp/KO_binary_matrices/"
# return_1a <- make_KO_binary_plots_colourized(file_1a, source_1a)
# hm_1a <- return_1a$hh
# func_1a <- return_1a$function_add_annotations


