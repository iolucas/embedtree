import sys

from transverse import getArticleClusters

import py2neo
from py2neo import Graph

#Load database
print "Initing db..."
py2neo.authenticate("localhost:7474", "neo4j", "lucas")
neo4jGraph = Graph("http://localhost:7474/db/data/")

articleTitle = sys.argv[1]

clusters = getArticleClusters(articleTitle, "1..3", True, "weak", "sum", neo4jGraph, True)

leadNode = clusters[0][0][0][0]

print ""
print leadNode
print ""

print "Filling database..."

#Create "requires" relation

dbQuery = " ".join([
    'MATCH (n1:Article {title:"N1-TITLE"}), (n2:Article {title:"N2-TITLE"})',
    # 'WHERE NOT (n1)-[:Requires]-(n2)',
    'CREATE UNIQUE (n1)-[l:Requires{level:TRANSV-LEVEL}]->(n2)',
    'RETURN l'
]).replace("N1-TITLE", articleTitle).replace("N2-TITLE", leadNode).replace("TRANSV-LEVEL", "3")

#Execute query
for r in neo4jGraph.run(dbQuery):
    print r