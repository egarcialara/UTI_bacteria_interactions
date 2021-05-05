source("src/visualization/fig2_function.R")
library(ggplot2)

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
  "D"= expression(atop(paste("100", mu,sep=""), paste("folic acid")))
)


results <- data.frame(
  A.blanc = c(0.002,0.003,0.004,0.002,0.002,0.003),
  B.ten = c(0.002,0.006,0.002,0.001,0.005,0.004), # FAKE
  C.fifty = c(0.004,0.005,0.007,0.006,0.007,0.009), 
  D.hundred = c(0.003,0.005,0.002,0.006,0.001,0.003) # FAKE
)%>%
  summarize(
    across(A.blanc:D.hundred, c(mean, sd))
  )
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

# ---
# Same as Figs 2a-c - pathway 2: Folate biosynthesis
source_dir_2d = "~/Documents/GitHub/UTI_bacteria_interactions/created/interaction_matrices/complementarity_3/"
file_2d = "Folate biosynthesis.csv"
title_2d = "Folate biosynthesis  \n"
results_fig2d <- make_fig2(file_2d, source_dir_2d, title_2d)
h2d <- results_fig2d$hm
funct2d <- results_fig2d$func
#
grid.newpage()
pushViewport(viewport(layout.pos.row = 1, layout.pos.col = 1))
draw(h2d)
funct2d()
popViewport()
grab2d <- grid.grab()

# ---
# 850 x 450
cowplot::plot_grid(
  p1,
  grab2d,
  labels = c("A", "B"),
  scale=c(.85, .85),
  align = "h")

