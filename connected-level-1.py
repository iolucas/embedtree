import sys

import py2neo
from py2neo import Graph

import networkx as nx

import matplotlib.pyplot as plt


#Load database
py2neo.authenticate("localhost:7474", "neo4j", "lucas")
graph = Graph("http://localhost:7474/db/data/")

#Get article title from the args
connection = sys.argv[1]
method = sys.argv[2]
articleTitle = sys.argv[3]


#Construct the query
dbQuery = " ".join([
    'MATCH (n1:Article {title:"ARTICLE-TITLE"})-[l1:ConnectsTo]->(n2:Article)',
    'OPTIONAL MATCH (n2)-[l2:ConnectsTo]->(n3:Article)',
    'WHERE (n1)-[:ConnectsTo]->(n3)',
    'RETURN n2,n3'
]).replace("ARTICLE-TITLE", articleTitle)

#Execute it
results = graph.run(dbQuery)


#Create a directed graph

G = nx.DiGraph()

#Iterate thru results adding nodes and edges to the graph
for r in results:
    #If there is no node3, only add node 2 title
    if r['n3'] == None:
        G.add_node(r['n2']['title'])
    else: #If there is node 3, there is a relation, add it directly so nodes are add automatically
        G.add_edge(r['n2']['title'], r['n3']['title'])

#Get the connected nodes of G according to choose method
if connection == 'weak':
    sc_nodes = nx.weakly_connected_components(G)
elif connection == 'strong':
    sc_nodes = nx.strongly_connected_components(G)

subgraphs = [G.subgraph(nlist) for nlist in sc_nodes]

#Function to compute incomming edges
def sumInEdges(g):
    connDict = dict() #Dictionary to compute values
    edges = g.edges() #get graph edges

    if not edges: #If there is no edges
        connDict[g.nodes()[0]] = 0 #Put only the first node found and return

    for e in edges: #iterate thru edges
        target = e[1] #get target
        if not target in connDict: #if the target has not been initiated @ the dict,
            connDict[target] = 0 #init it
        connDict[target] += 1 #Sum one value
    
    return connDict #return the dict

#Array to keep the clusters found 
clusters = []

#Iterate thru the subgraphs
for dir_sg in subgraphs:
    #Compute the most import node of the cluster
    #We may use the page rank, or only the incomming edges sum

    if method == 'pagerank':
        pr = nx.pagerank(dir_sg).items() #Pagerank
    elif method == 'sum':
        pr = sumInEdges(dir_sg).items() #Incomming edges

    biggestPr = max(pr, key=lambda a: a[1])[0] #Select the biggest value to represent the cluster
    clusters.append((biggestPr, len(dir_sg.nodes()))) #Append it to the subgraphs with the number of nodes

#Print sorted results
for n in sorted(clusters, key=lambda a: a[1], reverse=True):
    print n




# nx.draw(G)
# plt.show()



