import sys
import os
import xml.etree.ElementTree as ET
import string
import datetime

AMOEBA_SENSOR_DEBUG=0
AMOEBA_COMMAND_DEBUG=0
AMOEBA_PARAMETER_DEBUG=0
AMOEBA_IMPORT_READING_DEBUG=0
AMOEBA_TOTAL_READINGS_WRITTEN=0

from Amoeba import *

class Amoeba_sensor():

    def __init__(self):
        """
        This class stores the necessary methods and data for a sensor(this can be either a sensor or a controller).
        """
        self.number_of_parameters = 0
        self.commands = []
        self.parameters = []
        self.description = ""
        self.address=-1
        self.type=""
        self.name=""
        self.filename=""

    def read_in_from_XML(self,fileName):
        """
        This method reads in an Amoeba_sensor from an XML file.
        :param fileName: Path to the XML file.
        :return: Returns an Amoeba_sensor.
        """
        tree = ET.parse(fileName)
        self.filename = os.path.basename(fileName)
        root = tree.getroot()
        self.name = root.attrib.get("name")
        address = root.attrib.get("address")
        self.description = root.attrib.get("description")
        self.number_of_parameters = int(root.attrib.get("number_of_parameters"))
        self.address = int(address)
        self.type = root.attrib.get("type")
        for child in root:
            if child.tag == "command":
                cmd = Amoeba_command()
                self.commands.append(cmd.retrieve_data(child))
            if child.tag == "parameter":
                param= Amoeba_parameter()
                self.parameters.append(param.retrieve_data(child))
        if AMOEBA_SENSOR_DEBUG:
            for i in self.parameters:
                i.print_parameter()
            for i in self.commands:
                i.print_command()
        return self

    def print_command(self):
        """
        This method prints out the Amoeba_sensor.
        """
        print "Name = " + str(self.name)
        print "Address = " + str(self.address)
        print "Description = " + str(self.description)
        print "Type = " + str(self.type)
        print "Filename = " + str(self.filename)
        for i in self.parameters:
            i.print_parameter() # slightly cryptic python way of writing self.parameters[i]
        for i in self.commands:
            i.print_command()

    def get_address(self):
        """
        This method returns the address of the Amoeba_sensor.
        :return: Address of the Amoeba_sensor.
        """
        return self.address

    def add_reading(self,channel_num,reading):
        """
        This method add readings to the sensor.
        :param sensor_num:
        :param reading:
        """
        if AMOEBA_SENSOR_DEBUG:
            print "Add reading.  Data added: Sensor address = " + str(self.address) + "Sensor channel = " + str(channel_num) + " Reading = "
            reading.print_reading()
        try:
            self.parameters[channel_num].add_reading(reading)
        except:
            print "Error out of range:\nChannel number = " + str(channel_num) + " Instrument address = " + str(self.address)

    def get_newest_readings(self):
        """
        This method returns the most recent readings for an Amoeba_sensor.
        :return: A list of Amoeba_reading containing the newest readings.
        """
        reading = []
        for i in self.parameters:
            last = i.get_newest_reading()
            if last != -1:      # -1 returned if no readings are present
                reading.append(last)
                if AMOEBA_SENSOR_DEBUG:
                    print " Reading = "
                    #last.print_reading()           LINE DOESN'T WORK, FIND OUT WHY WHEN I HAVE THE TIME
            else:
                reading = "N.A."
                if AMOEBA_SENSOR_DEBUG:
                    print "N.A."
        return reading

    def writeExperimentElement(self,inst):
        """
        This method writes the Amoeba_sensor to an Elementtree element.
        :param inst: Instrument element needs to be passed in.
        :return: Instrument element with all the attributes added.
        """
        if AMOEBA_SENSOR_DEBUG:
            print "Write experiment element."
            
        inst.attrib['address']=str(self.address)
        inst.attrib['name']=str(self.name)
        inst.attrib['sensor_file_name']=str(self.filename)

        return inst

    def clear(self):
        """
        This method clears the data from all the instruments.
        """
        for i in self.parameters:
            i.clear()

    def writeReadingsToXML(self):
        """
        This method writes the reading to an XML string.
        """
        print "Write to XML."

