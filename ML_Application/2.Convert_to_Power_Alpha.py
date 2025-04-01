import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.integrate import simps

# Load the CSV file
file_path = 'C:/Users/dataset_from_PiEEG.csv'  # Update with your actual file path
data = pd.read_csv(file_path)

# Ensure only numeric columns are processed
data = data.select_dtypes(include=[np.number])

# Sampling frequency (Hz)
fs = 250  
window_size = 250  # 1-second windows (250 samples)
low_alpha, high_alpha = 8, 13  # Alpha band range (Hz)

# Store alpha power for each channel over time
alpha_powers = {col: [] for col in data.columns}
timestamps = []  # Store timestamps for each segment

# Iterate through 250-sample windows
for start in range(0, len(data), window_size):
    end = start + window_size
    if end > len(data):  # Ensure we don't exceed the dataset
        break

    timestamps.append(start / fs)  # Convert sample index to time in seconds

    for col in data.columns:
        segment = data[col][start:end]

        # Compute Welch's PSD
        freqs, psd = signal.welch(segment, fs, nperseg=window_size)

        # Find alpha range in frequencies
        idx_alpha = np.logical_and(freqs >= low_alpha, freqs <= high_alpha)

        # Compute absolute alpha power (area under the curve)
        freq_res = freqs[1] - freqs[0]  # Frequency resolution
        alpha_power = simps(psd[idx_alpha], dx=freq_res)

        alpha_powers[col].append(alpha_power)

# Convert results to DataFrame
alpha_df = pd.DataFrame(alpha_powers)
alpha_df.insert(0, 'Time (s)', timestamps)  # Insert time column at the beginning

# Save to Excel
excel_filename = 'alpha_power_results.xlsx'
alpha_df.to_excel(excel_filename, index=False)
print(f'Alpha power results saved to {excel_filename}')

# Plot alpha power trends for all channels
plt.figure(figsize=(12, 6))
for col in alpha_df.columns[1:]:  # Skip 'Time (s)'
    plt.plot(alpha_df['Time (s)'], alpha_df[col], label=f'Alpha Power - {col}')

plt.xlabel('Time (s)')
plt.ylabel('Alpha Power (uV^2)')
plt.title('Alpha Rhythm Power Over Time')
plt.legend()
plt.grid()
plt.show()
