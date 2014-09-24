# Useful example of using Matplotlib and PySide found at: 

import sys
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
import thread

import pylab as pl
import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import date2num

from PySide.QtCore import *
from PySide.QtGui import *

from AmoebaSensor import *
from Amoeba import *

AMOEBA_SENSOR_TAB_DEBUG=0
AMOEBA_PARAMETER_DEBUG=0
AMOEBA_LINE_GRAPH_DEBUG=0
AMOEBA_PARAMETER_DEBUG=0
AMOEBA_SUMMARY_UI_DEBUG=0

class Amoeba_Sensor_Tab(QWidget):

    def __init__(self,parent=None):
        """
        This class creates the tabs which display the value of each instrument.
        :param parent: Inheritance parameter.
        """
        QWidget.__init__(self,parent)
        self.sensor = Amoeba_sensor()
        self.graph = Amoeba_Line_Graph()
        self.canvas = self.graph.retrieve_graph()
        self.graphs = []
        self.index = 0
        self.summary = Amoeba_Instrument_Summary_UI()

    def import_sensor(self,Amoeba_sensor):
        """
        This function sets the sensor attribute of the Sensor Tab class.
        :param Amoeba_sensor: Sensor
        """
        self.sensor = Amoeba_sensor
        if AMOEBA_SENSOR_TAB_DEBUG:
            print self.sensor
            print "Sensors loaded:"
            self.sensor.print_command()
            print "Loaded Sensor."

    def create_tab(self):
        """
        This method creates the tab from imported Amoeba_sensor.
        """
        # Set up scroll widget.
        if AMOEBA_SENSOR_TAB_DEBUG:
            print "Sensor memory location: " + str(self.sensor)
        scrollLayout = QVBoxLayout()
        scrollwidget = QWidget()
        scrollwidget.setLayout(scrollLayout)
        templayout = QVBoxLayout()
        self.UIs = QVBoxLayout()
        # Set up scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scrollwidget)
        # Set up the summary boxes
        self.summarybox = QGroupBox()
        if AMOEBA_SENSOR_TAB_DEBUG:
            print "Create tab"
        self.UIs.addWidget(scroll)
        #Create tab
        for i in self.sensor.parameters:
            #  Create sub tab for each parameter
            tmp = Amoeba_Parameter_UI(i)
            self.graphs.append(tmp)
            i.UI=tmp
            scrollLayout.addWidget(tmp.return_widget())
        self.sensor.get_newest_readings()
        self.setLayout(self.UIs)
        #  Create the tab summary.
        self.summary.createFromSensor(self.sensor)

    def update(self):
        """
        This method updates the tab.
        """
        for i in self.sensor.parameters:
            datax = []
            datay = []
            length = len(i.readings)
            if AMOEBA_SENSOR_TAB_DEBUG:
                print "Length = " + str(length)
                print "Sensor tab data:"
            for j in i.readings:
                datax.append(j.get_reading_time())
                datay.append(j.get_sensor_reading())
            if AMOEBA_SENSOR_TAB_DEBUG:
                print "Sensor data check:"
                print "X ="
                print datax
                print "Y ="
                print datay
            i.UI.setData(datay,datax)
            i.UI.run()
        self.summary.updateSummary()

    def clear_graphs(self):
        for i in self.sensor.parameters:
            i.clear()

    def getSummaryWidget(self):
        return self.summary


