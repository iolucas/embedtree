import cherrypy
import os

from transverse import *

import json

def get_map():
    """Func"""

    db_connection = connectDb()

    db_query = "MATCH (:Article)-[r:requisits{level:'1..2'}]->(:Article) RETURN r"

    # db_query = " ".join([
    #     'MATCH (n1:Article {name:"ARTICLE-TITLE"})-[l1:RefersTo*TRANSVERSAL-LEVEL]->(n2:Article)',
    #     'RETURN l1'
    # ]).replace("ARTICLE-TITLE", article_title).replace("TRANSVERSAL-LEVEL", transversal_level)

    #Execute query and compute ids

    edges = []

    for result in db_connection.run(db_query):
        edge = result['r']
        edges.append((edge.start_node()['name'], edge.end_node()['name']))

    return edges

def get_k_most(db_connection, seed_node, k):
    
    article_title = seed_node
    transversal_level = "1..3" #For debug display scheme

    #db_connection = connectDb()

    graph = getGraph(article_title, transversal_level, db_connection)

    paths_probs = get_prereq_probs(graph, article_title, 3)

    sorted_data = sorted(paths_probs.iteritems(), key=lambda a: a[1][1], reverse=True)

    return sorted_data[:k]

class HelloWorld(object):

    def __init__(self):
        self.db_connection = connectDb()

    @cherrypy.expose
    def index(self, node):
        """Func"""
        return open("public/index.html")

    @cherrypy.expose
    def map(self):
        """Func"""

        edges = get_map()

        return json.dumps(edges)

    @cherrypy.expose
    def target_map(self, node):

        prereq_nodes = get_k_most(self.db_connection, node,5)

        edges = []

        for i, node in enumerate(prereq_nodes):
            if i == 0:
                continue
            edges.append((prereq_nodes[i-1][0], prereq_nodes[i][0]))

        return json.dumps(edges)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            #'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public/static'
        }
    }
    cherrypy.quickstart(HelloWorld(), '/', conf)

