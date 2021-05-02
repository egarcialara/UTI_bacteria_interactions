library(circlize)
library(ggpubr)
library(cowplot)
library(dplyr)
library(stringr)
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
  df_rate3 <- df_rate2 %>% select(-MM)%>%filter(!Groups=="MM")%>%
    pivot_longer(c(Ecoli, Ent, KECS, Pm, Ps, St))
  
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
  df_yield3 <- df_yield2 %>% select(-MM)%>%filter(!Groups=="MM")%>%
    pivot_longer(c(Ecoli, Ent, KECS, Pm, Ps, St))
  
  return(list(yield=df_yield3, rate=df_rate3))
}



plot_vs_growth <- function(file, growth, name_index, name_growth, name_title, legend=FALSE, rows=NULL){
  
  # Read files
  df <- read.csv(file, header=TRUE, row.names=rows)

  # Aggregate - please dont judge me
  if(!is.null(rows)){
    df$groups <- t(as.data.frame(str_split(rownames(df),"[.]"),stringsAsFactors = FALSE)[1,])
    df <- df %>%
      group_by(groups) %>%
      summarize(across(everything(), mean, na.rm=TRUE))
      df2 <- data.frame(t(df[c(2:ncol(df))]))
    names_for_later <- df$groups
  }else{
    df <- df %>%
      mutate(X = as.character(X)) %>%
      group_by(X) %>%
      summarize(across(everything(), mean, na.rm=TRUE))
    names_for_later <- df$X
    }
  
  df2 <- data.frame(t(df[c(2:ncol(df))])) 
  df2$groups <- t(as.data.frame(str_split(rownames(df2),"[.]"),stringsAsFactors = FALSE)[1,])
  df2 <- df2 %>%
    group_by(groups) %>%
    summarize(across(everything(), mean, na.rm=TRUE))
  colnames(df2) <- c("Groups", names_for_later)
  df2 <- as.data.frame(as.matrix(df2),stringsAsFactors = FALSE)

  df3 <- df2 %>%
    mutate(MM="aa")%>%
    select(-MM)%>%
    filter(Groups!="MM")%>%
    pivot_longer(c(Ecoli, Ent, KECS, Pm, Ps, St)) %>%
    rename(
      Donor = Groups,
      Acceptor = name,
      complementarity_3 = value
    ) %>%
    mutate(growth = growth)
  
  if(!is.null(rows)){
    minx = NA_integer_
    maxx=NA_integer_
  }else{
    minx=0
    maxx=1
  }
  
  # (add legend or not)
  if(legend==FALSE){
    fig_decoration <- theme(legend.position = "none")
  }else{
    fig_decoration <- theme(legend.box='horizontal')
  }
  
  # Plot
  p <- df3 %>%
    ggplot(aes(x=as.double(complementarity_3), y=growth,
               colour = Donor,
               shape=Acceptor))+
    geom_point()+
    theme_classic()+
    scale_colour_manual(values=col)+
    labs(x=name_index, y=name_growth,
    title=name_title)+
    lims(x=c(minx,maxx), y=c(-1,1)) +
    fig_decoration
  
  return(p)
    
}