class Amoeba_Instrument_Summary_UI(QWidget):
    def __init__(self,parent=None):
        """
        This class creates the summary widget for an individual instrument, this widget is shown on the left hand side to the GUI.
        :param sensor: Amoeba Sensor which the UI displays.
        :param parent: Inheritance details.
        """
        QWidget.__init__(self,parent)
        layout = QVBoxLayout()
        self.summary_layout = QVBoxLayout()
        self.summary_box = QGroupBox()
        self.params = []
        layout.addWidget(self.summary_box)
        self.setLayout(layout)

    def createFromSensor(self,sensor):
        """
        This method sets up the summary boxes from the sensor.
        :param sensor:
        :return:
        """
        self.sensor = sensor
        if AMOEBA_SUMMARY_UI_DEBUG:
            print "Print instrument:"
            self.sensor.print_command()
        self.summary_box.setTitle(self.sensor.name)
        for i in self.sensor.parameters:
            param = Amoeba_Parameter_Summary(i)
            self.summary_layout.addWidget(param)
            self.params.append(param)
        self.summary_box.setLayout(self.summary_layout)

    def updateSummary(self):
        """
        This method updates the summary boxes.
        :return:
        """
        for i in self.params:
            i.update()


class Amoeba_Parameter_Summary(QWidget):
    def __init__(self,parameter,parent=None):
        """
        This class creates the summary widget for a single parameter.
        :param parameter: The parameter which it creates the Widget from.
        :param parent: Inheritance variable.
        """
        QWidget.__init__(self,parent)
        self.parameter=parameter
        layout = QHBoxLayout()
        self.name = QLabel(str(self.parameter.name+":"))
        self.value = QLabel(str(self.parameter.get_newest_reading()))
        layout.addWidget(self.name)
        layout.addWidget(self.value)
        self.setLayout(layout)

    def update(self):
        self.value.setText(str(self.parameter.get_newest_reading()))


class Amoeba_Parameter_UI(QThread):
    def __init__(self,parameter,parent=None):
        """
        This class creates the UI for each parameter.  These are added to the Amoeba_Sensor_Tab widget to create the UI
        for each instrument.
        :param parameter: Instrument parameter which UI gets created fro.
        :param parent: Inheritance variable.
        """
        QThread.__init__(self)
        self.timeToUpdate = True
        self.datax = []
        self.datay = []
        #Set up each item in the group.
        if AMOEBA_PARAMETER_DEBUG:
            parameter.print_parameter()
        #Set up the Parameters
        self.parameter = parameter 
        self.name=QLabel(parameter.name)
        self.description=QLabel(parameter.description)
        self.current_val=QLabel("N.A.")
        #Set up the Plot
        self.plot=Amoeba_Line_Graph()
        self.scrollBar = QScrollBar(Qt.Horizontal)
        self.num_past_readings = QSpinBox()
        self.num_past_readings.setValue(50)
        self.mostRecentReadings = QCheckBox("Most Recent Readings.")
        self.mostRecentReadings.setChecked(True)
        #Set up ordering of boxes
        self.groupbox=QGroupBox(parameter.name)
        
        layoutA=QVBoxLayout()
        layoutA.addWidget(self.plot.retrieve_graph())
        layoutA.addWidget(self.scrollBar)
        layoutB=QHBoxLayout()
        layoutB.addWidget(self.num_past_readings)
        layoutB.addWidget(self.mostRecentReadings)
        layoutB.addWidget(self.current_val)
        layoutC=QVBoxLayout()
        layoutC.addLayout(layoutB)
        layoutC.addWidget(self.description)
        
        self.mainlayout=QHBoxLayout()
        self.mainlayout.addLayout(layoutA)
        self.mainlayout.addLayout(layoutC)
        self.groupbox.setLayout(self.mainlayout)

        self.scrollBar.valueChanged.connect(self.update)
        self.mostRecentReadings.stateChanged.connect(self.update)
        self.num_past_readings.valueChanged.connect(self.update)
        self.num_past_readings.setMinimum(10)

    def return_layout(self):
        """
        This method returns the layout of the widget.
        :return: Layout of the widget.
        """
        return self.mainlayout

    def return_widget(self):
        """
        This method returns the class' widget.
        :return: QWidget
        """
        return self.groupbox

    def setData(self,datay,datax):
        """
        This method updates the data for the plot.
        :param datay: Y axis of the points to plot.
        :param datax: X axis of the points to plot.
        """
        if datax != self.datax and datay != self.datay:
            self.datax = datax
            self.datay = datay
            self.timeToUpdate = True
        else:
            self.timeToUpdate = False

    def run(self, *args, **kwargs):
        """
        This method is used to update the UI on it's own thread.
        """
        self.update()

    def update(self):
        """
        This method updates the widget's plot.
        """
        if self.timeToUpdate == True:
            if AMOEBA_PARAMETER_DEBUG:
                print "Updates Amoeba Parameter " + str(self.name)
                print "X = "
                print self.datax
                print "Y = "
                print self.datay
            length = len(self.datax)
            numReadings = int(self.num_past_readings.text())
            maximum = len(self.datax)- numReadings
            if maximum < 0:
                maximum = 0
            self.scrollBar.setMaximum(maximum)
            if maximum == 0:
                #  Update plot
                self.plot.update(self.datay,self.datax)
            else:
                if self.mostRecentReadings.isChecked() == True:
                    datatoplotx = self.datax[(length-numReadings):length]
                    datatoploty = self.datay[(length-numReadings):length]
                    self.scrollBar.setValue(maximum)
                else:
                    startVal = self.scrollBar.sliderPosition()
                    datatoplotx = self.datax[startVal:(startVal+numReadings)]
                    datatoploty = self.datay[startVal:(startVal+numReadings)]
                self.plot.update(datatoploty,datatoplotx)
            #  Get and display the last item in the array.
            if len(self.datay)!=0:
                txt = str(self.datay[-1])
                self.current_val.setText(txt)
        self.timeToUpdate = True

    def size(self):
        """
        This method returns the size of the widget.
        :return: Widget size.
        """
        return self.groupbox.size()

    def clear(self):
        """
        This method clears the plot for the channel.
        """
        self.plot.clear_graph()

