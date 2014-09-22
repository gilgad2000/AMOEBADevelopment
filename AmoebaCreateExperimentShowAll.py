#import socket
#import sys
import os
import fnmatch
import Amoeba
#from PySide.QtCore import *
from PySide.QtGui import *
from AmoebaSensor import *
from Amoeba import *

AMOEBA_CREATE_EXPERIMENT_DEBUG = 0
AMOEBA_CREATE_SELECT_UI_DEBUG=0

class AmoebaShowAllInstuments(QWidget):
    def __init__(self,parent=None):
        """
        This function creates the widget which displays all available AMOEBA modules for an experiment.  It reads them
        in from the XML files in the instruments directory.
        :param parent:
        """
        QWidget.__init__(self, parent)
        instruments = []
        self.selectWidgets = []
        selectWidgetsLayout = QVBoxLayout()

        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
            print "Create Instrument Window"
            print "Show Window."
            
        #Retreive all the instruments from the instruments folder.
        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
            print Amoeba.INSTRUMENT_FOLDER
            
        filelist = os.listdir(INSTRUMENT_FOLDER)
        
        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
            print filelist

        for i in os.listdir(INSTRUMENT_FOLDER):
            if fnmatch.fnmatch(i, '*.xml'):
                sensor = Amoeba_sensor()
                
                if AMOEBA_CREATE_EXPERIMENT_DEBUG:
                    print i + "\n"
                    
                sensor.read_in_from_XML((INSTRUMENT_FOLDER + i))
                
                if AMOEBA_CREATE_EXPERIMENT_DEBUG:
                    print "Instrument read in from file:"
                    sensor.print_command()
                    print "\n"
                    
                instruments.append(sensor)

        #Import the instruments.
        for i in instruments:
            
            if AMOEBA_CREATE_EXPERIMENT_DEBUG:
                print "Create widgets. For:"
                i.print_command()
                
            selectWidget = SelectInstruments(i)
            self.selectWidgets.append(selectWidget)
            selectWidgetsLayout.addWidget(selectWidget.return_widget())

        #Set Layout
        self.setLayout(selectWidgetsLayout)

    def retrieve_selected(self):
        """
        This function retrieves the AMOEBA modules selected by the user.
        :return: A list of the chosen instruments.
        """
        chosen_instruments = []
        for i in self.selectWidgets:
            if i.selected.checkState():
                if AMOEBA_CREATE_EXPERIMENT_DEBUG: 
                    print "Chosen Instrument"
                    i.instrument.print_command()
                chosen_instruments.append(i.instrument)
        return chosen_instruments


class SelectInstruments():
    def __init__(self,instrument):
        """
        This class creates the UI for selecting that instruments.
        :param instrument: The instrument the UI is to be created for.
        """
        self.instrument = instrument

        if AMOEBA_CREATE_SELECT_UI_DEBUG:
            print "Create selection widgets for each instrument."
            instrument.print_command()
            
        #Create the widgets for the UI.
        #self.box = QGroupBox(instrument.name)
        self.num_sensors = QLabel("Number of sensors: " + str(instrument.number_of_parameters))
        self.sensor_name = QLabel("Sensor name: " + instrument.name)
        self.sensor_type = QLabel("Sensor type: " + instrument.type)
        self.sensor_description = QLabel("Description: " + instrument.description)
        self.selected = QCheckBox("Use sensor.")
        
        #Put widgets into layouts.
        layoutA = QHBoxLayout()
        mainlayout = QVBoxLayout()
        layoutA.addWidget(self.num_sensors)
        mainlayout.addLayout(layoutA)
        mainlayout.addWidget(self.sensor_type)
        mainlayout.addWidget(self.sensor_description)
        mainlayout.addWidget(self.selected)
        
        if AMOEBA_CREATE_SELECT_UI_DEBUG:
            print "Selection Widgets created."

        #Set up ordering of boxes
        self.groupbox=QGroupBox(instrument.name)
        self.groupbox.setLayout(mainlayout)

    def return_widget(self):
        """
        THis returns the widgets which indicates whether the user has selected the module or not.
        Since returning to this function I have realised that I have done this in a retarded way.  What it should do is
        return the state of the box.  Will change when I have time.
        :return:
        """
        return self.groupbox