class Amoeba_reading():

    def __init__(self):
        """
        This class stores the readings for the sensors.
        """
        self.time=-1
        self.reading=-1

    def set_sensor_reading(self,num):
        """
        This method sets the readings value.
        :param num: Value.
        """
        self.reading = float(num)

    def set_reading_time(self,time):
        """
        This method allows you to set the reading time.
        :param time: Reading time.
        """
        self.time = time

    def get_sensor_reading(self):
        """
        This method returns the reading.
        :return: reading
        """
        return self.reading

    def get_reading_time(self):
        """
        This method returns the time the reading was taken.
        :return: reading time
        """
        return self.time

    def print_reading(self):
        """
        This method prints out the reading.
        """
        print "Time taken = " + str(self.time) + " Reading = " + str(self.reading)

    def importFromTree(self,treeElement):
        date = treeElement.attrib.get("date")
        date = date.split("-")
        time = treeElement.attrib.get("time")
        time = time.split(':')
        time = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(round(float(time[2]))))
        #  Retrieve sensor address
        sensor_address = int(treeElement.attrib.get("address"))
        if AMOEBA_IMPORT_READING_DEBUG:
            print time
            print "Test" + str(treeElement.tag) + str(treeElement.attrib)
            print "Instrument address = " + str(sensor_address) + " Location in array = " + str(sensor_address)
        self.set_reading_time(time)
        self.set_sensor_reading(float(treeElement.attrib.get("val")))

 
class Amoeba_command():

    def __init__(self):
        """
        This method stores a command used by the sensor.
        """
        self.number_inputs = 0
        self.number_outputs = 0
        self.command_string = ""

    def retrieve_data(self,data_string):
        """
        TRetrieves the reading data from an elementTree Element.
        :param data_string: ElementTree Element.
        :return: Amoeba_command.
        """
        self.number_inputs = data_string.attrib.get("inputs")
        self.number_outputs = data_string.attrib.get("outputs")
        self.command_string = data_string.attrib.get("command")
        if AMOEBA_COMMAND_DEBUG:   
            self.print_command()
        return self

    def print_command(self):
        """
        This method prints out a command.number_of_
        """
        print "String = " + self.command_string + " Outputs = " + self.number_outputs + " Inputs = " + self.number_inputs

class Amoeba_parameter():
    
    def __init__(self):
        """
        This class stores the data and methods for each channel in an Amoeba_sensor.
        """
        self.name = ""
        self.description = ""
        self.number = 0
        self.readings=[]

    def retrieve_data(self,data_string):
        """
        This method retrieves the parameter from an Element Tree element.
        :param data_string: Input data string.
        :return: Amoeba_parameter with the corAmoebarect data.
        """
        self.name = data_string.attrib.get("name")
        self.number = data_string.attrib.get("number")
        self.description = data_string.attrib.get("description")
        if AMOEBA_PARAMETER_DEBUG:
            self.print_parameter()
        return self

    def print_parameter(self):
        """
        This method prints out a parameter.
        """
        print "Name = " + self.name + " Description = " + self.description + " Number = " + self.number

    def add_reading(self,data):
        """
        This method adds a reading to the parameter.
        :param data: Reading.
        """
        if AMOEBA_PARAMETER_DEBUG:
            data.print_reading()
        self.readings.append(data)

    def link_to_UI(self,UI):
        """
        This method links parameter class with its UI.
        :param UI:
        """
        self.UI=UI

    def get_newest_reading(self):
        """
        This method returns the latest reading for that parameter.
        :return: Latest reading.
        """
        length = len(self.readings)
        if length > 0:
            return self.readings[length-1].reading
        else:
            return "N.A."

    def clear(self):
        """
        This method clears all past readings from the channel.
        """
        print "Clear"
        self.readings=[]

    def writeDataToXML(self,dataRoot,address):
        """
        Write readings to an XML tree.
        """
        count = 0
        for i in self.readings:
            readingEl = ET.SubElement(dataRoot,"value")
            readingEl.attrib['address'] = str(address)
            readingEl.attrib['parameter_num'] = str(self.number)
            readingEl.attrib['val'] = str(i.reading)
            readingEl.attrib['time'] = str(i.time.time())
            readingEl.attrib['date'] = str(i.time.date())
            count = count + 1
        if AMOEBA_TOTAL_READINGS_WRITTEN:
            print "Total readings written = " + str(count)

if __name__== "__main__":
    tree = Amoeba_sensor()
    tree.read_in_from_XML("C:\\devel\\Ameoba\\Support_Files\\Sensors\\Thermocouples.xml")
    #tree.read_in_from_XML("C:\\devel\\Ameoba\\Support_Files\\CO2sensor.xml")
    tree.print_command()
