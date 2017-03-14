from transverse import connectDb, getGraph, getCentralNodes

import sys


def create_all_cons(args):
    """Func"""

    article_title = args[1]

    db_connection = connectDb()

    for transv in ["1..1", "1..2", "1..3"]:
        create_connections(article_title, transv, db_connection)

    print "DONE!\n"

def create_connections(article_title, transversal_level, db_connection):
    """Func"""

    graph = getGraph(article_title, transversal_level, db_connection)

    central_nodes = reversed(getCentralNodes(graph))

    for node in central_nodes:
        lead_node = node[0]
        #If is the same as article title, skip it
        if lead_node != article_title:
            break

    print ""
    print [lead_node]
    print ""

    print "Filling database..."

    #Create "requires" relation

    db_query = " ".join([
        'MATCH (n1:Article {name:"N1-TITLE"}), (n2:Article {name:"N2-TITLE"})',
        # 'WHERE NOT (n1)-[:Requires]-(n2)',
        'CREATE UNIQUE (n1)-[l:Requires{level:"TRANSV-LEVEL"}]->(n2)',
        'RETURN l'
    ]).replace("N1-TITLE", article_title).replace("N2-TITLE", lead_node).replace("TRANSV-LEVEL", transversal_level)

    print [db_query]

    #Execute query
    for r in db_connection.run(db_query):
        print r


if __name__ == "__main__":
    create_all_cons(sys.argv)
    
