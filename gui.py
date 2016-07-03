from PyQt4 import QtGui, QtCore
import matplotlib as mpl
mpl.use("Qt4Agg")
import sys
from numpy import linspace
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import data_processing


class MyMplCanvas(FigureCanvas):
  def __init__(self, parent=None, width=5, height=4, dpi=100):
      fig = Figure(figsize=(width, height), dpi=dpi)
      self.axes = fig.add_subplot(111)
      # We want the axes cleared every time plot() is called
      self.axes.hold(False)
      FigureCanvas.__init__(self, fig)
      self.setParent(parent)

      FigureCanvas.setSizePolicy(self,
                                 QtGui.QSizePolicy.Expanding,
                                 QtGui.QSizePolicy.Expanding)
      FigureCanvas.updateGeometry(self)
      self.compute_initial_figure()

  
  def compute_initial_figure(self):
    filtered_eeg = data.get_data()
    x = linspace(0,len(filtered_eeg[0]), 
                    num=len(filtered_eeg[0]), dtype=int)
    y = filtered_eeg[0]
    self.axes.plot(x,y)
  
  def update_figure():
    pass

class ApplicationWindow(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    self.setWindowTitle("application main window")

    self.file_menu = QtGui.QMenu('&File', self)
    self.file_menu.addAction('&Quit', self.fileQuit,
                             QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
    self.menuBar().addMenu(self.file_menu)

    self.help_menu = QtGui.QMenu('&Help', self)
    self.menuBar().addSeparator()
    self.menuBar().addMenu(self.help_menu)

    self.help_menu.addAction('&About', self.about)

    self.main_widget = QtGui.QWidget(self)

    l = QtGui.QVBoxLayout(self.main_widget)
    sc = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)
    l.addWidget(sc)

    self.main_widget.setFocus()
    self.setCentralWidget(self.main_widget)
  def fileQuit(self):
     self.close()

  def closeEvent(self, ce):
     self.fileQuit()

     
  def about(self):
    QtGui.QMessageBox.about(self, "About")


def main():
  global data
  data = data_processing.EEG_Data()
  data.data_import('Trial_1.csv',delimiter=',')
  qApp = QtGui.QApplication(sys.argv)
  window = ApplicationWindow()
  window.setWindowTitle("Filters")
  window.show()
  sys.exit(qApp.exec_())

if __name__ == '__main__':
  main()

