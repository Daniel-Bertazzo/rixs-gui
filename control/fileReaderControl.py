# ***** Imports *****

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui as QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

import sys
import h5py

from dataPlotControl import DataPlotWindow


# ***** Code *****

class FileReaderWindow(QMainWindow):
    '''Main window class: hdf and h5 file processing    
    '''
    
    def __init__(self):
        super(FileReaderWindow, self).__init__()
        
        # Loads ui made in qt designer
        uic.loadUi("../ui/fileReader.ui", baseinstance=self)

        # Config option to display the image the correct way (without needing to transpose) later
        # when using pyqgraph.ImageView
        pg.setConfigOptions(imageAxisOrder='row-major')

        # Disables footer frame (because no data has been loaded yet)
        self.footerFrame.setEnabled(False)

        # Connects widgets' signals to the custom slots
        self.pushButtonOpen.clicked.connect(self.openFile)
        self.pushButtonPlot.clicked.connect(self.plotData)
        self.pushButtonClear.clicked.connect(self.clearFields)
        
        # Displays the window
        self.show()

    @pyqtSlot()
    def openFile(self):
        '''Slot responsible for opening the Open File dialog and load the hdf/h5 file into memory
        when the `pushButtonOpen` is pressed.
        
        '''

        # Filter file types to avoid errors
        fileFilter = "hdf/h5 file (*.h5 *.hdf)"
        # Gets file name (including path)
        self.fileName = QFileDialog.getOpenFileName(caption="Select a file", filter=fileFilter)[0]

        # If no file is selected, do nothing
        if self.fileName == "":
            return

        # Loads the file using h5py
        self.f = h5py.File(self.fileName, 'r')
        self.data = self.f['entry/data/data']
        
        self.clearFields()
        self.comboBox.addItems([str(x) for x in range(self.data.shape[0])])
        
        # Shows footer frame (data has been loaded, visualization is now possible)
        self.footerFrame.setEnabled(True)



        # Displays the file's metadata by adding each field to a list widget
        self.listWidget.clear()
        self.listWidget.addItem(f"--> File loaded: \'{self.fileName}\' \n")
        self.listWidget.addItem(f"--> Data info: {self.f['entry/data/data']} \n")
        self.listWidget.addItem(f"--> Data preview:\n{self.f['entry/data/data'][...]} \n")
        self.listWidget.addItem(f"--> Instrument data:")
        for itemName in self.f['entry/instrument/NDAttributes/']:
            item = str(self.f['entry/instrument/NDAttributes/' + itemName][...]).replace('\n', '')
            self.listWidget.addItem("|")
            self.listWidget.addItem(f"|    --> {itemName}: {item}")


    @pyqtSlot()
    def plotData(self):
        '''Slot responsible for opening a new window containing the ImageView widget from pyqtgraph. This
        allows the data to be visualized and manipulated using a graphic user interface.
        
        '''

        if self.fileName.endswith(".hdf"):
            # Creates new window (ui made in qt designer)
            self.plotWindow = DataPlotWindow()
            
            # Creates a layout for the new window and sets it to its central widget
            layout = QtGui.QGridLayout()
            self.plotWindow.centralWidget.setLayout(layout)

            # Creates an ImageView instance
            imv = pg.ImageView(view=pg.PlotItem())

            # Selects which dataset will be plotted (selected from drop-down menu)
            dataIndex = int(self.comboBox.currentText())
            # Sets that dataset as the image to be plotted
            imv.setImage(self.f['entry/data/data'][dataIndex])
            

            # Adds the widget to the window's layout
            layout.addWidget(imv)
            
            # Shows the window
            self.plotWindow.show()

        else:
            QMessageBox.about(self, "Warning", "Visualization for \'.h5\' files not implemented yet.")


    @pyqtSlot()
    def clearFields(self):
        self.listWidget.clear()
        self.footerFrame.setEnabled(False)
        self.comboBox.clear()

        


if __name__ == "__main__":

    app = QApplication([])
    fileReader = FileReaderWindow()
    sys.exit(app.exec_())