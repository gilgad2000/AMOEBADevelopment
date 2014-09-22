from AmoebaBaseServer import *

DEFAULT_PORT = 5005
BUFFER_SIZE = 4096



class AmoebaServer(AmoebaBaseServer):
    def __init__(self,experiment,parent=None):
        AMOEBA_SERVER_INIT=0
        if AMOEBA_SERVER_INIT:
            print "Initialising AMOEBA server."
        AmoebaBaseServer.__init__(self,experiment)
        self.experiment = experiment
        self.ip = '0.0.0.0'
        self.port = 0


    def timeOut(self):
        """
        This method is called if the socket times out.  Mostly to warn the user that it has happened.
        """
        print "Socket timed out."

    def requestData(self,command_string):
        """
        This method requests data from the server.
        :param command_string: The command string to retrieve the desired data from the server.
        :return: Data requested from the server.  Note this data will be stored in a string.
        """
        AMOEBA_SERVER_REQUEST_DATA_DEBUG = 0
        if AMOEBA_SERVER_REQUEST_DATA_DEBUG:
            print "Request Data from Server."
        #Send request.

    def checkReady(self, command_string, data_string_length):
        """
        This method checks to see if the server is ready to receive data.
        :param command_string: The command string to send to the server.
        :param data_string_length: Length of the data to send to the server.  NOTE:  The data must be sent as a string.
        :return: 0 for Success.
        """
        AMOEBA_CHECK_READY_DEBUG = 0
        if AMOEBA_CHECK_READY_DEBUG:
            print "Checking to see if server is ready to receive data."


    def receive(self):
        """
        The method handles receiving data.
        :return: The data received by the buffer.
        """
        AMOEBA_RECEIVE_DEBUG=0
        if AMOEBA_RECEIVE_DEBUG:
            print "Receive message."
        #  Retrieve the received data from the server and process the strings.


    def checkRunning(self):
        """
        This method checks to see if the experiment is still running.
        :return: A number depending on whether the experiment is running or not.  The number is defined in the hash
        defines above.
        """
        AMOEBA_CHECK_RUNNING_DEBUG = 0
        if AMOEBA_CHECK_RUNNING_DEBUG:
            print "Check running."


    def receiveLongString(self):
        """
        This method is used to receive a data string that may be very long.  It splits the data string up into several
        smaller strings.
        """
        AMOEBA_RECEIVE_LONG_STRING_DEBUG = 0
        if AMOEBA_RECEIVE_LONG_STRING_DEBUG:
            print "Receive long string."
