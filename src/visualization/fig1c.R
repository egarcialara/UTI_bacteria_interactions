# x-axis: avg correlation of complementarity index vs growth yield
# y-axis: avg correlation of complementarity index vs growth rate
# Group in the 6 groups. Add sd for both axis.
# Legend TBD

# libraries
library(ggplot2)
library(RColorBrewer)
library(readxl)
library(dplyr)
library(tidyverse)


# Get data
index_dir = paste(getwd(), "/created/interaction_matrices/complementarity_3/", sep="")
growth_dir <- paste(getwd(), "/created/growth/", sep="")
growth_rate_file <- paste(growth_dir, "GR_3.csv", sep="")
growth_yield_file <- paste(growth_dir, "MaxOD_3.csv", sep="")

saving_dir <- "~/Documents/GitHub/UTI_bacteria_interactions/figures/exploratory/"
saving_file <- paste(saving_dir, "correlation_rate_vs_yield", sep="")
saving_format = ".pdf"


make_fig1c <- function(growth_rate_file, growth_yield_file, legend){
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
  
  
  
  
  # Per pathway
  list_cor_rate <- c()
  list_cor_yield <- c()
  list_cor_rate_p <- c()
  list_cor_yield_p <- c()
  names_sel <- c("Ecoli", "Ent", "KECS", "Pm", "Ps", "St")
  for(pathway in list.files(index_dir, pattern="*.csv")){
      index_file <- paste(index_dir, pathway, sep="")
      df <- read.csv(index_file, row.names=1)
  
      # aggregate
      df$groups <- t(as.data.frame(str_split(rownames(df),"[.]"),stringsAsFactors = FALSE)[1,])
      df2 <- df %>%
        group_by(groups) %>%
        summarize(across(everything(), mean, na.rm=TRUE))
      df3 <- data.frame(t(df2[c(2:ncol(df2))])) 
      df3$groups <- t(as.data.frame(str_split(rownames(df3),"[.]"),stringsAsFactors = FALSE)[1,])
      df3 <- df3 %>%
        group_by(groups) %>%
        summarize(across(everything(), mean, na.rm=TRUE))
      colnames(df3) <- c("Groups", df2$groups)
      
      # correlation
      v <- unlist(df3[names_sel])
      v_rate <- unlist(df_rate3[names_sel])
      v_yield <- unlist(df_yield3[names_sel])
      cor_rate <- cor.test(v, v_rate, method="spearman")
      cor_yield <- cor.test(v, v_yield, method="spearman")
      list_cor_rate <- c(list_cor_rate, cor(v, v_rate, method="spearman"))
      list_cor_rate_p <- c(list_cor_rate_p, cor_rate$p.value)
      list_cor_yield <- c(list_cor_yield, cor(v, v_yield, method="spearman"))
      list_cor_yield_p <- c(list_cor_yield_p, cor_yield$p.value)
  }
  
  
  df_plot <- data.frame(
    values_rate = list_cor_rate, values_yield = list_cor_yield,
    pvals_rate = list_cor_rate_p, pvals_yield = list_cor_yield_p
  ) %>%
    rowwise%>%
    mutate(pval = max(pvals_rate, pvals_yield))
  
  # Save (part1)
  # pdf(paste(saving_file, saving_format, sep=""))
  
  if(legend==FALSE){
    fig_decoration <- theme(legend.position = "none")
  }else{
    fig_decoration <- theme(legend.box='horizontal')
  }
  
  fig_1c <- df_plot %>%
    ggplot()+
    geom_point(aes(x=values_rate, y=values_yield, colour=pval))+
    geom_abline(colour="gray", linetype = "dashed")+
    lims(x=c(-0.7, 0.7), y=c(-0.7, 0.7))+
    scale_colour_gradientn(colours=c("blue", "red"), breaks=c(0.05, 0.25,0.50,0.75),
                           limits=c(0.05,max(df_plot$pval)), oob = scales::censor, na.value="darkblue")+
    theme_minimal()+
    labs(x="Correlation complementarity 3 vs growth rate",
         y="Correlation complementarity 3 vs growth yield",
         colour="Max pvalue")+
    fig_decoration
  
  # Save (part 2)
  # dev.off()
  return(fig_1c)
}
