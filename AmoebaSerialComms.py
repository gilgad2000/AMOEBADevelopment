__author__ = 'Matt'

import serial
import AmoebaBusString
import thread
import time
import datetime

AMOEBA_SERIAL_COMMS = 0
AMOEBA_SERIAL_COMMS_MONITOR = 0
class AmoebaSerialComms():
    def __init__(self,port):
        """
        This method initialises the serial comms for AMOEBA.
        """
        #  Set up the serial communications method.
        self.serialConnection = serial.Serial()
        self.serialConnection.baudrate = 115200
        self.serialConnection.port = port
        self.serialConnection.bytesize = serial.EIGHTBITS
        self.serialConnection.timeout = 1

        #  Create the string creation method.
        self.stringMaker = AmoebaBusString.AmoebaBusStringMethods()

        #  Create the continue read variable.
        self.read = False

        #  This variable stores if is connected to the bus.
        self.connected = False

        #  This structure stores all the strings that come off the bus.
        self.stringFromBus = []

    def connect(self):
        """
        This method handles the opening of the serial connection.
        """
        try:
            self.serialConnection.open()
            if AMOEBA_SERIAL_COMMS:
                print "Connect."
            time.sleep(1)
            readStr = self.serialConnection.readline()
            print readStr
            if readStr == "can init ok!!\r\n":
                if AMOEBA_SERIAL_COMMS:
                    print "Connection successfully."
                #  Start receive thread.
                self.connected = True
            else:
                if AMOEBA_SERIAL_COMMS:
                    print "Connection failed."
                self.connected = False
        except serial.serialutil.SerialException:
            raise Exception, "Channel did not open"


    def readFromBus(self):
        #  Loop until read is False.
        while self.read==True:
            received = ''
            #  Read from serial port.
            received = self.serialConnection.readline()
            #  If the received line is not empty.
            if received != '':
                readingtime = datetime.datetime.now()
                self.stringFromBus.append([received,readingtime])
        if AMOEBA_SERIAL_COMMS:
            print "Read thread stopped."

    def program(self,controller_address,controller_channel,sensor_address,sensor_channel,value,inverse,error):
        """
        This method programs a controller which is connected to the bus.
        """
        if self.connected == True:
            #  Create the string to send to the Arduino to program the first part of the controller.
            sendStr = self.stringMaker.ProgramA(sensor_address,sensor_channel,value,controller_channel,controller_address)
            self.serialConnection.flush()
            self.serialConnection.write(sendStr)
            if AMOEBA_SERIAL_COMMS_MONITOR:
                print sendStr
            time.sleep(0.1)
            #  Create the string to send to the Arduino to program the second part of the controller.
            sendStr = self.stringMaker.ProgramB(controller_address,controller_channel,inverse,error)
            self.serialConnection.flush()
            self.serialConnection.write(sendStr)
            if AMOEBA_SERIAL_COMMS_MONITOR:
                print sendStr
            time.sleep(1)

    def requestData(self,address,channel):
        """
        This method is used to request Data from client.
        """
        if self.connected == True:
            sendStr = self.stringMaker.requestData(address,channel)
            self.serialConnection.flush()
            self.serialConnection.write(sendStr)
            if AMOEBA_SERIAL_COMMS_MONITOR:
                print sendStr

    def control(self,address,channel,value):
        """
        This method is used to send a control string to set the value of a controller.
        """
        if self.connected == True:
            sendStr = self.stringMaker.Control(address,channel,value)
            self.serialConnection.flush()
            self.serialConnection.write(sendStr)
            if AMOEBA_SERIAL_COMMS_MONITOR:
                print sendStr

    def start(self):
        """
        This method starts an experiment.
        """
        if self.connected == True:
            #  Start the receive thread.
            self.read = True
            thread.start_new_thread(self.readFromBus,())
            #  Start the experiment.
            self.serialConnection.flush()
            self.serialConnection.write("Start:\n")
            if AMOEBA_SERIAL_COMMS_MONITOR:
                print "Start:"
            self.stringFromBus = []

    def stop(self):
        """
        This method stops an experiment.  The packed is sent multiple times to make sure it reaches all the controllers
        on the network.
        """
        if self.connected == True:
            self.stringFromBus = []
            self.read = False
            for i in range(0,10):
                self.serialConnection.flush()
                self.serialConnection.write("Stop:\n")
                if AMOEBA_SERIAL_COMMS_MONITOR:
                    print "Stop:"
                time.sleep(0.1)
            time.sleep(1)

    def disconnect(self):
        """
        This method closes the serial connection.
        """
        if self.connected == True:
            if AMOEBA_SERIAL_COMMS:
                print "Stop."
            self.read = False
            try:
                self.serialConnection.close()
            except:
                "Error: Didn't close properly."

    def clearAll(self):
        """
        This method starts an experiment.
        """
        if self.connected == True:
            if AMOEBA_SERIAL_COMMS:
                print "Clear All."
            self.serialConnection.flush()
            self.serialConnection.write("ClearAll:")
            if AMOEBA_SERIAL_COMMS_MONITOR:
                print "ClearAll:"

if __name__ == '__main__':
    port = "COM5"
    try:
        SerialComms = AmoebaSerialComms(port)
        SerialComms.connect()
        SerialComms.program(10,0,11,0,512,0,20)
        SerialComms.requestData(11,0)
        thread.start_new_thread(SerialComms.readFromBus,())
        SerialComms.start()
        for j in range(0,10):
            for i in range(0,10):
                SerialComms.requestData(11,0)
                SerialComms.requestData(10,0)
                time.sleep(0.3)
        SerialComms.stop()
        SerialComms.clearAll()
        SerialComms.disconnect()
    except:
        print "Fail!!"