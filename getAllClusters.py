import sys

from transverse import getArticleClusters

import py2neo
from py2neo import Graph

#Load database
print "Initing db..."
py2neo.authenticate("localhost:7474", "neo4j", "lucas")
neo4jGraph = Graph("http://localhost:7474/db/data/")

queryParams = [
    [sys.argv[1], "1..1", "weak", "sum"],
    [sys.argv[1], "1..1", "weak", "pagerank"],
    [sys.argv[1], "1..1", "strong", "sum"],
    [sys.argv[1], "1..1", "strong", "pagerank"],

    [sys.argv[1], "1..2", "weak", "sum"],
    [sys.argv[1], "1..2", "weak", "pagerank"],
    [sys.argv[1], "1..2", "strong", "sum"],
    [sys.argv[1], "1..2", "strong", "pagerank"],  

    [sys.argv[1], "1..3", "weak", "sum"],
    [sys.argv[1], "1..3", "weak", "pagerank"],
    [sys.argv[1], "1..3", "strong", "sum"],
    [sys.argv[1], "1..3", "strong", "pagerank"]   
]

for p in queryParams:
    print "Getting clusters for " + str(p) + "..."

    clusters = getArticleClusters(p[0], p[1], True, p[2], p[3], neo4jGraph, True)

    #String to store the result of the process
    resultLog = ""

    print "Creating log..."
    #Iterate thru clusters
    for c in clusters:
        resultLog += "Cluster nodes: " + str(c[1]) + "\n\r"
        for node in c[0]:
            resultLog += str(node) + "\n\r"
        resultLog += "\n\r"

    print "Saving log..."
    #Save result log with its properties
    fileName = "-".join([p[0], p[1], "True", p[2], p[3]]) + ".txt"
    with open("results/" + fileName, "w") as f:
        f.write(resultLog)
    f.close()

print "Done"
