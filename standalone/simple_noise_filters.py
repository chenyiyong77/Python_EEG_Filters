from scipy import signal

def filter_data(eeg_data, fs):
    #FILTER CONSTANTS
  fn = fs/2
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


  channel =  eeg_data
  high_passed = signal.filtfilt(b1,a1,channel);        # high pass filter
  low_passed = signal.filtfilt(b,a,high_passed);                # low pass filter
  y = signal.filtfilt(bn,an,low_passed);        # notch filter

  return y