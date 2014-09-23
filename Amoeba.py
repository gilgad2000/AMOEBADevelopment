import sys
from PySide.QtCore import *
from PySide.QtGui import *
from AmoebaMainWindow import *
from AmoebaServer import*
from AmoebaImportExperiment import *

#GIT TEST 2 !!!!

# Serial data testing program for use with an Ardunio board connected via USB on COM3.

#Global define variables.

DEFAULT_FOLDER = "C:\\devel\\Amoeba\\Support_Files\\"

EXPERIMENT_FOLDER = "C:\\devel\\Amoeba\\Support_Files\\Experiments\\"

INSTRUMENT_FOLDER = "C:\\devel\\Amoeba\\Support_Files\\Sensors\\"

SUCCESS = 0

#DEFAULT_IP = "129.236.254.122"

#Global Debug Variables
#Change 0s to 1s to run in debug mode.

class AmoebaSys():
    def __init__(self):
        """
        This function runs the main application.

        """
        print "Create Amoeba System."
        self.mainUI = AmoebaMainWindow()

def main():
    """
    From here the whole program is launched.

    """
    app = QApplication(sys.argv)
    app.setFont(QFont('SansSerif',11))
    #  Import the and install the qt reactor for twisted.
    Amoeba = AmoebaSys()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
