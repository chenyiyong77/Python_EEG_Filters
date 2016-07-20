import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D

def choose_filter(type='butterworth'):
	

eeg_data = np.genfromtxt('../Data/single.txt',delimiter=',',dtype='float32')[0:]
print(np.shape(eeg_data))
print(np.shape(eeg_data[1000:1256]))


Fs = 256		# sampling rate
Ts = 1.0/Fs # sampling interval
t = np.arange(0,129)
print(t)
print(len(t))

fft = np.empty([256])
# channel = random.sample(range(-250,250),256)
channel = eeg_data[1000:1256]
#FFT ALGORITHM
temp_fft = np.fft.fft(channel)
temp_fft = np.abs(temp_fft/len(channel))
temp_fft = temp_fft[0:(len(channel)/2 + 1)]
temp_fft[1:len(temp_fft)] = 2*temp_fft[1:len(temp_fft)]
fft = temp_fft
fft[0] = 0
print(fft)
print(np.shape(fft))
fig = plt.figure(1)
plt.yscale('log')
ax = fig.add_subplot(111)
plt.plot(t,fft)

plt.show()
