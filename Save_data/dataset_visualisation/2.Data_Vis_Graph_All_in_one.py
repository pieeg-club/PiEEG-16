import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Load the CSV file
file_path = 'C:/Users/3.Alpha_test.xlsx'  # Update with your actual file path
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
highcut = 12.0 # High cutoff frequency (in Hz)
fs = 250.0     # Sampling frequency (in Hz)

# Apply the filter to each channel
filtered_data = data.copy()
for column in data.columns:
    filtered_data[column] = bandpass_filter(data[column], lowcut, highcut, fs)

# Plot the original and filtered data for each channel in a 4x4 grid
fig, axs = plt.subplots(4, 4, figsize=(20, 15))
axs = axs.flatten()  # Flatten the 2D array of axes to iterate easily

for i, column in enumerate(data.columns):
    #axs[i].plot(data[column], label=f'Original {column}', alpha=0.5)
    axs[i].plot(filtered_data[column], label=f'Filtered {column}', linestyle='--')
    axs[i].set_title(f'Channel {column}')
    axs[i].set_xlabel('Sample Index')
    axs[i].set_ylabel('Amplitude')
    axs[i].legend()

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
