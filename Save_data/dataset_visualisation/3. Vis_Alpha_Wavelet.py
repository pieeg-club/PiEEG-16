import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy import signal

# Load the CSV file
file_path = 'C:/Users/3.Alpha_test.xlsx'  # Update with your actual file path

# Load the CSV file
data = pd.read_excel(file_path)

# Define the band-pass filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Parameters for the band-pass filter
lowcut = 8   # Low cutoff frequency (in Hz)
highcut = 12 # High cutoff frequency (in Hz)
fs = 250.0    # Sampling frequency (in Hz)

# Apply the filter to each channel
filtered_data = data.copy()
for column in data.columns:
    filtered_data[column] = bandpass_filter(data[column], lowcut, highcut, fs)
plt.figure(figsize=(15, 8))


def wavelet(eeg_signal, channel):
  fs = 250
  wavelet = 'cmor'  # Complex Morlet wavelet
  scales = np.arange(1, 32)  #  128 Scale range
  coefficients, frequencies = pywt.cwt(eeg_signal, scales, wavelet, sampling_period=1/fs)

  plt.figure(figsize=(12, 6))
  plt.subplot(2, 1, 1)
  plt.plot(eeg_signal)

  #plt.plot(marker_level,label='Marker, high - Closed, low - Open')
  plt.legend(loc = "lower left") #upper

  plt.title('Original EEG Signal ' + channel)
  plt.xlabel('Time (s)')
  plt.ylabel('Amplitude')

  # Plot the wavelet transform
  plt.subplot(2, 1, 2)
  plt.imshow(np.abs(coefficients), aspect='auto') # , extent=[t[0], t[-1], scales[-1], scales[0]], cmap='jet'

  plt.title('Wavelet Transform ' + channel)
  #plt.plot(marker_level,label='Marker, high - activity, low - rest')
  plt.legend(loc = "lower left") #upper

  plt.xlabel('Time (s)')
  plt.ylabel('Scale')
  plt.yscale('log')  # Use a logarithmic scale for better visualization
  plt.colorbar(label='Magnitude')

  plt.tight_layout()
  plt.show()

channel_0 = "Ch 0"
channel_1 = "Ch 1"
channel_2 = "Ch 2"
channel_3 = "Ch 3"

wavelet(filtered_data["data_1ch_test"], channel_0)
wavelet(filtered_data["data_2ch_test"], channel_1)
wavelet(filtered_data["data_3ch_test"], channel_2)
wavelet(filtered_data["data_4]ch_test"], channel_3)
