import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def cluster1D(n):
    G = nx.Graph()
    G.add_node(0,pos=(0,0))
    for i in range(n-1):
        G.add_node(i+1,pos=(i+1,0))
        G.add_edge(i,i+1)   
    return G
    
#nb(qubits) = n*n
def cluster2D(n):
    G = nx.Graph()
    for j in range(n) :
        if j ==0 :
            G.add_node(j*n,pos=(j,n-1))
            for i in range(n-1):
                G.add_node(j*n+i+1,pos=(j,n-i-2))
                G.add_edge(j*n+i,j*n+i+1)
        else : 
            G.add_node(j*n,pos=(j,n-1))
            for i in range(n-1):
                G.add_node(j*n+i+1,pos=(j,n-i-2))
                G.add_edge(j*n+i,j*n+i+1)
                G.add_edge(j*n+i,(j-1)*n+i)
            G.add_edge(j*n+i+1,(j-1)*n+i+1)
    return G

def draw_graph(Edges):
    G = nx.Graph()
    for E in Edges:
        G.add_edge(E[0],E[1])
    nx.draw(G,with_labels = True)
    plt.show(block = False)
    
    
#G = cluster2D(5)
#pos=nx.get_node_attributes(G,'pos')
#print(pos)
#pos = nx.circular_layout(G)
#nx.draw(G, pos, with_labels = True)
#nx.draw(G, pos, with_labels = True)
#plt.show()

#Edges = [[2, 3], [1, 3], [3, 4], [1, 5], [4, 5], [5, 6], [4, 7], [6, 7], [7, 8]]
##for E in Edges:
 #   G.add_edge(E[0],E[1])
#draw_graph(G,Edges)
#nx.draw(G, with_labels = True)
#plt.show()

def draw_graph_pos(Edges,ninput,nqubits):
    #plt.show()
    G = nx.Graph()
    Nodes = []
    l = 0
    c = 0
    nNodes = 0
    colors = []
    nEdges = len(Edges)
    len_edg = 0;
    for i in range(ninput):
        G.add_node(i+1,pos=(0,i))
        colors.append('blue')
        Nodes.append(i+1)
    nNodes = len(set(Nodes))
    New_Nodes = []
    for E in Edges:
        if E[0] <= ninput:
            if New_Nodes.count(E[1]) == 0:
                G.add_node(E[1],pos=(1,l))
                colors.append('gray')
                New_Nodes.append(E[1])
                #print("E = {} l = {} New_Nodes = {}".format(E,l,New_Nodes))
                l+=1
            G.add_edge(E[0],E[1])
            len_edg+=1
            #print("Ajoute E = {}".format(E))
    Nodes = Nodes + New_Nodes
    #print("Nodes = {}".format(Nodes))

   
    c = 2
    l = 0
    print("nNodes = {}".format(nNodes))
    while(len_edg != nEdges ):
        Temp_Nodes = []
        for E in Edges:
            if New_Nodes.count(E[0]) == 1:
                if Nodes.count(E[1]) == 0:
                    if Temp_Nodes.count(E[1]) == 0:
                        G.add_node(E[1],pos=(c,l))
                        colors.append('gray')
                        l+=1
                        Temp_Nodes.append(E[1])
                        #print("E = {} l = {} Temp_Nodes = {}".format(E,l,Temp_Nodes))
                G.add_edge(E[0],E[1])
                len_edg+=1
                #print("Ajoute E = {}".format(E))
        New_Nodes = Temp_Nodes
        Nodes = Nodes + New_Nodes
        #print("Nodes = {} New_Nodes = {}".format(Nodes,New_Nodes))
        #print("nNodes = {}".format(nNodes))
        c+=1
        l=0

    pos=nx.get_node_attributes(G,'pos')
    #splt.ion()
    #plt.show()
    nx.draw(G,pos,node_color=colors,with_labels = True)
    plt.pause(0.001)
    return G,pos,colors

def update_graph(G,pos,colors,idx_output):
    for node in G:
        if idx_output.count(node-1):
            colors[node-1]='red'
    #plt.ion()
    #plt.show()
    nx.draw(G,pos,node_color=colors,with_labels = True)
    plt.pause(0.001)

if __name__ == "__main__":

    Edges = [[1, 3], [3, 4], [2, 5], [4, 5], [5, 6], [4, 6]]
    ninput = 2
    nqubits = 6
    result=draw_graph_pos(Edges,ninput,nqubits)
    idx_output = [3,5]
    update_graph(result[0],result[1],result[2],idx_output)
    plt.show()