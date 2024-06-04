library(readr)
library(ggplot2)
library(ggridges)
library(tidyverse)


db_tot <- read_csv("Fin1024 - All.csv", 
                  col_types = cols(X1 = col_skip(), 
                  target = col_integer(), targetsize = col_integer(),
                  training = col_integer(), trainsize = col_integer()))

db_gen <- read_csv("Fin1024 - Generic.csv", 
                  col_types = cols(X1 = col_skip(), 
                  target = col_integer(), targetsize = col_integer(),
                  training = col_integer(), trainsize = col_integer()))


db_t2 <- read_csv("Fin1024T4 - AESSHA.csv", 
                  col_types = cols(X1 = col_skip(), 
                  target = col_integer(), targetsize = col_integer(),
                  training = col_integer(), trainsize = col_integer()))
db_t1 <- read_csv("Fin1024T4 - TDEAAES.csv", 
                  col_types = cols(X1 = col_skip(), 
                  target = col_integer(), targetsize = col_integer(),
                  training = col_integer(), trainsize = col_integer()))
db_target <- rbind(db_t1,db_t2)




# Different Training Plot - 1300x400 - PDF

db_train <- db_gen[db_gen$algs %in% c("('aes256', 'sha256')","('tdea', 'aes256')")
                   & db_gen$targetsize == 65536,]

db_train$algs <- factor(db_train$algs, levels = unique(db_train$algs), 
                         labels = (function(x) gsub(", "," - ",(gsub("[\\('\\)]","",x)))) 
                         (unique(db_train$algs)) )
db_train$algs <- factor(db_train$algs, levels = unique(db_train$algs), 
                        labels = (function(x) gsub(", "," - ",(gsub("[\\('\\)]","",x)))) 
                        (unique(db_train$algs)) )



ggplot(data = db_train ,aes(x = NB,fill=algs)) +
  #geom_density(alpha=0.4) +
  geom_vline(xintercept=0.5, linetype="dashed", color = "red") +
  
  geom_histogram(binwidth=0.0001, colour="black")+ 
  
  facet_grid( algs ~ trainsize ) +
  theme_bw()+
  theme(
    strip.text.x = element_text(size = 12, face = "bold"),
    strip.text.y = element_text(size = 12, face = "bold"),
    axis.title.x = element_text(size = 15, face = "bold", margin = margin(1,0,0,0,"lines")),
    axis.title.y = element_text(size = 15, face = "bold", margin = margin(0,1,0,0,"lines")),
    panel.spacing = unit(1, "lines"),
    legend.position = "none"
  ) +
  labs(x="Accuracy",y="# Distinguishers")

ggsave( "training.pdf", scale = 1, width = 270,  height = 120,
        units = "mm",  dpi = 300,  limitsize = FALSE)







# Different Target Plot - 1300x400 - PDF

db_target$target <- factor(db_target$target, levels = c(0,1,2,3), 
                  labels = (function(xx) paste("Target ",xx+1))(c(0,1,2,3)) )

db_target$algs <- factor(db_target$algs, levels = unique(db_target$algs), 
                        labels = (function(x) gsub(", "," - ",(gsub("[\\('\\)]","",x)))) 
                          (unique(db_target$algs)) )

ggplot(data = db_target, aes(x = NB,fill=algs)) +
  #geom_density(alpha=0.4) +
  geom_vline(xintercept=0.5, linetype="dashed", color = "red") +
  
  geom_histogram(binwidth=0.0001, colour="black")+ 
  
  facet_grid( algs ~ target ) +
  theme_bw()+
  theme(
    strip.text.x = element_text(size = 12, face = "bold"),
    strip.text.y = element_text(size = 12, face = "bold"),
    axis.title.x = element_text(size = 15, face = "bold", margin = margin(1,0,0,0,"lines")),
    axis.title.y = element_text(size = 15, face = "bold", margin = margin(0,1,0,0,"lines")),
    panel.spacing = unit(1, "lines"),
    
    legend.position = "none"
  ) +
  labs(x="Accuracy",y="# Distinguishers")

ggsave( "target.pdf", scale = 1, width = 270,  height = 120,
        units = "mm",  dpi = 300,  limitsize = FALSE)





# Different General Combination Plot - 900x600 - PDF

db_gen$algs <- factor(db_gen$algs, levels = unique(db_gen$algs), 
                         labels = (function(x) gsub(", "," - ",(gsub("[\\('\\)]","",x)))) 
                         (unique(db_gen$algs)))
db_gen$trainsize <- factor(db_gen$trainsize, levels = unique(db_gen$trainsize), 
                      labels = (function(x) paste("TrainingSize =",x) ) 
                      (unique(db_gen$trainsize)) )
db_gen$targetsize <- factor(db_gen$targetsize, levels = unique(db_gen$targetsize), 
                           labels = (function(x) paste("TargetSize =",x) ) 
                           (unique(db_gen$targetsize)) )



ggplot(data = db_gen, aes(x = NB,y=algs,fill=algs)) +
  #geom_density(alpha=0.4,aes(height = ..scaled..)) +
  geom_density_ridges(scale = 3)+
  xlim(0.4925, 0.5075)+

  geom_vline(xintercept=0.5, linetype="dashed", color = "red") +
  #geom_histogram(bins = 32, colour="black")+ 
  
  
  facet_grid( targetsize ~ trainsize ) +
  theme_bw()+
  theme(
    strip.text.x = element_text(size = 12, face = "bold"),
    strip.text.y = element_text(size = 12, face = "bold"),
    axis.title.x = element_text(size = 15, face = "bold", margin = margin(1,0,0,0,"lines")),
    #axis.title.y = element_text(size = 15, face = "bold", margin = margin(0,1,0,0,"lines")),
    panel.spacing = unit(1, "lines"),
    
    legend.position = "none"
  ) +
  labs(x="Accuracy",y="")

ggsave( "general.pdf", scale = 1, width = 270,  height = 180,
        units = "mm",  dpi = 300,  limitsize = FALSE)






# Different All Combination Plot - 900x600 - PDF

db_tot$algs <- factor(db_tot$algs, levels = unique(db_tot$algs), 
                      labels = (function(x) gsub(", "," - ",(gsub("[\\('\\)]","",x)))) 
                      (unique(db_tot$algs)))

db_tot$algs <- reorder(db_tot$algs, db_tot$NB, var)

ggplot(data = db_tot[db_tot$NB > 0.494 & db_tot$NB < 0.506, ], aes(x = NB, y=algs, fill=algs)) +
  #geom_density(alpha=0.4,aes(height = ..scaled..)) +
  geom_density_ridges(scale = 4)+
  
  scale_x_continuous(n.breaks = 10) +
  
    
  geom_vline(xintercept=0.5, linetype="dashed", color = "red") +
  #geom_histogram(bins = 32, colour="black")+ 
  
  
  #facet_grid( targetsize ~ trainsize ) +
  theme_bw()+
  theme(
    strip.text.x = element_text(size = 12, face = "bold"),
    strip.text.y = element_text(size = 12, face = "bold"),
    axis.title.x = element_text(size = 15, face = "bold", margin = margin(0.3,0,0,0,"lines")),
    #axis.title.y = element_text(size = 15, face = "bold", margin = margin(0,1,0,0,"lines")),
    panel.spacing = unit(1, "lines"),
    
    legend.position = "none"
  ) +
  labs(x="Accuracy",y="")


ggsave( "all.pdf", scale = 1, width = 270,  height = 420,
        units = "mm",  dpi = 300,  limitsize = FALSE)

