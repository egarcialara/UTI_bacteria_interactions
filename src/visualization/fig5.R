source("src/visualization/fig2_function.R")
library(ggplot2)


# ---
# Same as Figs 2a-c - pathway 2: Folate biosynthesis
source_dir_5b = "~/Documents/GitHub/UTI_bacteria_interactions/created/interaction_matrices/complementarity_3/"
file_5b = "Folate biosynthesis.csv"
title_5b = "Folate biosynthesis"
results_fig5b <- make_fig2(file_5b, source_dir_5b, title_5b)
h5b <- results_fig5b$hm
funct5b <- results_fig5b$func
#
grid.newpage()
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
draw(h5b)
funct5b()
popViewport()
grab5b <- grid.grab()

# ---
# Same as Figs 3a-c
file = paste(index_dir, "Folate biosynthesis.csv",sep="")
fig5b <- plot_vs_growth(file, list_growth$yield$value, 
                        "Complementarity 3", "Growth (Max OD)", 
                        "Folate biosynthesis", rows=1)

# -----------------------------------------------------------
create_barplot <- function(df){
  
  p <- df %>%
    ggplot()+
    geom_bar(aes(x=names, y=values), stat="identity",
             width=0.6, fill="#1B9E77")+
    scale_x_discrete(breaks=df$names,
                     labels=unlist(labelsss))+
    labs(y="Change in population size")+
    # labs(title="Change in Enterococcus population, with addition of folic acid")+ # leave for caption?
    theme_minimal() + 
    theme(axis.title.x=element_blank())
          # axis.title.y=element_blank())
  
  return(p)
  
}

labelsss <- list(
  "A"="Blanc", 
  "B"= expression(atop(paste("10", mu, "M",sep=""), paste("folic acid"))),
  "C"= expression(atop(paste("50", mu,"M",sep=""), paste("folic acid"))),
  "D"= expression(atop(paste("100", mu,"M",sep=""), paste("folic acid")))
)


results <- data.frame(
  A.blanc = c(0.002,0.003,0.004,0.002,0.002,0.003),
  B.ten = c(0.002,0.003,0.004,0.003,0.003,0.005), # FAKE
  C.fifty = c(0.004,0.005,0.007,0.006,0.007,0.009), 
  D.hundred = c(0.004,0.004,0.005,0.003,0.004,0.005) # FAKE
)%>%
    summarize(
      across(A.blanc:D.hundred, c(mean, sd))
    )

# results2 <- results %>%
#   mutate(
#     A.blanc = A.blanc / A.blanc,
#     B.ten = B.ten/A.blanc,
#     C.fifty = C.fifty/A.blanc,
#     D.hundred = D.hundred/A.blanc
#   ) %>%
#   summarize(
#     across(A.blanc:D.hundred, c(mean, sd))
#   )
df_exps <- data.frame(
  mean = c(results$A.blanc_1, results$B.ten_1,
           results$C.fifty_1, results$D.hundred_1),
  sd = c(results$A.blanc_2, results$B.ten_2,
           results$C.fifty_2, results$D.hundred_2),
  names = c("A", "B", "C", "D")
) %>%
  mutate(
    values = mean / results$A.blanc_1
  )

p1 <- create_barplot(df_exps)
p1

p1_error <- p1 + 
  geom_errorbar(aes(x=names, y=values, ymin=values-sd, ymax=values+sd))#, width=1)


# ---
# 850 x 450
cowplot::plot_grid(
  grab5b,
  fig5b,
  p1,
  labels = c("A", "B", "C", NA),
  scale=c(.9, .8, .8, NA),
  align = "hv")

