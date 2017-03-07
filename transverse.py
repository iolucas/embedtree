"""
Algorithm to compute required articles applying the pagerank algorithm to a graph generated by 
tranversing the target article by a few levels.
"""



"""
                                            ---NOTES---

- Tests showed that in_degree_centrality is better than pagerank to elect the most relevant nodes
- Clusters would be good to take the most variate areas of the knowledge but is hard to choose a 
algorithm and fitness function that can extract these areas



"""



#think how to construct things by this


import sys #Lib to interact with the system

import py2neo #Libs to connect to neo4j

import networkx as nx #Lib to create and manipulate graphs

from tabulate import tabulate #Lib to format data as tables before print

#import matplotlib.pyplot as plt #Lib to plot info graphics

VERBOSE = True #Flag to signalize whether to print process info or not

neo4jGraph = None #Connection to neo4j graph


def connectDb():
    """Function to connect to neo4j database."""

    global neo4jGraph

    printLog("Initing db...")
    py2neo.authenticate("localhost:7474", "neo4j", "lucas")
    neo4jGraph = py2neo.Graph("http://localhost:7474/db/data/")


def getGraph(articleTitle, transversalLevel):
    """Function to get a graph data from db and create a networkx graph."""

    #global neo4jGraph

    if neo4jGraph == None:
        raise "Neo4j not connected."

    #Create a directed graph
    G = nx.DiGraph()

    #All directions query based on forward nodes

    #Query all nodes id related to the seed node
    dbQuery = " ".join([
        'MATCH (n1:Article {name:"ARTICLE-TITLE"})-[l1:RefersTo*TRANSVERSAL-LEVEL]->(n2:Article)',
        'RETURN collect(DISTINCT ID(n1)) + collect(DISTINCT ID(n2)) as ids'
    ]).replace("ARTICLE-TITLE", articleTitle).replace("TRANSVERSAL-LEVEL", transversalLevel)

    nodeIds = [] #Array to keep node ids

    printLog("Querying ids...")

    #Execute query and compute ids
    for r in neo4jGraph.run(dbQuery):
        nodeIds += r['ids']

    #Now query all connectTo relations between these nodes
    dbQuery = " ".join([
        'MATCH (n1:Article)-[l1:RefersTo]-(n2:Article)',
        'WHERE (ID(n1) IN NODE-IDS AND ID(n2) IN NODE-IDS)',
        'RETURN l1 as edges'
    ]).replace("NODE-IDS", str(nodeIds))

    #QUery edges and create the graph with them
    printLog("Querying edges and create graph...")

    for val in neo4jGraph.run(dbQuery):
        e = val[0]
        G.add_edge(e.start_node()['name'], e.end_node()['name'])

    return G


def getGraphClusters(G, clusterAllocMethod, clusterRankMethod):

    #Delete main node if it is needed
    # if deleteMainNode:
    #     if verbose:
    #         print "Deleting main node..."
    #     G.remove_node(articleTitle)

    printLog("Generating clusters...")

    #Get the connected nodes of G according to choose method
    if clusterAllocMethod == 'weak':
        clusters_nodes = nx.weakly_connected_components(G)
    elif clusterAllocMethod == 'strong':
        clusters_nodes = nx.strongly_connected_components(G)

    printLog("Getting clusters graphs...")

    clusters_subgraphs = [G.subgraph(nlist) for nlist in clusters_nodes]

    #Array to keep the clusters
    clusters = []

    #Iterate thru the clusters subgraphs
    for cluster_sg in clusters_subgraphs:

        #Calculate the rank for each node in the cluster
        if clusterRankMethod == 'pagerank':
            cluster_node_ranks = nx.pagerank(cluster_sg).items() #Pagerank
        elif clusterRankMethod == 'in_degree':
            cluster_node_ranks = nx.in_degree_centrality(cluster_sg).items() #Incomming edges sum

        #Order cluster in decreasing order
        cluster_node_ranks = sorted(cluster_node_ranks, key=lambda a: a[1], reverse=False) 

        #Append the cluster to the clusters array with its length
        clusters.append((cluster_node_ranks, len(cluster_node_ranks)))

    #Order clusters in decreasing order
    clusters = sorted(clusters, key=lambda a: a[1], reverse=True) 

    return clusters


def getCentralNodes(G):
    """Function to get the central nodes of graph G based on incomming degree of the nodes."""

    centralNodes = nx.in_degree_centrality(G)
    sortedNodes = sorted(centralNodes.items(), key=lambda a: a[1], reverse=False)
    return sortedNodes

def printLog(msg):
    """Function to print data in case verbose flag is up."""
    if VERBOSE:
        print msg



def main(args):
    """Main function used for tests."""

    connectDb()
    G = getGraph(args[1], args[2])
    #clusters = getGraphClusters(G, "weak", "in_degree")

    centralNodes = reversed(getCentralNodes(G))

    for n in centralNodes:
        centralNode = n[0]
        break

    #print centralNode
    print ""

    keep working on creating the space with node datas
    

    targetNodes = []
    for edge in G.edges():
        if edge[1] == centralNode:
            targetNodes.append(edge[0])

    for d in map(lambda a: [a], targetNodes):
        print d


    # print ""
    # print(tabulate(map(lambda a: [a], centralNodes), headers=['centralNodes']))


