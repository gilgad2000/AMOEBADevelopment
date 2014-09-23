import sys
from PySide.QtCore import *
from PySide.QtGui import *
from Amoeba import *
from AmoebaMainGUI import *
from AmoebaGenerateExperiment import *
from AmoebaConnectServer import *
from AmoebaCreateExperiment import *
from AmoebaImportExperiment import *
from AmoebaExperimentControl import *
from AmoebaDesktopExperiment import *

class AmoebaMainWindow(QMainWindow):

    def __init__(self):
        """
        This class is for the main project window.
        """
        super(AmoebaMainWindow,self).__init__()
        self.tabs = TabDialog()
        self.currentExperiment = Amoeba_desktop_experiment(self.tabs)
        self.setCentralWidget(self.tabs)
        
        self.Menu()
        self.setWindowTitle(self.tr("Amoeba: Making Environmental Control Simple"))
        self.show()
        self.loadexperiment = AmoebaLoadExperiment()
        
        #Initialise the server connections.
        self.server = AmoebaServer(self.currentExperiment)
        self.experimentControl = AmoebaExperimentControl(self.server,self.currentExperiment,self.tabs)
        
        self.connectServer = AmoebaConnectServer(self.server,self.experimentControl)
        self.createExperiment = AmoebaCreateExperimentWindow(self.currentExperiment)

    def Menu(self):
        """
        This method sets up the menus for the main window.
        """
        menu = self.menuBar()
        
        filemenu = menu.addMenu('File')
        connectmenu = menu.addMenu('Connect')

        file_new = QAction('New Experiment',self)

        file_save = QAction('Save Experiment', self)
        file_save.triggered.connect(self.SaveExperiment)

        file_save_csv = QAction('Save Experiment as CSV File', self)
        file_save_csv.triggered.connect(self.SaveExperimentAsCSV)

        file_load = QAction('Load Experiment', self)
        file_load.setStatusTip('Load a previous experiment.')
        file_load.triggered.connect(self.LoadExperiment)

        clear_GUI = QAction('Clear Gui', self)
        clear_GUI.setStatusTip('Clear the GUI.')
        clear_GUI.triggered.connect(self.clearGui)

        file_exit = QAction('Exit', self)
        file_exit.setStatusTip('Close the program')

        #Add all the actions to the menu
        filemenu.addAction(file_new)
        filemenu.addAction(file_load)
        filemenu.addAction(file_save)
        filemenu.addAction(file_save_csv)
        filemenu.addAction(clear_GUI)
        filemenu.addAction(file_exit)

        connect_server = QAction('Connect to an Amoeba Server.',self)
        connect_newdevice = QAction('Connect a new devise.',self)

        connect_server.triggered.connect(self.ConnectServer)
        file_new.triggered.connect(self.CreateExperiment)

        connectmenu.addAction(connect_server)
        connectmenu.addAction(connect_newdevice)
        
        file_exit.triggered.connect(self.close)

    def LoadExperiment(self):
        """
        The method loads in an experiment.
        """
        print "Load experiment"
        self.currentExperiment = Amoeba_desktop_experiment(self.tabs)
        self.path = self.loadexperiment.load()
        self.currentExperiment.read_in_from_XML(self.path)
        self.tabs.clear_gui()
        self.tabs.make_gui(self.currentExperiment)
        self.tabs.update()

    def ConnectServer(self):
        """
        This method shows the Connect Server Window.
        """
        print "Connect Server"
        self.connectServer.show()

    def CreateExperiment(self):
        """
        This method shows the create experiment widget.
        """
        print "Create Experiment."
        self.createExperiment.show()

    def SaveExperiment(self):
        """
        This method saves the experiment.
        """
        filename, _ = QFileDialog.getSaveFileName(self,"Save", "", "*.xml")
        self.currentExperiment.save(filename)

    def SaveExperimentAsCSV(self):
        """
        This method saves the experiment.
        """
        filename, _ = QFileDialog.getSaveFileName(self,"Save", "", "*.csv")
        self.currentExperiment.saveAsCSV(filename)

    def closeEvent(self, event):
        """
        This method is inacted when the window is closed.  Currently is gracefully shuts down communications with the server.
        :param event: Event
        """
        if self.server.connected ==1:
            self.server.disconnect()
        if self.experimentControl.connectedLocally == True:
            self.experimentControl.disconnectFromLocalServer()

    def clearGui(self):
        """
        This method clears the GUI.
        :return:
        """
        self.tabs.clear_gui()
        self.currentExperiment = Amoeba_desktop_experiment(self.tabs)
        
def main():
    app = QApplication(sys.argv)
    Amoeba = AmoebaMainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
