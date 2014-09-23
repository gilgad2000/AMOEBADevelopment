import sys
from PySide.QtCore import *
from PySide.QtGui import *
from AmoebaSensorTab import *
from AmoebaSensor import *
from AmoebaImportExperiment import *
from Amoeba import *

AMOEBA_TAB_DIALOG_DEBUG=0

class TabDialog(QWidget,QThread):
    def __init__(self, parent=None):
        """
        The class is used to create the tabbed dialogue used for the main UI.
        :param parent: Used for inheritance purposes.
        """
        QWidget.__init__(self, parent)
        QThread.__init__(self)

        self.loaded = 0
        self.tabs = []
        self.summaries = []

        if AMOEBA_TAB_DIALOG_DEBUG:
            print "Creating tab widget"

        self.tabWidget=QTabWidget()
        self.tabWidget.setMinimumWidth(1000)
        self.tabWidget.setMaximumWidth(1100)
        self.tabWidget.setMinimumHeight(400)
        self.summary_box = QGroupBox("Summary")
        
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.summary_box)
        mainLayout.addWidget(self.tabWidget)
        self.setLayout(mainLayout)

    def make_gui(self,experiment):
        """
        This method creates the tabs in GUI from an experiment.
        :param experiment: AmoebaExperiment class containing and experiment.
        """
        #Create the scroll widget
        self.clear_gui()
        self.scrollLayout = QVBoxLayout()
        scrollwidget = QWidget()
        scrollwidget.setLayout(self.scrollLayout)
        
        #  Create a scroll bar for the summary area
        self.sum_scroll = QScrollArea()
        self.sum_scroll.setWidgetResizable(True)
        self.sum_scroll.setWidget(scrollwidget)

        for i in experiment.instruments:
            if AMOEBA_TAB_DIALOG_DEBUG:
                print "Start = " + str(i)
                i.print_command()
                print "Finish\n"
            tab = Amoeba_Sensor_Tab()
            tab.import_sensor(i)
            tab.create_tab()
            tab.index = self.tabWidget.addTab(tab, tab.sensor.name)

            self.scrollLayout.addWidget(tab.getSummaryWidget())

            if AMOEBA_TAB_DIALOG_DEBUG:
                print "Index = " + str(tab.index)
            self.tabs.append(tab)
        self.summary_box.setLayout(self.scrollLayout)
        self.loaded = 1


    def clear_gui(self):
        """
        This method clears the UI.  It still doesn't clear the tabs.
        """
        if AMOEBA_TAB_DIALOG_DEBUG:
            print "Clear tabs"
        #  Clear the summaries.
        self.scrollLayout = QVBoxLayout()
        #  Clear the tabs.
        self.tabWidget.clear()
        self.tabWidget.update()
        self.tabs = []

    def run(self, *args, **kwargs):
        self.update()

    def update(self):
        """
        This method updates the tabs in the GUI.  I think it still needs some work doing to it.
        """
        if AMOEBA_TAB_DIALOG_DEBUG:
            print "Update: "
        for i in self.tabs:
            i.update()
            if AMOEBA_TAB_DIALOG_DEBUG:
                print i

    def clear(self):
        for i in self.tabs:
            i.clear_graphs()

    def print_command(self):
        """
        I'm not sure this method is used.  I will return to it later and delete it.
        """
        print "Tab name = "

if __name__ == "__main__":
    app = QApplication(sys.argv)
    experiment = Amoeba_experiment()
    experiment.read_in_from_XML("C:\\devel\\Ameoba\\Support_Files\\Experiments\\Experiment.xml")
    tabdialog = TabDialog()
    tabdialog.make_gui(experiment)
    tabdialog.update()
    sys.exit(app.exec_())