if __name__ == "__main__":
    main(sys.argv)












#Function to get the article cluster
def getArticleClusters(articleTitle, transversalLevel, deleteMainNode, clusterAllocMethod, clusterRankMethod, neo4jGraph, verbose):

    def sortConcatAndPrint(dict1, dict2):

        #Sort
        sortedDict1 = sorted(dict1.items(), key=lambda a: a[1], reverse=False)
        sortedDict2 = sorted(dict2.items(), key=lambda a: a[1], reverse=False)

        #Concatenate
        dictSize = len(sortedDict1)
        printData = list()
        for i in xrange(dictSize):
            #Convert data to list to be editable
            sortedDict1[i] = list(sortedDict1[i])
            sortedDict2[i] = list(sortedDict2[i])

            #Truncate too long string
            sortedDict1[i][0] = sortedDict1[i][0][:40]
            sortedDict2[i][0] = sortedDict2[i][0][:40]

            #Round decimal values to fit on screen
            sortedDict1[i][1] = round(sortedDict1[i][1], 2)
            sortedDict2[i][1] = round(sortedDict2[i][1], 2)

            printData.append([str(sortedDict1[i]), str(sortedDict2[i])])

        #Print
        print(tabulate(printData, headers=['PageRank', 'InCentrality']))



    def sortAndPrint(items):
        sortedItems = sorted(items.items(), key=lambda a: a[1], reverse=False)
        for d in sortedItems:
            print d.encode('ascii', 'ignore')
    

    sortConcatAndPrint(pagerank, centrality)

    #print ""
    #sortAndPrint(centrality)

    #print ""
    #sortAndPrint(pagerank)

    sys.exit()



    if verbose:
        print "Generating clusters..."

    #Get the connected nodes of G according to choose method
    if clusterAllocMethod == 'weak':
        clusters_nodes = nx.weakly_connected_components(G)
    elif clusterAllocMethod == 'strong':
        clusters_nodes = nx.strongly_connected_components(G)

    if verbose:
        print "Getting clusters graphs..."

    clusters_subgraphs = [G.subgraph(nlist) for nlist in clusters_nodes]

    #Array to keep the clusters
    clusters = []

    #Iterate thru the clusters subgraphs
    for cluster_sg in clusters_subgraphs:

        #Calculate the rank for each node in the cluster
        if clusterRankMethod == 'pagerank':
            cluster_node_ranks = nx.pagerank(cluster_sg).items() #Pagerank
        elif clusterRankMethod == 'sum':
            cluster_node_ranks = in_degree_centrality(cluster_sg).items() #Incomming edges

        #Order cluster in decreasing order
        cluster_node_ranks = sorted(cluster_node_ranks, key=lambda a: a[1], reverse=True) 

        #Append the cluster to the clusters array with its length
        clusters.append((cluster_node_ranks, len(cluster_node_ranks)))

    #Order clusters in decreasing order
    clusters = sorted(clusters, key=lambda a: a[1], reverse=True) 

    return clusters



#--------------main()-----------------
# if __name__ == "__main__":
#     main(sys.argv)
    # print "Initing db..."

    # #Load database
    # py2neo.authenticate("localhost:7474", "neo4j", "lucas")
    # neo4jGraph = Graph("http://localhost:7474/db/data/")

    # #Default Configuration
    # articleTitle = "MQTT" #Article to generate graph from
    # transversalLevel = "1..3" #Graph transversal level 
    # deleteMainNode = True #Exclude the main node in the cluster computation
    # clusterAllocMethod = "weak" # 'weak' for weakly-connnected-components and 'strong' for strongly-connected-components
    # clusterRankMethod = "sum" #'sum' to simply sum incomming nodes and 'pagerank' to compute nodes pageranks
    # #betweenNodesConnections #TO BE IMPLEMENTED Whether to get connections between graph nodes or only their forward connections

    # #Replace configs
    # try: 
    #     articleTitle = sys.argv[1]
    # except: 
    #     pass

    # try:
    #     transversalLevel = sys.argv[2]
    # except: 
    #     pass

    # try:
    #     clusterAllocMethod = sys.argv[3]
    # except: 
    #     pass

    # try:
    #     clusterRankMethod = sys.argv[4]
    # except: 
    #     pass


    # clusters = getArticleClusters(articleTitle, transversalLevel, True, clusterAllocMethod, clusterRankMethod, neo4jGraph, True)


    # #String to store the result of the process
    # resultLog = ""

    # #Iterate thru clusters
    # for c in clusters:
    #     resultLog += "Cluster nodes: " + str(c[1]) + "\n\r"
    #     for node in c[0]:
    #         resultLog += str(node) + "\n\r"
    #     resultLog += "\n\r"

    # #Save result log with its properties
    # fileName = "-".join([articleTitle, transversalLevel, str(deleteMainNode), clusterAllocMethod, clusterRankMethod]) + ".txt"
    # with open("results/" + fileName, "w") as f:
    #     f.write(resultLog)
    # f.close()

    # print ""
    # print resultLog

    # # nx.draw(G)
    # # plt.show()