import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Load the CSV file
file_path = 'C:/Users/1.Chewing_Blinking.xlsx'  # Update with your actual file path
print("ok")
data = pd.read_excel(file_path)

print (data)
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


plt.plot(data["data_1ch_test"], label=f'Original {column}', alpha=0.5)  # replace the Ch
plt.plot(filtered_data["data_1ch_test"], label=f'Original {column}', alpha=0.5)


plt.title('Original')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.legend()
plt.show()


    
