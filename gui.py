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



class MplCanvas(FigureCanvas):
  def __init__(self, parent=None, width=5, height=4, dpi=100):
      fig = Figure(figsize=(width, height), dpi=dpi)
      FigureCanvas.__init__(self, fig)
      self.setParent(parent)
  
  def update_figure():
    pass

class FilterCanvas(QtGui.QWidget):
  def __init__(self, parent=None, width=5, height=4, dpi=100):
      QtGui.QWidget.__init__(self)
      self.setParent(parent)
      self.layout = QtGui.QGridLayout()
      self.setLayout(self.layout)
      self.filter_types = ["Bandstop", "Bandpass", "Lowpass", "Highpass"]
      self.initialize_widget()

  def initialize_widget(self):

      ## BUTTON
      self.file_button = QtGui.QPushButton("Import File", self)
      self.file_button.setFixedWidth(100)
      self.file_button.clicked.connect(self.parent().open_file_window)


      ## "FILE:" LABEL
      self.file_label = QtGui.QLabel()
      self.file_label.setText("File:")
      self.file_label.setStyleSheet('font-weight:bold')

      ## GROUP OF VERTICAL LINE
      verticalLine0 = QtGui.QFrame()
      verticalLine0.setFrameShape(QtGui.QFrame().HLine)
      verticalLine0.setFrameShadow(QtGui.QFrame().Sunken)
      verticalLine1 = QtGui.QFrame()
      verticalLine1.setFrameShape(QtGui.QFrame().HLine)
      verticalLine1.setFrameShadow(QtGui.QFrame().Sunken)


      ## "FILTERS LABEL"
      filter_labels = QtGui.QLabel()
      filter_labels.setText("Filters")
      filter_labels.setStyleSheet('font-weight:bold')


      ## Create ADD Button
      add_button = QtGui.QPushButton("+", self)
      add_button.setFixedWidth(25)
      add_button.setFixedHeight(25)
      add_button.clicked.connect(self.add_filter)

      # place in layout
      self.file_name_label = QtGui.QLabel()
      self.layout.addWidget(self.file_button,1,0, 1,4)
      self.layout.addWidget(verticalLine0,2,0,1,10)
      self.layout.addWidget(self.file_label,3,0)
      self.layout.addWidget(self.file_name_label,3,1)
      self.layout.addWidget(verticalLine1,4,0,1,10)
      self.layout.addWidget(filter_labels,5,0)
      self.layout.addWidget(add_button,6,0)

  def add_filter(self):
    print("next")
    filter_choice = QtGui.QComboBox()
    for filters in self.filter_types:
      filter_choice.addItem(filters)
    ## create vertical divider
    verticalLine = QtGui.QFrame()
    verticalLine.setFrameShape(QtGui.QFrame().HLine)
    verticalLine.setFrameShadow(QtGui.QFrame().Sunken)
    ## create add button
    add_button = QtGui.QPushButton("+", self)
    add_button.setFixedWidth(25)
    add_button.setFixedHeight(25)
    add_button.clicked.connect(self.add_filter)
    ## add buttons to the layout
    self.layout.addWidget(filter_choice,self.layout.rowCount()-1,0)
    self.layout.addWidget(verticalLine,self.layout.rowCount(),0,1,10)
    self.layout.addWidget(add_button,self.layout.rowCount()+1,0)

