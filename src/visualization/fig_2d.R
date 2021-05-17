library(circlize)
library(ggplot2)
library(cowplot)
library(dplyr)
library(tidyverse)


get_growth_arrays <- function(){
  
  # Read files
  df_rate <- read.csv(growth_rate_file)
  df_yield <- read.csv(growth_yield_file)
  
  # Clean infinites
  df_rate <- do.call(data.frame,lapply(df_rate, function(x) replace(x, is.infinite(x),NA)))
  df_yield <- do.call(data.frame,lapply(df_yield, function(x) replace(x, is.infinite(x),NA)))
  
  # Aggregate - please dont judge me
  # rate
  df_rate <- df_rate %>%
    mutate(X = as.character(X)) %>%
    group_by(X) %>%
    summarize(across(everything(), mean, na.rm=TRUE))
  
  df_rate2 <- data.frame(t(df_rate[c(2:ncol(df_rate))])) 
  df_rate2$groups <- t(as.data.frame(str_split(rownames(df_rate2),"[.]"),stringsAsFactors = FALSE)[1,])
  df_rate2 <- df_rate2 %>%
    group_by(groups) %>%
    summarize(across(everything(), mean, na.rm=TRUE))
  colnames(df_rate2) <- c("Groups", df_rate$X)
  df_rate3 <- df_rate2 %>% select(-MM)%>%filter(!Groups=="MM")
  
  # yield
  df_yield <- df_yield %>%
    mutate(X = as.character(X)) %>%
    group_by(X) %>%
    summarize(across(everything(), mean, na.rm=TRUE))
  
  df_yield2 <- data.frame(t(df_yield[c(2:ncol(df_yield))])) 
  df_yield2$groups <- t(as.data.frame(str_split(rownames(df_yield2),"[.]"),stringsAsFactors = FALSE)[1,])
  df_yield2 <- df_yield2 %>%
    group_by(groups) %>%
    summarize(across(everything(), mean, na.rm=TRUE))
  colnames(df_yield2) <- c("Groups", df_yield$X)
  df_yield3 <- df_yield2 %>% select(-MM)%>%filter(!Groups=="MM")
  
  return(list(yield=df_yield3, rate=df_rate3))
}


make_corr <- function(index_dir, growth_rate_file, growth_yield_file){
  
  # Per pathway / module
  list_cor_rate <- c()
  list_cor_yield <- c()
  list_cor_rate_p <- c()
  list_cor_yield_p <- c()
  names_sel <- c("Ecoli", "Ent", "KECS", "Pm", "Ps", "St")
  for(pathway in list.files(index_dir, pattern="*.csv")){
    index_file <- paste(index_dir, pathway, sep="")
    df <- read.csv(index_file, row.names=1)
    
    # aggregate
    df$groups <- t(as.data.frame(str_split(rownames(df),"[.]"),
                                 stringsAsFactors = FALSE)[1,])
    df2 <- df %>%
      group_by(groups) %>%
      summarize(across(everything(), mean, na.rm=TRUE))
    df3 <- data.frame(t(df2[c(2:ncol(df2))])) 
    df3$groups <- t(as.data.frame(str_split(rownames(df3),"[.]"),
                                  stringsAsFactors = FALSE)[1,])
    df3 <- df3 %>%
      group_by(groups) %>%
      summarize(across(everything(), mean, na.rm=TRUE))
    colnames(df3) <- c("Groups", df2$groups)
    df3 <- df3 %>% filter(!Groups=="MM") 
    if("MM" %in% colnames(df3)){df3<-df3%>% select(-"MM")}
    
    # correlation
    list_ = get_growth_arrays()
    df_rate3 <- list_$rate
    df_yield3 <- list_$yield
    #
    v <- unlist(df3[names_sel])
    v_rate <- unlist(df_rate3[names_sel])
    v_yield <- unlist(df_yield3[names_sel])
    cor_rate <- cor.test(v, v_rate, method="pearson")
    cor_yield <- cor.test(v, v_yield, method="pearson")
    list_cor_rate <- c(list_cor_rate, cor(v, v_rate, method="pearson"))
    list_cor_rate_p <- c(list_cor_rate_p, cor_rate$p.value)
    list_cor_yield <- c(list_cor_yield, cor(v, v_yield, method="pearson"))
    list_cor_yield_p <- c(list_cor_yield_p, cor_yield$p.value)
  }
  
  return(list_cor_yield)
  
}


plot_corr <- function(list_pathways, list_modules, list_all){
  
  max.len = max(length(list_pathways), length(list_modules))
  
  df_plot <- data.frame(
    "pathways" = c(list_pathways, rep(NA, max.len-length(list_pathways))),
    "modules" = c(list_modules, rep(NA, max.len-length(list_modules)))
  ) %>%
    pivot_longer(col=c("pathways", "modules"),
                 names_to = "Names",
                 values_to = "Values")
  
  p_corr <- df_plot %>%
    ggplot()+
    geom_density(aes(Values, fill=Names),
                 alpha=0.6)+
    geom_vline(aes(xintercept=list_all[[1]]), col="grey50")+
    scale_fill_manual(values=c("pathways" = "#5B84B1",
                                 "modules" = "#FC766A")) +
    theme_minimal()+
    labs(y="", x="Correlation", 
           fill="Full KO list\n segmentation")+
    lims(x=c(-0.45, 0.85))
  
  return(p_corr)
  
}



run_together <- function(growth_dir, growth_yield_file,
                         index_pathways, index_modules, index_all
                         ){
  
  # Pathways
  list_cor_pathways <- make_corr(index_pathways, growth_rate_file, growth_yield_file)
  
  # Modules
  list_cor_modules <- make_corr(index_modules, growth_rate_file, growth_yield_file)
  
  # All
  list_cor_all = make_corr(index_all, growth_rate_file, growth_yield_file)
  
  # Plot
  col <- c(RColorBrewer::brewer.pal(n = 3, name = "Dark2"))
  p_corr <- plot_corr(list_cor_pathways, list_cor_modules, list_cor_all)
  
  return(p_corr)
  
}

# To run:
# growth_dir <- paste(getwd(), "/created/growth/", sep="")
# growth_yield_file <- paste(growth_dir, "MaxOD_3.csv", sep="")
# index_pathways = paste(getwd(), "/created/interaction_matrices/complementarity_3/", sep="")
# index_modules = paste(getwd(), "/src/visualization/util/fig2/temp/complementarity_3/", sep="")
# index_all = paste(getwd(), "/src/visualization/util/fig2/temp/complementarity_3/all/", sep="")
# run_together(growth_dir, growth_yield_file, index_pathways, index_modules, index_all)

