def do_heatmap(df, name, name_pw):
    # plots heatmap, including cluster
    # make it look better pls (???)
    try:
        cm = sns.clustermap(df, col_cluster=True, row_cluster=True, metric='correlation', cmap='Greys')  #  'cosine'
        ## metric = braycurtis, correlation
        ## col_culster=False/True
        # cm = sns.heatmap(df)#, col_cluster=True, metric='correlation', cmap='Greys')
        # cm = plt.pcolor(df)
    except:
        print 'Error in ' + name_pw
        return
    hm = cm.ax_heatmap.get_position()
    plt.setp(cm.ax_heatmap.yaxis.get_majorticklabels(), rotation=0 , fontsize=6)
    plt.setp(cm.ax_heatmap.xaxis.get_majorticklabels(), rotation=270, fontsize=6)
    # cm.ax_heatmap.set_position([hm.x0*0.57, hm.y0, hm.width*1.05, hm.height*1.3])
    # col = cm.ax_col_dendrogram.get_position()
    # cm.ax_col_dendrogram.set_position([col.x0, col.y0, col.width*0.25, col.height*0.5])
    # row = cm.ax_row_dendrogram.get_position()
    # cm.ax_row_dendrogram.set_position([row.x0*0., row.y0, row.width*1, row.height*1.3])
    plt.title(name_pw, loc='center')
    plt.savefig(name)
    print name, "was saved"
    # plt.show()



# modules table
# affinity propagation on similarity matrix (e.g. braycurtis) -> get representatives for each cluster
# (N)MDS on similarity
# tsne on both (binary, similarity)
