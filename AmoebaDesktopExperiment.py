#import Amoeba
#import sys
#import xml.etree.ElementTree as ET
#import string
#import AmoebaSensor
#import datetime
from Amoeba import *
from AmoebaImportExperiment import *

AMOEBA_PI_EXPERIMENT_DEBUG=0

class Amoeba_desktop_experiment(Amoeba_experiment):
    def __init__(self,desktopUI,parent=None):
        """
        This class inherits from the generic experiment file.  It allows extra_functionality to be added the the
        experiment class which is specific only to the desktop client.  A similar version exists on the server.
        :param desktopUI:
        :param parent:
        """
        Amoeba_experiment.__init__(self)
        self.UI = desktopUI

    def make_gui(self):
        """
        This calls a function which makes a GUI for the experiment.
        """
        self.UI.make_gui(self)

    def update(self):
        """
        This function updates the UI according to the experiment.
        """
        self.UI.update()

    def processServerResponse(self,string):
        AMOEBA_PROCESS_SERVER_RESPONSE_DEBUG=0
        if AMOEBA_PROCESS_SERVER_RESPONSE_DEBUG:
            print "Response from server."


    def processUpdateFromServer(self):
        AMOEBA_PROCESS_UPDATE_FROM_SERVER=0
        if AMOEBA_PROCESS_UPDATE_FROM_SERVER:
            print "Process update form serer."

    def processStart(self):
        AMOEBA_PROCESS_START = 0
        if AMOEBA_PROCESS_START:
            print "Experiment started."

    def processStop(self):
        AMOEBA_PROCESS_STOP = 0
        if AMOEBA_PROCESS_STOP:
            print "Experiment started."

    def processExperimentRunning(self):
        AMOEBA_PROCESS_EXPERIMENT_RUNNING = 0
        if AMOEBA_PROCESS_EXPERIMENT_RUNNING:
            print "Experiment started."

    def processReceiveExperiment(self):
        AMOEBA_PROCESS_RECEIVE_EXPERIMENT = 0
        if AMOEBA_PROCESS_RECEIVE_EXPERIMENT:
            print "Experiment received."

    def processRequestExperiment(self):
        AMOEBA_PROCESS_REQUEST_EXPERIMENT = 0
        if AMOEBA_PROCESS_REQUEST_EXPERIMENT:
            print "Request experiment received."
