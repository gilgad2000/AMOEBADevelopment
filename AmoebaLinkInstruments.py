import socket
import sys
import os
import fnmatch
import Amoeba
from PySide.QtCore import *
from PySide.QtGui import *
from AmoebaSensor import *
from Amoeba import *
import xml.etree.ElementTree as ET

AMOEBA_LINK_SELECTED_UI_DEBUG=0

AMOEBA_INSTRUMENT_LINK_DEBUG=0

class LinkInstrumentsForm(QWidget):
    def __init__(self,parent=None):
        """
        The LinkInstrumentsForm class is the UI used in the AmoebaCreateExperiment class to link the instruments which
        have been chosen in the previous sections.
        :param parent: Parent of this class.
        """
        QWidget.__init__(self, parent)
        if AMOEBA_LINK_SELECTED_UI_DEBUG:
            print "Link instruments."
        self.widgets = []

    def setInstruments(self,instruments):
        """
        This function selects the instruments to add to the linker widget.
        :param instruments: This is a list of chosen instruments.
        """
        self.instruments = instruments
        self.linkLayout = QVBoxLayout()
        #Create a widget for each sensor.
        for i in self.instruments:
            if i.type == "control":
                widget = LinkInstrumentWidget(i,instruments)
                self.linkLayout.addWidget(widget)
                self.widgets.append(widget)
        self.setLayout(self.linkLayout)

    def getLinksandControl(self):
        """
        This function returns the instrument links from the options that the user has selected.
        :return: Instrument links.  Proceed 0 if all the forms are correctly filled out, if not then a number other than
        0 is returned.
        """
        links = []
        controls = []
        proceed = 0
        if AMOEBA_LINK_SELECTED_UI_DEBUG:
            print "Link instruments."
            print self.widgets
        for i in self.widgets:
            if AMOEBA_LINK_SELECTED_UI_DEBUG:
                print i.getLink()
            link, control, proceedable  = i.getLink()
            print "Initial bit getLinksandControl links: " + str(len(link)) + " control: " + str(len(control))
            for j in link:
                if j.channel!=-1:
                    links.append(j)
            for j in control:
                if j.channel!=-1:
                    controls.append(j)
            proceed = proceed + proceedable
        if AMOEBA_LINK_SELECTED_UI_DEBUG:
            print "Links:"
            for i in links:
                i.print_links()
        print "getLinksandControl Length of links: " + str(len(links)) + " controls: " + str(len(controls))
        return links, controls, proceed

    def checkProceed(self):
        return 1
        

class LinkInstrumentWidget(QWidget):
    def __init__(self,instrument,instruments,parent=None):
        """
        This class is the link selector widget.
        :param instrument: The instrument that the user has is going to control
        :param instruments: The parameter contains all the controls that the user has selected to use.
        :param parent: Parent.
        """
        QWidget.__init__(self, parent)
        if AMOEBA_LINK_SELECTED_UI_DEBUG:
            print "Link instruments."
        #Set instrument
        self.instrument = instrument

        self.links = []
        self.box = QGroupBox(instrument.name)

        #Setup the layouts
        widgetLayout = QVBoxLayout()
        boxLayout = QVBoxLayout()

        for i in self.instrument.parameters:
            #Ceate the widgets.
            self.linkOptions = AmoebaSensorSelect(instruments,i,instrument)
            
            self.links.append(self.linkOptions)
            #Add the items to the layout
            boxLayout.addWidget(self.linkOptions)
            self.box.setLayout(boxLayout)
            widgetLayout.addWidget(self.box)
            self.setLayout(widgetLayout)

    def getLink(self):
        """
        This method returns the link from the data the user has entered into the form.
        :return:  links = The chosen link.  proceed = If enough data has been entered correctly then this will be 0.
        """
        proceed = 0
        links = []
        controls = []
        for i in self.links:
            #  If islnk is True then it's a link, otherwise it's a control.
            link, tmpproceed, islnk = i.getState()
            proceed = proceed + tmpproceed
            if islnk == True:
                links.append(link)
            else:
                controls.append(link)
        print "getLink   Links: " + str(len(links)) + " Controls: " + str(len(controls))
        return links, controls, proceed
            
