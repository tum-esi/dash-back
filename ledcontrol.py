import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

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



class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")    

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler),
	    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "templates"}),
	    #(r'/(templates/)', tornado.web.StaticFileHandler, {'path':'./'})
        ]
 
        settings = {
			'template_path': 'templates'
			"static_path": os.path.join(os.path.dirname('click.gif'), "templates")
			}
        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == '__main__':
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
