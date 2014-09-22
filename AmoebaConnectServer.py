import socket
from Amoeba import *
from PySide.QtGui import *

AMOEBA_CONNECT_SERVER_DEBUG=1

class AmoebaConnectServer(QWidget):
 
 
    def __init__(self,server,control):
        """

        This function creates the server control UI.

        When I have time I will make this class independent of the server variable.

        :param server: This is the global server class for the desktop client.
        :param control: This class controls the server.  It interfaces with the server.
        """
        super(AmoebaConnectServer,self).__init__()

        #  Running in Localmode by default
        self.running_local_mode = True

        #Create the server
        self.server = server
        self.control = control
        if AMOEBA_CONNECT_SERVER_DEBUG:
            print "Connect to Amoeba Server"
            
        #Create the new UI widgets.
        self.setWindowTitle("Amoeba Server Settings.")
        self.connect_button = QPushButton("Connect")
        self.disconnect_button = QPushButton("Disconnect")

        self.IP_address = QLineEdit(server.ip)
        self.IP_label = QLabel("Amoeba I.P.")
        self.port_number = QLineEdit(str(server.port))
        self.port_label = QLabel("Port")
        self.status_label = QLabel("Status:")
        self.status = QLabel("Not Connected")
        
        #Send experiment to Server widget.
        self.sendDataLabel = QLabel("Send Experiment to Server:")
        self.sendDataButton = QPushButton("Send")
        
        #Retrieve experiment from Server widget.
        self.retrieveDataLabel = QLabel("Retrieve Data from Server:")
        self.retrieveDataButton = QPushButton("Retrieve Data")
        
        #Test experiment widget.
        self.testExperimentLabel = QLabel("Test bus:")
        self.testExperimentButton = QPushButton("Test")

        #Start experiment widget.
        self.startExperiment = QLabel("Experiment:")
        self.startExperimentWidget = QPushButton("Start")
        
        #Stop experiment widget.
        self.stopExperimentWidget = QPushButton("Stop")

        #Local mode details
        self.local_mode = QCheckBox("Local Mode")
        self.serial_port_label = QLabel("Serial Port:")
        self.serial_port = QLineEdit("COM5")
        self.local_connect_button = QPushButton("Connect Locally")

        self.local_mode.setChecked(1)
                                                                     
        #Set up the layouts.
        self.layoutA = QHBoxLayout()
        self.layoutB = QHBoxLayout()
        self.layoutC = QHBoxLayout()
        self.layoutD = QHBoxLayout()
        self.layoutE = QVBoxLayout()
        self.layoutF = QVBoxLayout()
        self.layoutG = QVBoxLayout()
        self.layoutH = QHBoxLayout()
        self.layoutI = QVBoxLayout()
        self.layoutJ = QVBoxLayout()
        self.layoutK = QHBoxLayout()

        #Create Main Layout

        self.layoutE.addWidget(self.sendDataLabel)
        self.layoutE.addWidget(self.sendDataButton)
        
        self.layoutF.addWidget(self.retrieveDataLabel)
        self.layoutF.addWidget(self.retrieveDataButton)

        self.layoutG.addWidget(self.startExperiment)
        
        self.layoutH.addWidget(self.startExperimentWidget)
        self.layoutH.addWidget(self.stopExperimentWidget)

        self.layoutG.addLayout(self.layoutH)

        self.layoutI.addLayout(self.layoutJ)

        
        #Create Main Layout
        self.mainLayout  = QVBoxLayout()

        #Add widgets to layout.
        self.layoutA.addWidget(self.IP_label)
        self.layoutA.addWidget(self.IP_address)
        
        self.layoutC.addWidget(self.port_label)
        self.layoutC.addWidget(self.port_number)
        
        self.layoutB.addWidget(self.status_label)
        self.layoutB.addWidget(self.status)
        
        self.layoutD.addWidget(self.connect_button)
        self.layoutD.addWidget(self.disconnect_button)

        self.layoutK.addWidget(self.serial_port_label)
        self.layoutK.addWidget(self.serial_port)

        self.layoutJ.addWidget(self.local_mode)

        self.layoutJ.addLayout(self.layoutK)

        self.layoutJ.addWidget(self.local_connect_button)

        #Add sub layouts to main layout
        self.mainLayout.addLayout(self.layoutI)
        self.mainLayout.addLayout(self.layoutA)
        self.mainLayout.addLayout(self.layoutC)
        self.mainLayout.addLayout(self.layoutB)
        self.mainLayout.addLayout(self.layoutD)
        self.mainLayout.addLayout(self.layoutE)
        self.mainLayout.addLayout(self.layoutF)
        self.mainLayout.addLayout(self.layoutG)

        self.setLayout(self.mainLayout)
        
        #Create the window.
        self.subWindow = QMdiSubWindow()
        #Create IP Address window.
        self.subWindow.setWidget(self)

        #Link buttons with functions
        self.connect_button.clicked.connect(self.connectToServer)
        self.disconnect_button.clicked.connect(self.disconnectFromServer)

        self.sendDataButton.clicked.connect(self.send)
        self.startExperimentWidget.clicked.connect(self.start)
        self.stopExperimentWidget.clicked.connect(self.stop)
        self.retrieveDataButton.clicked.connect(self.retrieve)
        self.testExperimentButton.clicked.connect(self.test)
        self.local_mode.clicked.connect(self.localHost)
        self.local_connect_button.clicked.connect(self.connect_locally)

        #Disable necessary buttons.
        self.localModeActive()
        

    def test(self):
        """
        This function calls the control function which gets the AMOEBA Server to test that all the correct
        modules are connected to the bus for the loaded experiment.

        """
        self.control.testExperiment()

    def retrieve(self):
        """
        This function interfaces with the control to retrieve the current experiment from the server.

        """
        self.control.retrieveDataFromServer()

    def stop(self):
        """
        This function tells the control class to tell the Server to stop the current experiment.

        """
        self.stopExperimentWidget.setEnabled(0)
        self.startExperimentWidget.setEnabled(1)
        self.control.stopExperiment(self.running_local_mode)

    def start(self):
        """
        This function tells the control class to tell the Server to start the current experiment.
        """
        self.stopExperimentWidget.setEnabled(1)
        self.startExperimentWidget.setEnabled(0)
        print "Run experiment."
        self.control.connectedLocally = self.running_local_mode
        self.control.run()
        #self.control.startExperiment(self.running_local_mode)

    def show(self):
        """
        This function reveals the server control window.

        """
        if AMOEBA_CONNECT_SERVER_DEBUG:
            print "Show server connection window."
        self.mainLayout.update()
        self.subWindow.show()

    def send(self):
        """
        The calls the function which sends the current experiment to Server.

        """
        self.control.sendExperimentToServer()

    def connectToServer(self):
        """
        This function connects the client to the server.

        """
        if AMOEBA_CONNECT_SERVER_DEBUG:
            print "Connect to server."
        try:
            #Retrieve the data from line edits.
            ip = self.IP_address.text()
            port = int(self.port_number.text())
            if self.server.connect(ip,port) == "success":
                print "Connected."
                self.connectedEnable()
                self.status.setText("Connected")
                #  If the reactor isn't run here the whole program hangs.
                self.server.runReactor()
            else:
                print "Not connected."
                self.disconnectedDisabled()
                self.status.setText("Not Connected")
        except socket.error:
            print "Server not active."

    def disconnectFromServer(self):
        """
        This function disconnects with the Server.

        """
        if AMOEBA_CONNECT_SERVER_DEBUG:
            print "Disconnect from server."
        self.server.disconnect()

        self.disconnectedDisabled()
    
        self.disconnect_button.setEnabled(0)
        self.status.setText("Not Connected")

    def disconnectedDisabled(self):
        """
        This function disables and enables all the necessary buttons when the server is not connected.

        """
        self.disconnect_button.setEnabled(0)
        self.startExperimentWidget.setEnabled(0)
        self.stopExperimentWidget.setEnabled(0)
        self.retrieveDataButton.setEnabled(0)
        self.sendDataButton.setEnabled(0)
        
        self.connect_button.setEnabled(1)
        self.disconnect_button.setEnabled(0)

    def connectedEnable(self):
        """
        This function enables and disables all the necessary buttons once the server is connected.

        """
        print "Connected enable."
        self.disconnect_button.setEnabled(1)
        self.startExperimentWidget.setEnabled(1)
        self.stopExperimentWidget.setEnabled(0)
        self.retrieveDataButton.setEnabled(1)
        self.sendDataButton.setEnabled(1)

        self.connect_button.setEnabled(0)
        self.disconnect_button.setEnabled(1)
        
    def localHost(self):
        """
        This function sets AMEOABA into local host mode where the AMOEBA hardware is run off a uSB port on the local machine.

        """
        if self.local_mode.isChecked() == True:
            self.localModeActive()
            self.localMode = True
        else:
            self.localModeNotActive()
            self.disconnectedDisabled()
            self.localMode = False

    def localModeNotActive(self):
        """
        This function enables all the necessary buttons for remote operation.
        """
        self.disconnectedDisabled()

        #Activate local control
        self.connect_button.setEnabled(0)
        self.serial_port.setEnabled(0)
        self.local_connect_button.setEnabled(0)


    def localModeActive(self):
        """
        This function enables all the necessary
        """

        #Deactivate remote buttons.
        self.disconnectedDisabled()
        self.connect_button.setEnabled(0)

        #Activate local control
        self.serial_port.setEnabled(1)
        self.local_connect_button.setEnabled(1)

    def connect_locally(self):
        """
        This function connects to an AMOEBA system connected via a usb port.
        """
        print "Connect locally."
        success = self.control.connectToLocalServer(self.serial_port.text())
        if success == True:
            self.startExperimentWidget.setEnabled(1)
            self.stopExperimentWidget.setEnabled(0)


    def closeEvent(self, event):
        """
        This function hides the window when the user hits the close button.
        :param event: The window closing.
        """
        if AMOEBA_CONNECT_SERVER_DEBUG:
            print "Window closed."
        event.ignore()
        self.subWindow.hide()

def main():
    app = QApplication(sys.argv)
    Amoeba = AmoebaConnectServer()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
