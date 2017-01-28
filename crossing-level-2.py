import sys

import py2neo
from py2neo import Graph

import networkx as nx

import matplotlib.pyplot as plt

#Load database
py2neo.authenticate("localhost:7474", "neo4j", "lucas")
graph = Graph("http://localhost:7474/db/data/")

articleTitle = sys.argv[1]

#Construct the query
dbQuery = " ".join([
    # 'MATCH (n:Article {title:"ARTICLE-TITLE"})-[l:ConnectsTo]->(n1:Article)-[l1:ConnectsTo*1..2]->(n2:Article)',
    'MATCH (n1:Article {title:"ARTICLE-TITLE"})-[l1:ConnectsTo*1..3]->(n2:Article)',
    # 'OPTIONAL MATCH (n2)-[l2:ConnectsTo]->(n3:Article)',
    # 'WHERE (n1)-[:ConnectsTo]->(n3)',
    # 'WHERE n1 <> n2',
    # 'WHERE (n <> n1 AND n <> n2)',
    'RETURN n1,l1,n2'
]).replace("ARTICLE-TITLE", articleTitle)

#Create a directed graph

G = nx.DiGraph()

#Execute query 
#iterate over the results
#And add edges
for r in graph.run(dbQuery):
    for e in r['l1']:
        G.add_edge(e.start_node()['title'], e.end_node()['title'])
        # print (e.start_node()['title'], e.end_node()['title'])


print "\n".join(map(str, sorted(nx.pagerank(G).items(), key=lambda a: a[1], reverse=True))) #Pagerank

# for comp in nx.weakly_connected_components(G):
#     print comp

# for e in G.edges():
#     print e


# nx.draw(G)
# plt.show()