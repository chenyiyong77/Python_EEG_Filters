import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import argparse

np.set_printoptions(threshold=np.nan)
parser = argparse.ArgumentParser(description='Python EEG Filters')
parser.add_argument('--file', '-f')
parser.add_argument('--delim', '-d')


args = parser.parse_args()
file = args.file
delim = args.delim
print(file)
print(type(file))

eeg_data = np.genfromtxt(file,delimiter=delim,dtype='float32')[0:]
eeg_data = eeg_data[:,7:9]


fs = 250
fn = 125
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
# print(len(eeg_data[0]))
for i in range(len(eeg_data[0])):
  channel =  eeg_data[:,i]
  # print(np.shape(channel))
  # high_passed = signal.filtfilt(b1,a1,channel);        # high pass filter
  low_passed = signal.filtfilt(b,a,channel);                # low pass filter
  y = signal.filtfilt(bn,an,low_passed);        # notch filter
  filtered_eeg.append(y);
# plt.figure(1)

# # for channel in filtered_eeg:
# #   plt.subplot(411)
# #   plt.plot(x,channel)
# #   plt.axis([x_low,x_high,y_low,y_high])
# spec1 = plt.subplot(211)
# print(filtered_eeg[0])
# print(filtered_eeg[1])
# plt.specgram(filtered_eeg[0],Fs=250)
# spec2 = plt.subplot(212)
# plt.specgram(filtered_eeg[1],Fs=250)
# plt.show()
