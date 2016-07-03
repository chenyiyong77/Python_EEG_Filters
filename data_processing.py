import numpy as np
from scipy import signal


class EEG_Data:
  def __init__(self):
    self.filters = Filters()
  # DATA IMPORT
  def data_import(self,filename,delimiter=None,R1=1,R2=None,C1=1,C2=None):
    path = 'Data/' + filename
    eeg_data = np.genfromtxt(path,delimiter=delimiter,dtype='float32')[0:]
    if R2 is None:
      R2 = len(eeg_data)
    if C2 is None:
      C2 = len(eeg_data[0])
    self.eeg_data = eeg_data[(R1-1):(R2+1),(C1-1):(C2+1)]

  def get_data(self):
    return self.filters.filter_data(self.eeg_data)


class Filters:
  def __init__(self):
    self.fs = 250                 # Sampling frequency
    self.fn = self.fs/2           # Nyquist frequency

  def filter_data(self,eeg_data):
    #FILTER CONSTANTS
    fs = self.fs
    fn = self.fn
    filter_order = 2   #2nd order filter
    f_high = 50
    f_low = 5
    wn = [59,61]       #Nyquist filter window

    [b,a] = signal.butter(filter_order,f_high/fn, 'low')
    [b1,a1] = signal.butter(filter_order,f_low/fn, 'high')
    [bn,an] = signal.butter(4,[x/fn for x in wn], 'stop')

    filtered_eeg = []
    spectogram = []
    notched = []
    high_passed = []
    low_passed = []
    print(eeg_data)
    for i in range(len(eeg_data[0])):
      channel =  eeg_data[:,i]
      high_passed = signal.filtfilt(b1,a1,channel);        # high pass filter
      low_passed = signal.filtfilt(b,a,high_passed);                # low pass filter
      y = signal.filtfilt(bn,an,low_passed);        # notch filter
      filtered_eeg.append(y);
    self.filtered_eeg = filtered_eeg
    return filtered_eeg


# if __name__ == '__main__':
#   main()