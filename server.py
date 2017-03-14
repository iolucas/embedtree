import cherrypy
import os

from transverse import connectDb

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


class HelloWorld(object):

    @cherrypy.expose
    def index(self):
        """Func"""
        return open("public/index.html")

    @cherrypy.expose
    def map(self):
        """Func"""

        edges = get_map()

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