class FileWindow(QtGui.QWidget):
  def __init__(self, parent=None, width=5, height=4, dpi=100):
    QtGui.QDialog.__init__(self)
    self.initialize_window()

  def initialize_window(self):
    self.setWindowTitle("File Import")
    self.file_path = ''
    self.local_file_path = ""
    self.file_name = "None"
    self.layout = QtGui.QGridLayout()
    self.setLayout(self.layout)

    window_label = QtGui.QLabel()
    window_label.setText("File Import")
    window_label.setStyleSheet('font-size: 16pt; font-weight:bold')

    self.file_button = QtGui.QPushButton("File", self)
    self.file_button.setFixedWidth(75)
    self.file_button.clicked.connect(self.select_file)


    file_label = QtGui.QLabel()
    file_label.setText("File:")
    file_label.setStyleSheet('font-weight:bold')

    self.file_name_label = QtGui.QLabel()
    self.file_name_label.setText(self.file_name)

    delim_label = QtGui.QLabel()
    delim_label.setText("Delimiter")

    self.delim_entry = QtGui.QLineEdit()
    self.delim_entry.setFixedWidth(40)
    self.delim_entry.setText(',')

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
    self.layout.addWidget(file_label,2,0)
    self.layout.addWidget(self.file_name_label,2,1)
    self.layout.addWidget(delim_label,3,0)
    self.layout.addWidget(self.delim_entry,3,1)
    self.layout.addWidget(start_row_label,4,0)
    self.layout.addWidget(self.start_row_entry,4,1)
    self.layout.addWidget(end_row_label,5,0)
    self.layout.addWidget(self.end_row_entry,5,1)
    self.layout.addWidget(start_col_label,6,0)
    self.layout.addWidget(self.start_col_entry,6,1)
    self.layout.addWidget(end_col_label,7,0)
    self.layout.addWidget(self.end_col_entry,7,1)
    self.layout.addWidget(self.import_button,8,0,1,2)

  def select_file(self):
    # dialog = QtGui.QFileDialog()
    self.local_file_path = QtGui.QFileDialog.getOpenFileName()
    self.file_name = os.path.basename(self.local_file_path)
    self.file_name_label.setText(self.file_name)



  def import_file(self):
    #Errors
    if ((self.local_file_path == '') or (self.start_row_entry.text() is '') or (self.end_row_entry.text() is '') or 
            (self.start_col_entry.text() is '') or (self.end_col_entry.text() is '')) :
      print('empty')
      return 
    if (int(self.start_row_entry.text()) > int(self.end_row_entry.text())) and (int(self.end_row_entry.text())!=-1):
      print('start row > end row error')
      return
    if (int(self.start_col_entry.text()) > int(self.end_col_entry.text())) and (int(self.end_col_entry.text())!=-1):
      print('start col > end row error')
      return
    self.file_path = self.local_file_path;
    window.set_imported_file();
    self.close()


class ApplicationWindow(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    self.setWindowTitle("application main window")

    self.file_menu = QtGui.QMenu('&File', self)
    self.file_menu.addAction('&Import Dataset', self.open_file_window)
    self.menuBar().addMenu(self.file_menu)

    self.help_menu = QtGui.QMenu('&Help', self)
    self.menuBar().addSeparator()
    self.menuBar().addMenu(self.help_menu)

    self.help_menu.addAction('&About', self.about)

    self.main_widget = QtGui.QWidget(self)

    l = QtGui.QVBoxLayout(self.main_widget)
    mpl = MplCanvas(self, width=5, height=4, dpi=100)
    self.fc = FilterCanvas(self,width=5, height=4, dpi=100)
    l.addWidget(self.fc)
    l.addWidget(mpl)

    self.main_widget.setFocus()
    self.setCentralWidget(self.main_widget)

  def open_file_window(self):
    self.fw = FileWindow(self)
    self.fw.setGeometry(QtCore.QRect(100,100,250,300))
    self.fw.show()
    

  def set_imported_file(self):
    self.file_path = self.fw.file_path
    self.file_name = self.fw.file_name
    print(self.file_path)
    print(self.file_name)
    self.fc.file_label.setText(self.file_name)

  def fileQuit(self):
     self.close()

  def closeEvent(self, ce):
     self.fileQuit()

     
  def about(self):
    QtGui.QMessageBox.about(self, "About")


def main():
  global data
  global window
  data = data_processing.EEG_Data()
  # data.data_import('Trial_1.csv',delimiter=',')
  qApp = QtGui.QApplication(sys.argv)
  window = ApplicationWindow()
  window.setWindowTitle("Filters")
  window.show()
  signal.signal(signal.SIGINT, signal.SIG_DFL) #close on exit

  sys.exit(qApp.exec_())

if __name__ == '__main__':
  main()

