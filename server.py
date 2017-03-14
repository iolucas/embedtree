import cherrypy
import os

class HelloWorld(object):

    @cherrypy.expose
    def index(self):
        return open("public/index.html")


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
