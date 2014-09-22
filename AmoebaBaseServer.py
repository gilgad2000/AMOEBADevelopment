__author__ = 'Matt'


#from AmoebaFactory import *
#from twisted.internet import reactor
#import qt4reactor

class AmoebaBaseServer():
    def __init__(self,experiment):
        """
        This class handles the connection and communication with the Amoeba Servers.
        """
        AMOEBA_SERVER_INIT_DEBUG = 0
        if AMOEBA_SERVER_INIT_DEBUG:
            print "Amoeba Server"
        self.connected = 0
        #self.reactor = qt4reactor.QtReactor()
        #self.reactor = reactor
        #self.factory = AMOEBAFactory(experiment)
        #self.protocol = AMOEBAClient()

    def connect(self, ip, port):
        """
        This method connects to the server.
        :param ip: IP Address of the server.
        :param port: Port number.
        """
        AMOEBA_SERVER_CONNECT = 1
        if AMOEBA_SERVER_CONNECT:
            print "Create Socket."
        try:
            if AMOEBA_SERVER_CONNECT:
                 print "ip = ", ip
                 print "port = ", port
            #self.reactor.connectTCP(ip,port,self.factory)
            print "Connected."
            #  Run reactor at the end of the function call.
        except:
            print "ERROR:  Address or port number incorrect or already running"
            return "error"
        return "success"

    def runReactor(self):
        #self.reactor.run()
        x = 0

    def send(self,command_string):
        """
        This method sends a command string to the server.
        :param command_string:  Command you want to send to the server.
        :param data_string: The data to occupancy the command.
        """
        AMOEBA_SERVER_SEND_DEBUG = 1
        if AMOEBA_SERVER_SEND_DEBUG:
            print "Send data to the server."
            print "Sending to server = ", command_string
        #self.protocol.send(command_string)

    def disconnect(self):
        """
        This method handles disconnecting with the server.
        """
        AMOEBA_DISCONNECT_DEBUG = 1
        if AMOEBA_DISCONNECT_DEBUG:
            print "Disconnect from server."
        #self.protocol.disconnect()
        #self.reactor.stop()

    def connected(self):
        """
        This method checks to see if the client is connected to the server.
        """
        AMOEBA_SERVER_CONNECTED_DEBUG = 0
        if AMOEBA_SERVER_CONNECTED_DEBUG:
            print "Check to see if the server is connected."
        if self.connected:
            return "connected"
        else:
            return "not connected"