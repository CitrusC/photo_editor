#!/usr/bin/env python
import os, sys
from PyQt5 import QtCore, QtGui


filenames = []


class Window(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtGui.QWiget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.setCentralWidget(self.centralwidget)

        # create a layout for your scrollarea
        self.formLayout = QtGui.QFormLayout(self.scrollAreaWidgetContents)
        self.addFiles()

    def addFiles(self):
        global filenames
        filenames.append("~/files/newFile.txt")
        button = QtGui.QPushButton(os.path.basename(filenames[-1]))
        self.formLayout.addWidget(button)