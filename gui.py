from PyQt4 import QtGui, QtCore
import matplotlib as mpl
mpl.use("Qt4Agg")
import sys, os
from numpy import linspace
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import data_processing
import signal



class MyMplCanvas(FigureCanvas):
  def __init__(self, parent=None, width=5, height=4, dpi=100):
      fig = Figure(figsize=(width, height), dpi=dpi)
      # self.axes = fig.add_subplot(111)
      # self.axes.hold(False)
      FigureCanvas.__init__(self, fig)
      self.setParent(parent)

      # FigureCanvas.setSizePolicy(self,
      #                            QtGui.QSizePolicy.Expanding,
      #                            QtGui.QSizePolicy.Expanding)
      # FigureCanvas.updateGeometry(self)
  #     self.compute_initial_figure()

  
  # def compute_initial_figure(self):
  #   filtered_eeg = data.get_data()
  #   x = linspace(0,len(filtered_eeg[0]), 
  #                   num=len(filtered_eeg[0]), dtype=int)
  #   y = filtered_eeg[0]
  #   self.axes.plot(x,y)
  
  def update_figure():
    pass

class FilterCanvas():
  def __init__(self, parent=None, width=5, height=4, dpi=100):
      fig = Figure(figsize=(width, height), dpi=dpi)
      self.axes = fig.add_subplot(111)
      self.axes.hold(False)
      FigureCanvas.__init__(self, fig)
      self.setParent(parent)

      FigureCanvas.setSizePolicy(self,
                                 QtGui.QSizePolicy.Expanding,
                                 QtGui.QSizePolicy.Expanding)
      FigureCanvas.updateGeometry(self)

class FileWindow(QtGui.QWidget):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
      QtGui.QWidget.__init__(self)
      self.setWindowTitle("File Import")
      self.file_path = ""
      self.file_name = "None"
      self.layout = QtGui.QGridLayout()
      self.setLayout(self.layout)

      window_label = QtGui.QLabel()
      window_label.setText("File Import")
      window_label.setStyleSheet('font-size: 16pt; font-weight:bold')


      self.file_button = QtGui.QPushButton("File", self)
      self.file_button.setFixedWidth(75)
      self.file_button.clicked.connect(self.select_file)
      
      self.file_label = QtGui.QLabel()
      self.file_label.setText(self.file_name)


      delim_label = QtGui.QLabel()
      delim_label.setText("Delimiter")

      self.delim_entry = QtGui.QLineEdit()
      self.delim_entry.setFixedWidth(40)

      start_row_label = QtGui.QLabel()
      start_row_label.setText("Start Row")

      self.start_row_entry = QtGui.QLineEdit()
      self.start_row_entry.setFixedWidth(40)
      self.start_row_entry.setText("1")

      end_row_label = QtGui.QLabel()
      end_row_label.setText("End Row")

      self.end_row_entry = QtGui.QLineEdit()
      self.end_row_entry.setFixedWidth(40)
      self.end_row_entry.setText("-1")

      start_col_label = QtGui.QLabel()
      start_col_label.setText("Start Column")
      self.start_col_entry = QtGui.QLineEdit()
      self.start_col_entry.setFixedWidth(40)
      self.start_col_entry.setText("1")


      end_col_label = QtGui.QLabel()
      end_col_label.setText("End Column")
      self.end_col_entry = QtGui.QLineEdit()
      self.end_col_entry.setFixedWidth(40)
      self.end_col_entry.setText("-1")


      self.import_button = QtGui.QPushButton("Import")
      self.import_button.clicked.connect(self.import_file)


      self.layout.addWidget(window_label,0,0,1,2)
      self.layout.addWidget(self.file_button,1,0)
      self.layout.addWidget(self.file_label,1,1)
      self.layout.addWidget(delim_label,2,0)
      self.layout.addWidget(self.delim_entry,2,1)
      self.layout.addWidget(start_row_label,3,0)
      self.layout.addWidget(self.start_row_entry,3,1)
      self.layout.addWidget(end_row_label,4,0)
      self.layout.addWidget(self.end_row_entry,4,1)
      self.layout.addWidget(start_col_label,5,0)
      self.layout.addWidget(self.start_col_entry,5,1)
      self.layout.addWidget(end_col_label,6,0)
      self.layout.addWidget(self.end_col_entry,6,1)
      self.layout.addWidget(self.import_button,7,0,1,2)

    def select_file(self):
      self.file_path = QtGui.QFileDialog.getOpenFileName()
      self.file_name = os.path.basename(self.file_path)
      print(self.file_path)
      print(self.file_name)
      self.file_label.setText(self.file_name)

    def import_file(self):
      #TODO
      # check if all of the fields have been selected
      print("FILE SET!")
    # def create_child(self):
    #     # here put the code that creates the new window and shows it.
    #    child = FileWindow(self)
    #    child.show()


class ApplicationWindow(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    self.setWindowTitle("application main window")

    self.file_menu = QtGui.QMenu('&File', self)
    self.file_menu.addAction('&Import Dataset', self.open_file_window,
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
  
  def open_file_window(self):
    self.fw = FileWindow()
    self.fw.setGeometry(QtCore.QRect(100,100,250,300))
    self.fw.show()
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
  signal.signal(signal.SIGINT, signal.SIG_DFL) #close on exit

  sys.exit(qApp.exec_())

if __name__ == '__main__':
  main()

