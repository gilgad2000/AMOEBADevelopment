import sys
import os
import Amoeba
from PySide.QtCore import *
from PySide.QtGui import *
from AmoebaMainGUI import *


class AmoebaCreateExperiment():
    def __init__(self,parent=None):
        self.path = ""

    def create(self):
        print "Amoeba Create Experiment"



class AmoebaLoadExperiment():
    def __init__(self,parent=None):
        self.path = ""

    def load(self):
        path, _ = QFileDialog.getOpenFileName()
        return path

class AmoebaOpenMainUI():
    def __init__(self,path,parent=None):
        self.window = TabDialog()
        self.experiment = Amoeba_experiment()
        self.experiment.read_in_from_XML(path)
        self.window.make_gui(self.experiment)
        
    def show(self):
        self.window.show()

    def update(self):
        self.window.update()
