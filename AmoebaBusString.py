__author__ = 'Matt'
###  This file contains functions which are used to create and analyse strings for the bus or that come off the CAN bus.  ###
import xml.etree.ElementTree as ET
import AmoebaSensor

AMOEBA_BUS_DEBUG = 0
AMOEBA_SHOW_STRING_ERROR = 0

class AmoebaBusStringMethods():

    def requestData(self,address,channel):
        requestDataStr = "RequestData:" + str(address) + ":" + str(channel) + '\n'
        if AMOEBA_BUS_DEBUG:
            print requestDataStr
        return requestDataStr

    def ProgramA(self,sensor_address,sensor_channel,value,controller_channel,controller_address):
        ProgramAStr = "ProgramA:" + str(sensor_address) + ":" + str(sensor_channel) + ":" + str(value) + ":" + str(controller_channel) + ":" + str(controller_address) + "\n"
        if AMOEBA_BUS_DEBUG:
            print ProgramAStr
        return ProgramAStr

    def ProgramB(self, controller_address, controller_channel, inverse, error):
        if inverse == True:
            ProgramBStr = "ProgramB:" + str(controller_address) + ":" + str(controller_channel) + ":1:" + str(error) + '\n'
        else:
            ProgramBStr = "ProgramB:" + str(controller_address) + ":" + str(controller_channel) + ":0:" + str(error) + '\n'
        if AMOEBA_BUS_DEBUG:
            print ProgramBStr
        return ProgramBStr

    def Start(self):
        StartStr = "Start:\n"
        if AMOEBA_BUS_DEBUG:
            print StartStr
        return StartStr

    def Stop(self):
        StopStr = "Stop:\n"
        if AMOEBA_BUS_DEBUG:
            print StopStr
        return StopStr

    def Control(self,controller_address,controller_channel,value):
        ControlStr = "Control:" + str(controller_address) + ":" + str(controller_channel) + ":" + str(value) + '\n'
        if AMOEBA_BUS_DEBUG:
            print ControlStr
        return ControlStr

    def DataFrom(self,receivedString):
        tmp = receivedString.split(":")
        if tmp[0] == "DataFrom":
            tmp[1] = int(tmp[1])
            tmp[3] = int(tmp[3])
            tmp[5] = float(tmp[5])
        return tmp

    def AnalyseDataFromServer(self, receivedString, time):
        reading = AmoebaSensor.Amoeba_reading()
        reading.time = time
        receivedString = receivedString.split(":")
        if AMOEBA_BUS_DEBUG:
            print receivedString
        try:
            address = int(receivedString[1])
            channel = int(receivedString[3])
            value = float(receivedString[5])
            reading.reading = value
            if AMOEBA_BUS_DEBUG:
                print "Address = " + str(address) + "  Channel = " + str(channel) + " Value = " + str(value)
                print "Time = " + str(time)
            return address, channel, reading
        except:
            if AMOEBA_SHOW_STRING_ERROR:
                print "Error!!!!"
                print receivedString
            #  If there's an error return -1
            return -1, -1, -1

    def RemoteCalibration(self,deviceAddress,parameterNumber,value):
        remoteCalStr = "RemoteCalibration:" + str(deviceAddress) + ":" + str(parameterNumber) + ":" + str(value) + "\n"
        if AMOEBA_BUS_DEBUG:
            print remoteCalStr
        return remoteCalStr

    def RequestCalibration(self,deviceAddress,parameterNumber):
        reqCalStr = "RequestCalibration:" + str(deviceAddress) + ":" + str(parameterNumber) + "\n"
        if AMOEBA_BUS_DEBUG:
            print reqCalStr
        return reqCalStr