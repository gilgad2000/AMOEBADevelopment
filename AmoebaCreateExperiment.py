import sys
import os
import fnmatch
import Amoeba
from PySide.QtCore import *
from PySide.QtGui import *
from AmoebaSensor import *
from Amoeba import *
from AmoebaCreateExperimentShowAll import *
from AmoebaLinkInstruments import *
from AmoebaSetFundamentals import *
from AmoebaImportExperiment import *
import xml.etree.ElementTree as ET

#  Note:  Stages:
#  0 = select instruments,
#  1 = select timings,
#  2 = link instruments and select control parameters,
#  3 = select generic parameters,

AMOEBA_CREATE_EXPERIMENT_DEBUG=0


class AmoebaCreateExperimentWindow(QWidget):
    def __init__(self,currentExperiment):
        """
        This class holds the windows which shows the create experiment widget.
        :param currentExperiment:  The experiment currently in progress.
        """
        super(AmoebaCreateExperimentWindow,self).__init__()

        self.currentExperiment = currentExperiment

        #Create the window
        self.subWindow = QMdiSubWindow()

        self.widget = AmoebaCreateExperiment(self.subWindow,self.currentExperiment)
        
        #Create the UI.
        self.setWindowTitle("Create a new experiment.")

        self.scroll = QScrollArea()

        self.scroll.setMinimumWidth(270)
        self.scroll.setWidget(self.widget)
        self.scroll.setWidgetResizable(True)

        #Connect button to next function.
        self.subWindow.setWidget(self.scroll)

    def show(self):
        """
        This function shows the window which holds the widget.
        """
        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
            print "Show Window."
        self.subWindow.show()

    def closeEvent(self, event):
        """
        This function is triggered when the user tries to close the window.
        I'm not sure it fully works.
        :param event:
        """
        print "Window closed"
        event.ignore()
        print "Hide window."
        self.subWindow.hide()

########################################################################################################

class AmoebaCreateExperiment(QWidget):  
    def __init__(self,subWindow,currentExperiment):
        """
        This class stores the sub UIs involved in creating experiments, it also provides the basic control
        and framework for the revealing and hiding the correct UIs.
        :param subWindow:  Sub windows which displays the widgets.
        :param currentExperiment:  The experiment currently loaded.  Once completed this variable is set to the new experiment.
        """
        super(AmoebaCreateExperiment,self).__init__()
        self.stage = 0
        self.currentExperiment = currentExperiment
        #self.XMLWriter = ExperimentXMLWriter()
        self.XMLWriter = Amoeba_experiment()
        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
            print "Create new experiment."

        self.subWindow = subWindow

        #Create a scroll bar for the summary area
        self.layout = QVBoxLayout()

        #Create the widgets
        self.SetFundamentalParameters = AmoebaSetFundamentalParameters()
        self.ShowAllInstruments = AmoebaShowAllInstruments()
        self.LinkInstruments = LinkInstrumentsForm()

        self.next = QPushButton("Next")
        self.next.clicked.connect(self.next_pressed)

        #Add to the scroll widget
        self.layout.addWidget(self.SetFundamentalParameters)
        self.layout.addWidget(self.ShowAllInstruments)
        self.layout.addWidget(self.LinkInstruments)
        self.layout.addWidget(self.next)

        #Add the Widgets to the Subwindow
        self.setLayout(self.layout)

        #Hide all the widgets that will later be revealed.
        self.SetFundamentalParameters.hide()
        self.LinkInstruments.hide()

    def next_pressed(self):
        """
        This function handles the showing and hiding of UIs when the program is being run.
        """
        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
            print "Next pressed."

        #Check stage.
        if self.stage==0:
            self.ShowAllInstruments.retrieve_selected()
            self.XMLWriter.instruments = self.ShowAllInstruments.retrieve_selected()
            if len(self.XMLWriter.instruments)!=0:
                self.LinkInstruments.setInstruments(self.XMLWriter.instruments)
                #Show and hide appropriate widgets
                self.LinkInstruments.show()
                self.ShowAllInstruments.hide()
                #self.resize()
            else:
                print "No items in the list."
            self.stage = self.stage + 1
        else:
            if self.stage==1:
                #Retrieve Instruments
                self.XMLWriter.links, self.XMLWriter.control, proceed = self.LinkInstruments.getLinksandControl()
                if AMOEBA_CREATE_EXPERIMENT_DEBUG:
                    print "Proceed = " + str(proceed)
                if proceed == 0:
                    self.LinkInstruments.hide()
                    self.SetFundamentalParameters.show()
                    #self.resize()
                    for i in self.XMLWriter.links:
                        i.print_links()
                    self.stage = self.stage + 1
                else:
                    msg_box = QMessageBox()
                    msg_box.setText("Please Enter a Control Value for all Variables.")
                    msg_box.exec_()
            else:
                if self.stage==2:
                    #Hide widgets
                    self.XMLWriter.fundamentals = self.SetFundamentalParameters.getState()
                    self.XMLWriter.fundamentals.printFundamentals()
                    
                    self.stage = self.stage + 1
                    #Open up file dialog
                    path, _ = QFileDialog.getSaveFileName(self, "Save", '', "*.xml")
                    if path != "":
                        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
                            print "Write XML."
                            print path
                        self.XMLWriter.path = path
                        self.XMLWriter.writeElementTree()
                        self.XMLWriter.writeElementTreeToFile()
                        
                        self.currentExperiment.create_experiment_from_elementtree(self.XMLWriter.tree)
                        self.currentExperiment.make_gui()
                        self.currentExperiment.tree = self.XMLWriter.tree

                        if AMOEBA_CREATE_EXPERIMENT_DEBUG:
                            print ET.tostring(self.XMLWriter.tree, encoding='utf8', method='xml')

                        self.subWindow.hide()
                        self.stage = 0
