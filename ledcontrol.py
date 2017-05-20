import os.path
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from scapy.all import *
import time


# setting constants
STATIC_DIR='static'
TEMPLATE_DIR='templates'
sub=0
mysum=0
a= [0] * 6
#start_time = time.time()

def arp_display(pkt):

    global a
    if pkt.haslayer(ARP):
        if pkt[ARP].op == 1:
            if pkt[ARP].hwsrc=='44:65:0d:4a:af:e2':
                print "pushed PLAY DOUGH dash button with a mac address of: " + pkt[ARP].hwsrc
                a[0] = 1
            if pkt[ARP].hwsrc=='ac:63:be:74:c1:3e':
                print "pushed PERCIL button with a mac address of: " + pkt[ARP].hwsrc
                a[1] = 1
            if pkt[ARP].hwsrc=='50:f5:da:f7:08:10':
                print "pushed SHWARZKOPF button with a mac address of: " + pkt[ARP].hwsrc
                a[2] = 1
            if pkt[ARP].hwsrc=='ac:63:be:a3:57:96':
                print "pushed NOBO button with a mac address of: " + pkt[ARP].hwsrc
                a[3] = 1
            if pkt[ARP].hwsrc=='ac:63:be:95:f8:ad':
                print "pushed BARBANTIA button with a mac address of: " + pkt[ARP].hwsrc
                a[4] = 1
            if pkt[ARP].hwsrc=='ac:63:be:c7:79:63':
                print "pushed CESAR button with a mac address of: " + pkt[ARP].hwsrc
                a[5] = 1

    return


# our websocket handler
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print "Connection Opened"
        self.write_message("Connection Opened")
    def on_close(self):
        print "Connection Closed"

    def on_message(self, message):
        print "Message received: {}".format(message)
        #self.write_message("Message recieved:")
        if message == "ledon":
            global a
            subtracted=0
            mysum=0
            #self.write_message("script is started")
            print sniff(prn=arp_display, filter="arp", store=0, count=0, timeout=20)
            #self.write_message("script is ended")
            for element in a:
                mysum += element
            print mysum
            subtracted= 6-mysum
            print subtracted
            self.write_message("1")
            a= [0] * 6
        if message == "Yes Button":
            global mysum
            self.write_message(str(mysum))
        if message == "No Button":
            global subtracted
            self.write_message(str(subtracted))

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