class AmoebaSensorSelect(QWidget):
    def __init__(self,instruments,parameter,instrument):
        """
        This class is for the dynamic instrument selector which selects bother the parameter which controls
        :param instruments: The controllers from which it can choose.
        :param parameter: The parameter of the sensor which the controller will control.
        :param instrument: The sensor instrument for which the controllers are being selected.
        """
        QWidget.__init__(self, parent=None)
        if AMOEBA_LINK_SELECTED_UI_DEBUG:
            print "Link instruments."

        self.parameter = parameter
        self.controller_address = instrument.address
        self.controller_name = instrument.name

        mainLayout = QVBoxLayout()
        selectSensorLayout = QVBoxLayout()
        selectSensorChannelLayout = QVBoxLayout()
        setValueLayout = QHBoxLayout()
        setBoundariesLayout = QHBoxLayout()
        layoutA = QHBoxLayout()
        
        self.instruments = instruments

        #Create Combo box
        self.selectsensor = QComboBox()
        self.selectsensor.addItem("Measure Only")
        self.selectsensor.addItem("Set Constant Output")
        #Link value change to a function.
        self.selectsensor.currentIndexChanged.connect(self.dynamicChanelSelect)

        self.selectsensorchannel = QComboBox()
        self.selectsensorchannel.addItem("N.A.")

        #Create Controller Menu contents.
        for i in instruments:
            #if i.type == "control":
            if i.type == "sensor":
                if AMOEBA_LINK_SELECTED_UI_DEBUG:
                    print "Add item to combo box."
                self.selectsensor.addItem(i.name)

        #Create the box labels
        selectSensorLabel = QLabel("Select Sensor")
        selectSensorChannelLabel = QLabel("Select Channel")
        setValueLabel = QLabel("Set Value")
        setBoundaries = QLabel("Set boundaries +/-")
        
        #Create the widgets
        self.setValue = QLineEdit()
        self.setInverse = QCheckBox("Negative Control",self)
        self.setBoundaries = QLineEdit()

        #Add Put the items into the layouts.
        selectSensorLayout.addWidget(selectSensorLabel)
        selectSensorLayout.addWidget(self.selectsensor)

        selectSensorChannelLayout.addWidget(selectSensorChannelLabel)
        selectSensorChannelLayout.addWidget(self.selectsensorchannel)

        setValueLayout.addWidget(setValueLabel)
        setValueLayout.addWidget(self.setValue)

        setBoundariesLayout.addWidget(setBoundaries)
        setBoundariesLayout.addWidget(self.setBoundaries)
        
        mainLayout.addLayout(selectSensorLayout)
        mainLayout.addLayout(selectSensorChannelLayout)

        mainLayout.addLayout(layoutA)
        mainLayout.addLayout(setValueLayout)
        mainLayout.addWidget(self.setInverse)
        mainLayout.addLayout(setBoundariesLayout)
        
        self.setLayout(mainLayout)

    def dynamicChanelSelect(self):
        """
        This method modifies the contents of the selectcontrolchannel widget to contain to be inline with the
         instrument selected in selectcontroller widget.
        """
        if AMOEBA_LINK_SELECTED_UI_DEBUG:
            print "Dynamic Channel Select."
        currenttext = self.selectsensor.currentText()
        if AMOEBA_LINK_SELECTED_UI_DEBUG:
            print "Selected object = " + currenttext
            print "Count = " + str(self.selectsensorchannel.count())
        count = self.selectsensorchannel.count()
        # Remove current items.
        while count!=0:
            count = count - 1
            self.selectsensorchannel.removeItem(count)
        # Add new ones.
        count = 0
        # Find the newly selected option
        for i in self.instruments:
            if currenttext == i.name:
                instrument = i
        if AMOEBA_LINK_SELECTED_UI_DEBUG:
            print instrument.name
            print instrument.number_of_parameters
        # Add channel numbers to the combo box.
        if currenttext != "Measure Only" and  currenttext != "Set Constant Output":
            self.setBoundaries.setEnabled(True)
            while count != instrument.number_of_parameters:
                self.selectsensorchannel.addItem(str(count))
                count = count + 1
        else:
            self.selectsensorchannel.addItem("N.A.")
            if currenttext == "Set Constant Output":
                self.setBoundaries.setEnabled(False)
            else:
                self.setBoundaries.setEnabled(True)
    
    def checkProceed(self):
        """
        I'm not sure what this does, even if it is used.  I don't want to delete it at the moment incase it is used
        somewhere and I don't discover it for a while.
        :return:
        """
        return 0

    def getState(self):
        """
        This function gets the state of the selectcontroller and the selectcontrollerchannel widgets.  It then uses
        this data to create an AmoebaInstrumentLink class for the link.
        :return: link = AmoebaInstrumentLink class containing the desired link between sensor and controller.  proceed
        if 0 then all the correct options have been chosen by the user, if not then the user will be prompted to check
        the data which they have entered.
        """
        proceed = 0
        islnk = False
        proceed = self.checkProceed()
        if self.selectsensor.currentText()!="Set Constant Output":
            element = AmoebaInstrumentLink()
            #Retrieve information about the controller.
            if self.selectsensorchannel.currentText()!="N.A.":
                element.channel = int(self.selectsensorchannel.currentText())
                print self.selectsensorchannel.currentText()
                for i in self.instruments:
                    if AMOEBA_LINK_SELECTED_UI_DEBUG:
                        print "?????????????????????????????????"
                        print i.print_command()
                        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    if i.name==self.selectsensor.currentText():
                        element.sensoraddress = i.address
                        element.sensorchannel = int(self.selectsensorchannel.currentText())
                tmp = self.setValue.text()
                if tmp != "":
                    element.value = float(tmp)
                else:
                    proceed = 1
                tmp = self.setBoundaries.text()
                #Retrieve data about the controller.
                element.channel = int(self.parameter.number)
                element.sensor = self.selectsensor.currentText()
                element.controlleraddress = self.controller_address
                element.controller = self.controller_name
                print self.setInverse.checkState()
                if self.setInverse.isChecked():
                    element.inversly_proportional = 1
                else:
                    element.inversly_proportional = 0
                islnk = True
                if tmp !="":
                    element.boundaries = float(tmp)
                else:
                    proceed = 1
            else:
                element.channel = -1
            if AMOEBA_LINK_SELECTED_UI_DEBUG:
                self.parameter.print_parameter()
                print self.parameter.number
                element.print_links()
                print "Proceed = " + str(proceed)
        else:
            #  Read it as a control parameter.
            element = AmoebaCommandController()
            element.value = float(self.setValue.text())
            element.channel = int(self.parameter.number)
            element.address = self.controller_address
            element.print_command_value()
            islnk = False
        return element, proceed, islnk

