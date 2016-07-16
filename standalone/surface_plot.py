import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
np.set_printoptions(threshold=np.inf)


## Import Data from file
eeg_data = np.genfromtxt('../Data/single.txt',delimiter=',',dtype='float32')[0:]

## CONSTANTS
MAX_AMP = 10    		# maximum amplitude to plot
Fs = 256				# sampling rate
Fn = (Fs//2)				# Nyquist frequency
Ts = 1.0/Fs     		# sampling interval
window = 256			# window for fft (how many samples to perform the fft on)
resolution = 512
# Trim the eeg_data to get even windows of resolution
eeg_data = eeg_data[:len(eeg_data)- (len(eeg_data)%resolution)]
x = np.arange(0,Fn + 1) # FFT plot x-axis (range of frequencies -> 0 to Nyquist)
y = np.linspace(0,len(eeg_data)/resolution,num=len(eeg_data)/resolution) #the time axis (x-axis)
print(np.shape(x))
print(np.shape(y))


#################
# Function: Clip
# ---------------
# Sets all values greater than "amplitude_threshold" to this threshold.
# This function is used to make sure that the plot does not extend past
# the maximum you would want to plot_surface

def clip(data):
	for i,pt in enumerate(data):
		if pt > MAX_AMP or pt < -(MAX_AMP):
			data[i] = MAX_AMP
	return data


#############################
# Function: generate_spectrum
# ----------------------------
# Function generates the fft of each window along the graph and 
#
def generate_spectrum(eeg_data):
	fft = np.empty(((len(eeg_data)//resolution),Fn+1),dtype='float32') 
	for i in range(0,len(eeg_data)-window,resolution):
		temp_window = eeg_data[i:i+256]
		temp_fft = np.fft.fft(temp_window)
		temp_fft = np.abs(temp_fft/len(temp_window))
		temp_fft = temp_fft[0:Fn + 1]
		temp_fft[1:len(temp_fft)] = 2*temp_fft[1:len(temp_fft)]
		fft[i//resolution - 1] = clip(temp_fft)
	return fft

# Plotting
X,Y = np.meshgrid(x, y)
Z = generate_spectrum(eeg_data)
print(np.shape(X))
print(np.shape(Y))
print(np.shape(Z))

fig = plt.figure()
ax = fig.gca(projection='3d')               # 3d axes instance
# ax.set_title('EEG Surface Plot')        # title
surf = ax.plot_surface(X, Y, Z,             # data values (2D Arryas)
                       rstride=2,           # row step size
                       cstride=2,           # column step size
                       cmap=cm.viridis,        # color map
                       linewidth=1,
                       antialiased=True)
ax.set_title('EEG Spectrum' )
ax.set_xlim(0,Fn)
ax.set_ylim(0,len(Z))
ax.set_zlim(0,MAX_AMP)        # title
ax.set_xlabel('Frequency (Hz)' )
ax.set_ylabel( 'Time' )
ax.set_zlabel( 'Amplitude (uV)' )
fig.colorbar(surf, shrink=0.5, aspect=5)     # colour bar
plt.show()
