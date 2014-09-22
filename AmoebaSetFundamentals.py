import socket
import sys
import os
import fnmatch
import Amoeba
from PySide.QtCore import *
from PySide.QtGui import *
import xml.etree.ElementTree as ET

AMOEBA_SET_FUNDAMENTALS_DEBUG=1

class AmoebaSetFundamentalParameters(QWidget):
    def __init__(self):
        """
        This class is used to create and experiment.  It creates the UI which sets the fundamental parameters for the
        experiment.

        """
        super(AmoebaSetFundamentalParameters,self).__init__()

        #Create layouts.
        layoutA = QHBoxLayout()
        layoutB = QHBoxLayout()
        mainLayout = QVBoxLayout()

        readingTime = ["0.1s","0.2s","0.25s","0.5s","0.75s","1s"]
        self.readingTimeInt = [0.1,0.2,0.25,0.5,0.75,1]

        syncTime = ["1s","5s","10s","20s","30s","1 min","10 min"]
        self.syncTimeInt = [1,5,10,20,30,60,600]

        #Create widgets.
        readingLabel = QLabel("Measurement frequency:")
        syncLabel = QLabel("Update client every:")
        nameLabel = QLabel("Experiment Name:")
        descriptionLabel = QLabel("Experiment Description:")

        self.selectReadingTime = QComboBox()
        self.selectSyncTime = QComboBox()
        self.selectExperimentName = QLineEdit()
        self.selectExperimentDescription = QLineEdit()
        
        for i in readingTime:
            self.selectReadingTime.addItem(i)

        for i in syncTime:
            self.selectSyncTime.addItem(i)

        #Add Widgets to Layout

        mainLayout.addWidget(nameLabel)
        mainLayout.addWidget(self.selectExperimentName)

        mainLayout.addWidget(descriptionLabel)
        mainLayout.addWidget(self.selectExperimentDescription)

        layoutA.addWidget(readingLabel)
        layoutA.addWidget(self.selectReadingTime)

        layoutB.addWidget(syncLabel)
        layoutB.addWidget(self.selectSyncTime)

        mainLayout.addLayout(layoutA)
        mainLayout.addLayout(layoutB)

        self.setLayout(mainLayout)

    def getState(self):
        """
        This method creates an ExperimentFundamentals class from the options the user has selected.
        :return:
        """
        fundamentals = ExperimentFundamentals()
        #Retrieve fundamentals
        temp = self.selectSyncTime.currentIndex()
        fundamentals.sync = self.syncTimeInt[temp]
        temp = self.selectReadingTime.currentIndex()
        fundamentals.reading = self.readingTimeInt[temp]
        fundamentals.name = self.selectExperimentName.text()
        fundamentals.description = self.selectExperimentDescription.text()
        return fundamentals

class ExperimentFundamentals():
    def __init__(self):
        """
        This class stores the fundamentals of an Amoeba_Experiment.
        """
        self.sync = 0
        self.reading = 0
        self.name = ""
        self.description = ""

    def printFundamentals(self):
        """
        This method prints out the ExperimentFundamentals class.
        """
        print "Sync = " + str(self.sync)
        print "Reading = " + str(self.reading)
        print "Name = " + str(self.name)
        print "Description = " + str(self.description)

    def createTree(self,root):
        """
        This method creates and AmoebaExperiment Tree root using the ExperimentFundamentals class.
        :param root: Root of an Amoeba_Experiment elementTree.
        :return: The root of the tree.
        """
        if AMOEBA_SET_FUNDAMENTALS_DEBUG:
            print "Experiment fundamentals, Write to XML."
        #Create the element tree.
        root.attrib['name']=str(self.name)
        root.attrib['reading']=str(self.reading)
        root.attrib['sync']=str(self.sync)
        return root
