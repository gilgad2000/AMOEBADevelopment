import Amoeba
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import string
import AmoebaSensor
import datetime
from Amoeba import *
from AmoebaLinkInstruments import *

from AmoebaSetFundamentals import *
from PySide.QtGui import *

AMOEBA_EXPERIMENT_DEBUG=0

AMOEBA_CREATE_EXPERIMENT_DEBUG=0

AMOEBA_BUS=0

AMOEBA_INSTRUMENT_AT_ADDRESS_DEBUG = 0

AMOEBA_IMPORT_EXPERIMENT_DEBUG = 0

AMOEBA_EXPERIMENT_IMPORT_LINK_DEBUG = 0

class Amoeba_experiment():
    def __init__(self):
        """
        The Amoeba Experiment class this class stores the an experiment.
        """
        self.filename=""
        self.name=""
        self.description=""
        self.path = ""
        self.instruments=[]
        if AMOEBA_BUS:
            self.bus=[]
        self.links=[]
        self.control=[]
        self.reading=0
        self.sync=0
        self.fundamentals = ExperimentFundamentals()

    def read_in_from_XML(self,fileName):
        """
        This method reading an an Amoeba Experiment from an XML file.
        :param fileName: Path to the experiment xml file.
        """
        self.filename = fileName
        tree = ET.ElementTree()
        tree = ET.parse(fileName)
        try:
            print "First run."
            print ET.tostring(tree.getroot())
        except:
            print "Second run"
            tmp = ET.ElementTree(tree)
            print ET.tostring(tmp)
        self.create_experiment_from_elementtree(tree)

    def read_in_from_XML_string(self,xmlString):
        """
        This method creates an AMOEBA Experiment from an XML string.
        :param xmlString: An XML string containing an experiment.
        """
        if AMOEBA_EXPERIMENT_DEBUG:
            print xmlString
        tree = ET.ElementTree(ET.fromstring(xmlString))
        #Convert XML string to the experiment.
        self.create_experiment_from_elementtree(tree)
        self.loaded = 1
        if AMOEBA_EXPERIMENT_DEBUG:
            test_string = self.tree_string()
            print "Test string:"
            print test_string

    def instrument_at_address(self,address):
        """
        This function returns the instrument at the specified address.  If there is no instrument at the specified address
        it returns -1.
        :param address: CAN bus address of the instrument you are trying to receive.
        :return: return Instrument or -1 if there is no instrument at that address.
        """
        for i in self.instruments:
            if AMOEBA_INSTRUMENT_AT_ADDRESS_DEBUG:
                print i.print_command()
            if i.address==address:
                return i
        return -1

    def add_readings_from_XMLString(self,readings):
        """
        This function adds new readings to the experiment.  From an xml string.
        :param readings: New readings to add to the experiment.  These should be stored in an element tree.
        """
        if AMOEBA_EXPERIMENT_DEBUG:
            print "This method should update the experiment with data taken from the PI."
        #  Convert from string to Etree.
        tree = ET.fromstring(readings)
        self.add_readings_from_tree(tree)

    def add_readings_from_tree(self,readingsTree):
        """
        This method takes an ElementTree of readings and adds them to the experiment as well as updating all the necessary
        plots.
        :param readings: Element tree of readings.
        """
        if AMOEBA_EXPERIMENT_DEBUG:
            print "Adding readings from Element Tree."
        #root = readingsTree.getroot()
        root = readingsTree
        #  Check the root.
        if root.tag == "data":
            #  If the root is correct then add proceed to take the data from the tree.
            for readings in root:
                #  Retrieve which instrument needs to have data added to it.
                address = int(readings.attrib.get("address"))
                #  Retrieve reading time.
                time = readings.attrib.get("time")
                time = time.split(':')
                #  Retrieve reading date.
                date = readings.attrib.get("date")
                date = date.split('-')
                instrument_address = self.instrument_at_address(address)
                instrument = self.instruments[instrument_address]
                #instrument.print_command()
                for value in readings:
                    reading = AmoebaSensor.Amoeba_reading()
                    reading.set_reading_time(datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(round(float(time[2])))))
                    reading.set_sensor_reading(float(value.attrib.get("val")))
                    reading.print_reading()
                    channel_num = int(value.attrib.get("parameter_num"))
                    instrument.add_reading(channel_num,reading)
        else:
            return "ERROR"
        return "SUCCESS"


    def create_experiment_from_elementtree(self,tree):
        """
        This function converts an ElementTree containing an Amoeba Experiment into an Amoeba Experiment.
        :param tree: Element Tree Containing the experiment.
        """
        count = 0
        self.tree = ET.ElementTree()
        self.tree = tree
        experiment = tree.getroot()
        self.import_basics(experiment)
        #Retrieve name.
        for child in experiment:
            if AMOEBA_EXPERIMENT_DEBUG:
                print child.tag,child.attrib
            if child.tag == "link":
                tmplnk = AmoebaInstrumentLink()
                tmplnk.importFromTree(child)
                self.links.append(tmplnk)
            if child.tag == "instrument":
                self.import_instrument(child)
            if child.tag == "control":
                tmpcontrol = AmoebaCommandController()
                tmpcontrol.importFromTree(child)
                self.control.append(tmpcontrol)
            if child.tag == "data":
                values = child.getchildren()
                for value in values:
                    if value.tag == "value":
                        #   Import reading.
                        self.import_reading(value)
                        count = count + 1

    def import_basics(self,experiment):
        """
        This method imports the experiment basics.
        """
        try:
            self.name = experiment.attrib.get("name")
            if AMOEBA_EXPERIMENT_DEBUG:
                print self.name
            #Retrieve date.
            date = experiment.attrib.get("date_started")
            if str(date) != "None":
                date = date.split('-')
                self.date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
            if AMOEBA_EXPERIMENT_DEBUG:
                print self.date
            #Retrieve time.
            time = experiment.attrib.get("start_time")
            if str(time)!="None":
                time = time.split(':')
                #time = datetime.time(int(time[0]),int(time[1]),int(time[2]))
            datetaken = experiment.attrib.get("date_started")
            if str(datetaken)!="None":
                datetaken = datetaken.split('/')
            if str(time)!="None" and date != "None":
                self.time = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(round(float(time[2]))))
            if AMOEBA_EXPERIMENT_DEBUG:
                print self.time
        except:
            print "Error importing basics."

    def import_instrument(self,inst):
        try:
            #Retrieve name of file for the sensor.
            tmp = AmoebaSensor.Amoeba_sensor()
            file_name = inst.attrib.get("sensor_file_name")
            filename=Amoeba.INSTRUMENT_FOLDER+file_name
            if AMOEBA_EXPERIMENT_DEBUG:
                print filename
            #Retrieve sensor details from the file.
            sens = tmp.read_in_from_XML(filename)
            if AMOEBA_EXPERIMENT_DEBUG:
                sens.print_command()
            self.instruments.append(sens)
        except:
            print "Error importing experiment."

    def import_reading(self,element):
        #  Retrieve date and time.
        try:
            reading = AmoebaSensor.Amoeba_reading()
            #  Retrieve sensor address
            sensor_address = int(element.attrib.get("address"))
            sensor_num = int(element.attrib.get("parameter_num"))
            reading.importFromTree(element)
            if AMOEBA_IMPORT_EXPERIMENT_DEBUG:
                print time
                print "Instrument address = " + str(sensor_address) + " Location in array = " + str(sensor_address)
            inst = self.instrument_at_address(sensor_address)
            if inst != -1:
                inst.add_reading(sensor_num,reading)
            else:
                print "Error false address."
        except:
            print "Error importing reading."

    def tree_string(self):
        """
        This function returns an XML string of the element tree.
        :return: XML string of the ElementTree.
        """
        return tostring(self.tree.getroot(), encoding='utf8', method='xml')

    def clear_data(self):
        """
        This method clears the data from the instruments.
        """

    def create_tree_from_experiment(self):
        """
        This method creates a tree from the experiment.
        """


    def save(self,filename):
        """
        This method saves the experiment to an xml text file.
        """
        print "Save"
        self.writeElementTree()
        self.path = filename
        self.writeElementTreeToFile()

    def writeElementTree(self):
        """
        This function turns the parameters initialised above into an ElementTree.
        """
        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
            print "Write to XML."
        #Create the element tree.
        self.root = ET.Element("experiment")
        self.fundamentals.createTree(self.root)
        #Add the instruments to the tree
        for i in self.instruments:
            instrumentSubEl = ET.SubElement(self.root,"instrument")
            i.writeExperimentElement(instrumentSubEl)
        #Add the links to the tree
        for i in self.links:
            linkSubEl = ET.SubElement(self.root,"link")
            i.writeXMLElement(linkSubEl)
        #Add any readings available.
        print "Length of control array: " + str(len(self.control))
        for i in self.control:
            linkSubEl = ET.SubElement(self.root,"control")
            i.writeXMLElement(linkSubEl)
            print "Control!!!!!!!"
        dataelement = ET.SubElement(self.root,"data")
        for i in self.instruments:
            for j in i.parameters:
                j.writeDataToXML(dataelement,i.address)
        self.tree = ET.ElementTree(self.root)

    def writeElementTreeToFile(self):
        """
        This function writes the ElementTree to a file.
        """
        self.tree.write(self.path)

    def saveAsCSV(self,filename):
        """
        This method exports the experiment data to a comma separated file.
        """
        file = open(filename,'w')
        dataString = ""
        dataString = str(self.name) + "\n"
        for i in self.instruments:
            dataString = dataString + str(i.name) + "\n"
            for j in i.parameters:
                dataString = dataString + j.name + "\n" + "Time"
                for k in j.readings:
                    dataString = dataString + "," + str(k.time)
                dataString = dataString + "\n" + "Reading"
                for k in j.readings:
                    dataString = dataString + "," + str(k.reading)
                dataString = dataString + "\n"
        dataString = dataString + "\n"
        file.write(dataString)

if __name__=="__main__":
    tree = Amoeba_experiment()
    tree.read_in_from_XML("C:\\devel\\Ameoba\\Support_Files\\Experiment.xml")
    for i in tree.instruments:
        i.get_newest_readings()
