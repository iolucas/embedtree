from transverse import connectDb, getGraph, getCentralNodes

import sys


def create_all_cons(args):
    """Func"""

    article_title = args[1]

    db_connection = connectDb()

    for transv in ["1..2"]:
        create_connections(article_title, transv, db_connection)

    print "DONE!\n"

def create_connections(article_title, transversal_level, db_connection):
    """Func"""

    graph = getGraph(article_title, transversal_level, db_connection)

    lead_nodes = []
    max_size = 5

    for node in reversed(getCentralNodes(graph)):
        #the index 0 is where the name string is, the index 1 is the score
        if node[0] == article_title:
            continue

        lead_nodes.append(node[0])

        if len(lead_nodes) == max_size:
            break

    print ""
    print lead_nodes
    print ""

    print "Creating query..."

    match_list = ['(n1:Article {name:"' + article_title +'"})']
    for i, node in enumerate(lead_nodes):
        true_index = str(i + 2)
        match_list.append('(n' + true_index + ':Article {name:"' + node +'"})')

    create_unique_list = []
    for i, node in enumerate(lead_nodes):
        true_index = str(i + 2)
        create_unique_list.append('(n1)-[:requisits{level:"' + transversal_level + '"}]->(n'+ true_index +')')

    #print create_unique_list

    match_query = "MATCH " + ",".join(match_list)
    create_query = "CREATE UNIQUE " + ",".join(create_unique_list)

    db_query = match_query + "\n" + create_query

    print db_query

    #Execute query
    for result in db_connection.run(db_query):
        print result

    # db_query_list = [
    #     'MATCH',
    #     '(n1:Article {name:"N1-TITLE"})'

    # ]

    # db_query = " ".join([
    #     'MATCH (n1:Article {name:"N1-TITLE"}), (n2:Article {name:"N2-TITLE"})',
    #     # 'WHERE NOT (n1)-[:Requires]-(n2)',
    #     'CREATE UNIQUE (n1)-[l:Requires{level:"TRANSV-LEVEL"}]->(n2)',
    #     'RETURN l'
    # ]).replace("N1-TITLE", article_title).replace("N2-TITLE", lead_node).replace("TRANSV-LEVEL", transversal_level)


    # print "Filling database..."

    # #Create "requires" relation



    # print [db_query]

    # #Execute query
    # for r in db_connection.run(db_query):
    #     print r


if __name__ == "__main__":
    create_all_cons(sys.argv)
    
