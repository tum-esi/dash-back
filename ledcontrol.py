#import logging
import os.path
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
#import uuid
#from tornado.options import define, options


# setting constants
STATIC_DIR='static'
TEMPLATE_DIR='templates'



# our websocket handler
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print "Connection Opened"
        self.write_message("Connection Opened")
    def on_close(self):
        print "Connection Closed"

    def on_message(self, message):
        print "Message received: {}".format(message)
        self.write_message("Message recieved:")
        if message == "ledon":
            self.write_message("script is started")
            os.system('python script.py')
            self.write_message("script is ended")
        else: 
            self.write_message("insan ka bacha ban")


# our index page handler
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")



# tornado global configuration of handlers and settings
class Application(tornado.web.Application):
    def __init__(self):

        # declare application handlers
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler),
            #(r'/static/(.*)', tornado.web.StaticFileHandler, {'path':'./static', 'default_filename': 'index.html'})
        ]

        # declare application settings
        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), STATIC_DIR),
            'template_path': os.path.join(os.path.dirname(__file__), TEMPLATE_DIR),
		}

        # register handlers and settings on application
        tornado.web.Application.__init__(self, handlers, **settings)



# python main entry
if __name__ == '__main__':

    # instantiate tornado application
    app = Application()

    # instantiate tornado web server
    server = tornado.httpserver.HTTPServer(app)

    # open socket for incoming requests
    server.listen(8000)

    # run endless loop to serve requests
    tornado.ioloop.IOLoop.instance().start()


