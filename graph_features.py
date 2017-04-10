"""
Library to compute diverse graph features.
"""

import networkx as nx #Lib to create and manipulate graphs


def in_degree(graph):
    """Function to compute the in degree (# of incoming edges over the total # of edges). """
    return nx.in_degree_centrality(graph)