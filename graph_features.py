"""
Library to compute diverse graph features.
"""

import networkx as nx #Lib to create and manipulate graphs


def in_degree(graph):
    """Function to compute the in degree (# of incoming edges over the total # of edges). """
    return nx.in_degree_centrality(graph)

def pagerank(graph):
    """Function to compute pagerank of graph nodes."""
    return nx.pagerank(graph)

def extract_path_tuples(path):
    """Function that generates all path tuples from a list path."""
    path_tuples = []
    for i, _ in enumerate(path):
        if i == 0:
            continue
        path_tuples.append((path[i-1], path[i]))

    return path_tuples

def get_features(graph, seed_node, cutoff):
    """
    Function to compute the prereq probabilities for every node.
    Compute deeprank and bidirection rank. TO BE EXPLAINED

    Returns: bidir_probs, deeprank_probs, n_paths, min_depths, max_depths

    """

    #Compute number of edges per node
    nodes_edges = dict()
    for n1, n2 in graph.edges():
        #init nodes dict if not initiated
        if not nodes_edges.has_key(n1):
            nodes_edges[n1] = 0
        nodes_edges[n1] += 1

    #Compute initial edges probabilities
    #For bidirection rank we set 1 in case the edge is unidirectional and 0.5 in case bidirectional.
    #For deeprank we compute the fraction of the edge over all the edges in the same node.

    ### Later we need to create other methods to compute proper distribution for the cases above. ### 

    bidir_edges_values = dict()
    deeprank_edges_values = dict()

    #edges_values = dict()
    for n1, n2 in graph.edges():
        deeprank_edges_values[(n1, n2)] = 1.0 / nodes_edges[n1]
        
        if graph.has_edge(n2, n1):
            bidir_edges_values[(n1, n2)] = 0.5
        else:
            bidir_edges_values[(n1, n2)] = 1


    #Now compute all the paths to the target seed_node and sequence probabilities to each path
    bidir_probs = dict() #Probabilities of reach seed_node from each node based on bidir values
    deeprank_probs = dict() #Probabilities of reach seed_node from each node based on deeprank values
    min_depths = dict() #Each node min depth
    max_depths = dict() #Each node max depth
    ns_paths = dict() #Each node number of paths

    # create dicts for every feature extracted
    # try get insights from kmeans
    # try to find something to deploy FAST (the energy applied must be low!)

    n_nodes = nx.number_of_nodes(graph)

    #Iterate thru all the graph nodes
    for i, node in enumerate(graph.nodes()):

        print "Working on node ", i+1, "/", n_nodes

        #Init min max depth
        min_depth = cutoff + 2
        max_depth = 0

        #Skip seed_node since we do not want verify paths to itself
        if node == seed_node:
            continue

        n_paths = 0
        total_bidir_prob = 0
        total_deeprank_prob = 0

        for path in nx.all_simple_paths(graph, source=seed_node, target=node, cutoff=cutoff):

            n_paths += 1
            partial_bidir_prob = 1.0
            partial_deeprank_prob = 1.0

            #Computes min-max depth
            max_depth = max(max_depth, len(path))
            min_depth = min(min_depth, len(path))

            #Iterate the path tuples
            for i, edge_tuple in enumerate(extract_path_tuples(path)):
                partial_bidir_prob *= bidir_edges_values[edge_tuple]
                partial_deeprank_prob *= deeprank_edges_values[edge_tuple]

            total_bidir_prob += partial_bidir_prob
            total_deeprank_prob += partial_deeprank_prob

        #After processing all node paths, save the final values    
        bidir_probs[node] = total_bidir_prob / n_paths
        deeprank_probs[node] = total_deeprank_prob
        min_depths[node] = min_depth
        max_depths[node] = max_depth
        ns_paths[node] = n_paths 

    return bidir_probs, deeprank_probs, ns_paths, min_depths, max_depths