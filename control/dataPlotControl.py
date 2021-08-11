import sys
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow


# Plot window class: used to visualize hdf/h5 data
class DataPlotWindow(QMainWindow):
    
    def __init__(self):
        super(DataPlotWindow, self).__init__()
        uic.loadUi("../ui/dataPlot.ui", baseinstance=self)
        # self.show() # Uncomment only for testing (execute this file directly)



        

# # Uncomment only for testing (execute this file directly)
# if __name__ == "__main__":

#     app = QApplication([])
#     dataHistogram = DataPlotWindow()
#     sys.exit(app.exec_())