class Amoeba_Line_Graph():

    def __init__(self):
        """
        This class is for the plot on each of the parameter UIs.
        """
        #Generate plot
        x = []
        y = []
        self.fig = Figure(figsize=(8,4),dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        self.sub_plot = self.fig.add_subplot(111)
        self.sub_plot.xaxis_date()
        if AMOEBA_LINE_GRAPH_DEBUG:
            print "X = "
            print x
            print "Y = "
            print y
            print "Create "
            print self.sub_plot.plot
        self.sub_plot.plot(y,x,'b')
        self.sub_plot.set_xlabel('Time')
        self.fig.autofmt_xdate()
        #Create canvas for the plot
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setMinimumSize(self.canvas.size())

    def update(self,datay,datax):
        """
        This method updates the plot with the input data.
        :param datay: Y axis of the points to plot.
        :param datax: X axis of the points to plot.
        """
        if AMOEBA_LINE_GRAPH_DEBUG:
            print "Update sub plot"
            print "X = "
            print datax
            print "Y = "
            print datay
            print "Update "
            print self.sub_plot.plot
        # Clear the graph.
        self.clear_graph()
        self.sub_plot.plot(datax,datay,'b')
        self.sub_plot.set_visible(True)
        self.sub_plot.autoscale(True,"both")
        self.canvas.draw()
        
    def retrieve_graph(self):
        """
        This method returns the plot's widget.
        :return:
        """
        return self.canvas

    def clear_graph(self):
        """
        This method clears the graph.
        """
        y = []
        x = []
        self.sub_plot.clear()
        self.sub_plot.set_visible(True)
        self.sub_plot.autoscale(True,"both",False)
        self.sub_plot.plot(y,x,'b')
        self.canvas.draw()

if __name__ == '__main__':
    print "Running"
    SensTab = Amoeba_Sensor_Tab()
    Sens = Amoeba_sensor()
    Sens.read_in_from_XML("C:\\devel\\Ameoba\\Support_Files\\Thermocouples.xml")
    SensTab.import_sensor(Sens)
    SensTab.create_tab()