class AmoebaInstrumentLink():
    def __init__(self):
        """
        This class stores the links between sensors and controller.
        """
        self.sensoraddress = 0
        self.controller = ""
        self.value = 0.0
        self.channel = -1
        self.sensorchannel = -1
        self.inversly_proportional=0
        self.boundaries = 0.1
        self.controlleraddress = 0

    def print_links(self):
        """
        This method prints out the link to the terminal.
        """
        print "Link:"
        print "Sensor address = " + str(self.sensoraddress)
        print "Controller address = " + str(self.controlleraddress)
        print "Controller = " + str(self.controller)
        print "Value = " + str(self.value)
        print "Channel = " + str(self.channel)
        print "Sensor Channel = " + str(self.sensorchannel)
        print "Boundaries = " + str(self.boundaries)

    def __str__(self):
        string = "Link:\n"
        string = string + "Sensor address = " + str(self.sensoraddress) + "\n"
        string = string + "Controller address = " + str(self.controlleraddress) + "\n"
        string = string + "Controller = " + str(self.controller) + "\n"
        string = string + "Value = " + str(self.value) + "\n"
        string = string + "Channel = " + str(self.channel) + "\n"
        string = string + "Sensor Channel = " + str(self.sensorchannel) + "\n"
        string = string + "Boundaries = " + str(self.boundaries) + "\n"
        string = string + "Inverse = " + str(self.inversly_proportional)
        return string

    def writeXMLElement(self,link):
        """
        This method writes a link to an element for an elementTree.
        :param link: This should be a link element for an elementTree.
        :return:  Returns the link as an element
        """
        if AMOEBA_INSTRUMENT_LINK_DEBUG:
            print "Writing xml."
        link.attrib['sensor_address']=str(self.sensoraddress)
        link.attrib['controller_address']=str(self.controlleraddress)
        link.attrib['controller']=str(self.controller)
        link.attrib['value']=str(self.value)
        link.attrib['channel']=str(self.channel)
        link.attrib['sensor_channel']=str(self.sensorchannel)
        link.attrib['boundaries']=str(self.boundaries)
        link.attrib['inverse']=str(self.inversly_proportional)
        return link

    def importFromTree(self,treeElement):
        """
        Import a link from a tree.
        """
        self.boundaries = float(treeElement.attrib.get("boundaries"))
        self.channel = int(treeElement.attrib.get("channel"))
        self.controller = treeElement.attrib.get("controller")
        self.controlleraddress = int(treeElement.attrib.get("controller_address"))
        self.inversly_proportional = int(treeElement.attrib.get("inverse"))
        self.sensoraddress = int(treeElement.attrib.get("sensor_address"))
        self.sensorchannel = int(treeElement.attrib.get("sensor_channel"))
        self.value = float(treeElement.attrib.get("value"))

class AmoebaCommandController():
    def __init__(self):
        print "Set Controller Value."
        self.address = -1
        self.channel = -1
        self.value = -1

    def print_command_value(self):
        print "Command"
        print "Controller address = " + str(self.address)
        print "Controller channel = " + str(self.channel)
        print "Value = " + str(self.value)

    def __str__(self):
        string = "Command \n"
        string = string + "Controller address = " + str(self.address) + "\n"
        string = string + "Controller channel = " + str(self.channel) + "\n"
        string = string + "Value = " + str(self.value) + "\n"
        return string

    def writeXMLElement(self,element):
        element.attrib['controller_address'] = str(self.address)
        element.attrib['controller_channel'] = str(self.channel)
        element.attrib['value'] = str(self.value)

    def importFromTree(self,treeElement):
        self.channel = int(treeElement.attrib.get("controller_channel"))
        self.address = int(treeElement.attrib.get("controller_address"))
        self.value = float(treeElement.attrib.get("value"))
