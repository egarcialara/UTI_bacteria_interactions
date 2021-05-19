
library(igraph)

library(NetPathMiner)
#Load a kegg KGML map. can be obtained e.g. wget http://rest.kegg.jp/get/ko00340/kgml -O ko00340.xml
rgraph <- KGML2igraph("/home/chrats/Desktop/UTI_test/UTI_bacteria_interactions/created/histidine/ko00340.xml")

#modify shape of the network for compound and reaction
V(rgraph)$shape <-ifelse(grepl("C",names(V(rgraph))),"circle","square")

#clean reaction name
rgraph<-set.vertex.attribute(rgraph, "name", value=gsub("rn:","",names(V(rgraph))))
rgraph<-set.vertex.attribute(rgraph, "name", value=unlist(lapply(strsplit(names(V(rgraph))," "), function(x) x[1])))

#obtain KO information for each reaction
library(KEGGREST)
rn<-names(V(rgraph))[grepl("R",names(V(rgraph)))]
rn_all<-list()
for (j in 1:length(rn)){
  tryCatch({
    rn_all[[j]]<-keggGet(rn[j])
  }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
}
rn_all_ko<-lapply(rn_all, function(x) x[[1]]$ORTHOLOGY)
names(rn_all_ko)<-rn

#load KO bianry matrix of realavent pathway
Histidine <- read.csv("/home/chrats/Desktop/UTI_test/UTI_bacteria_interactions/created/histidine/Histidine metabolism.csv")
genomes<-as.matrix(Histidine)[,1]

Histidine<-Histidine[-match("MM.45",genomes),]
Histidine<-apply(as.matrix(Histidine[,-1]), 2, as.integer)
rownames(Histidine)<-genomes[-match("MM.45",genomes)]
Histidine<-Histidine[,-which(colSums(Histidine)==0)]

#reduce graph based on the binary KO matrix
rn_toremove<-lapply(rn_all_ko, function(x) all((names(x)%in%colnames(Histidine))==F))
rn_toremove_names<-names(which(unlist(rn_toremove)==T))

##### remove disconected reactions R04065 and R04674
rgraph_rR<-delete_vertices(rgraph,match(c("R04065","R04674"),names(V(rgraph))))
##################

rgraph_r<-delete_vertices(rgraph_rR, unlist(lapply(rn_toremove_names, function(x) grep(x,names(V(rgraph_rR))))))
Isolated = which(degree(rgraph_r)==0)
rgraph_r2 = delete.vertices(rgraph_r, Isolated)
V(rgraph_r2)$label.cex<-1



#######obtain compound names
cmp<-names(V(rgraph_r2))[grepl("C",names(V(rgraph_r2)))]
cmp_all<-list()
for (j in 1:length(cmp)){
  tryCatch({
    cmp_all[[j]]<-keggGet(cmp[j])
  }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
}
cmp_all_name<-lapply(cmp_all, function(x) x[[1]]$NAME)
names(cmp_all_name)<-cmp

cmp_all_name_s<-lapply(cmp_all_name, function(x) x[1])


V(rgraph_r2)$size <-ifelse(grepl("C",names(V(rgraph_r2))),3,15)
coords <-  layout_with_fr(rgraph_r2)
layout1 <- layout.fruchterman.reingold(rgraph_r2)

plot(rgraph_r2, layout = coords,vertex.label.dist=1.2,vertex.label.degree = -1.5,main="",edge.width=3,edge.curved=0.2,vertex.frame.width=13,
     vertex.label.color=ifelse(grepl("C",names(V(rgraph_r2))),"#2c7fb8","black"),
     vertex.label.font=2,margin=-.05)
rgraph_r2_u<-as.undirected(rgraph_r2)

plot(rgraph_r2_u, layout = coords,main="",edge.width=3,edge.curved=0.3,vertex.frame.width=10,
     vertex.label.color=ifelse(grepl("C",names(V(rgraph_r2))),"#2c7fb8","black"),
     vertex.label.font=2,margin=0)


V(rgraph_r2_u)$shape <-ifelse(grepl("C",names(V(rgraph_r2_u))),"circle","none")
E(rgraph_r2_u)$weight = 2
V(rgraph_r2_u)$size <-ifelse(grepl("C",names(V(rgraph_r2_u))),3,10)
V(rgraph_r2_u)$label.cex =0.8

layout1<-layout_as_tree(rgraph_r2_u,root = 22)
plot(rgraph_r2_u,  layout=layout1,main="",edge.width=3,edge.curved=0,vertex.frame.width=10,
     vertex.label.color=ifelse(grepl("C",names(V(rgraph_r2))),"#2c7fb8","black"),
     vertex.label.font=2,margin=0)
#############print list of reaction and compounds with names
library(KEGGREST)
rn<-names(V(rgraph_r2_u))[grepl("R",names(V(rgraph_r2_u)))]
rn_all<-list()
for (j in 1:length(rn)){
  tryCatch({
    rn_all[[j]]<-keggGet(rn[j])
  }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
}
final_to_print<-lapply(rn_all, function(x) x[[1]]$NAME)
names(final_to_print)<-rn

paste(paste0(names(unlist(final_to_print)),": ", unlist(final_to_print),", ",sep=""), collapse = "")
paste(paste0(names(unlist(cmp_all_name_s)),": ", unlist(cmp_all_name_s),", ",sep=""), collapse = "")

################################# 
#make barplots per reaction
################################
  grouping<-unlist(lapply(strsplit(rownames(Histidine),"[.]"), function(x) x[1]))
  library(reshape2)
  library(ggplot2)
  theme_set(theme_bw())
  names_legend<-c("Ecoli" , "Ent", "KECS", "Pm",  "Ps", "St")
  colors_legend<-c("#E6AB02","#1B9E77" ,"#66A61E", "#E7298A"  ,"#7570B3" ,"#D95F02")
  max_y<-max(apply(Histidine, 2, function(x) tapply(x, grouping, FUN=sum)))
  z<-max(table(grouping))
  store_plots<-list()
  for (j in 1:length(rn_all_ko)){
    print(j)
    temp<-match(names(rn_all_ko[[j]]),colnames(Histidine))
    temp<-temp[!is.na(temp)]
    
    if(length(temp)==1){
      data_temp<-Histidine[,temp]
      data<-tapply(data_temp, grouping, FUN=sum)
      data_rs<-data
      data_rs<-as.data.frame(data_rs)
      data_rs$g<-factor(rownames(data_rs),levels=names_legend)
      data_rs$data_rs<-data_rs$data_rs/table(grouping)*100
      gg<-ggplot(data_rs, aes(x=g, y=data_rs,fill=g)) + scale_fill_manual(values=colors_legend)+
        geom_bar(stat="identity")+labs(x="",y=names(rn_all_ko)[j])+theme(axis.text.x = element_blank(),legend.position = "none",
                                                                         axis.text.y = element_blank(),panel.border = element_rect(colour = "black", fill=NA, size=5),
                                                                         axis.ticks = element_blank(),axis.title.y = element_text( size=70,face="bold"))+ylim(0,100)
      plot(gg)
      ggsave(file=paste("/home/chrats/Desktop/UTI_test/UTI_bacteria_interactions/created/histidine/",names(rn_all_ko)[j],".pdf",sep = ""),dpi=600, width = 5, height = 4)
    }else if(length(temp)>1){
      data_temp<-Histidine[,temp]
      single<-rowSums(data_temp)
      single[single>1]<-1
      data_rs<-tapply(single, grouping, FUN=sum)
      data_rs<-as.data.frame(data_rs)
      data_rs$g<-factor(rownames(data_rs),levels=names_legend)
      data_rs$data_rs<-data_rs$data_rs/table(grouping)*100
      gg<-ggplot(data_rs, aes(x=g, y=data_rs,fill=g)) + scale_fill_manual(values=colors_legend)+
            geom_bar(stat="identity")+labs(x="",y=names(rn_all_ko)[j])+theme(axis.text.x = element_blank(),legend.position = "none",
                                                                         axis.text.y = element_blank(),panel.border = element_rect(colour = "black", fill=NA, size=5),
                                                                         axis.ticks = element_blank(),axis.title.y = element_text( size=70,face="bold"))+ylim(0,100)
      plot(gg)
      ggsave(file=paste("/home/chrats/Desktop/UTI_test/UTI_bacteria_interactions/created/histidine/",names(rn_all_ko)[j],".pdf",sep = ""),dpi=600, width = 5, height = 4)
    }
    
  
    
  }
