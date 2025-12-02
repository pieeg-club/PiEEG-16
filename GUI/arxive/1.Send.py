import spidev
import time
import gpiod
from matplotlib import pyplot as plt
from scipy import signal

# -----------------------------
# GPIO and SPI Setup
# -----------------------------
DRDY_PIN = 26     # DRDY from first ADS1299
CS_PIN = 19       # Chip select
SPI_BUS = 0
SPI_DEVICE = 0

chip = gpiod.Chip("/dev/gpiochip4")

# Request CS line
cs_line = chip.get_line(CS_PIN)
cs_req = gpiod.line_request()
cs_req.consumer = "SPI_CS"
cs_req.request_type = gpiod.line_request.DIRECTION_OUTPUT
cs_line.request(cs_req)
cs_line.set_value(1)  # CS idle high

# Request DRDY line
drdy_line = chip.get_line(DRDY_PIN)
drdy_req = gpiod.line_request()
drdy_req.consumer = "DRDY"
drdy_req.request_type = gpiod.line_request.DIRECTION_INPUT
drdy_line.request(drdy_req)

# SPI setup
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 1000000
spi.mode = 0b01
spi.bits_per_word = 8

# -----------------------------
# ADS1299 Commands and Registers
# -----------------------------
CMD_WAKEUP = 0x02
CMD_STANDBY = 0x04
CMD_RESET = 0x06
CMD_START = 0x08
CMD_STOP = 0x0A
CMD_RDATAC = 0x10
CMD_SDATAC = 0x11
CMD_RDATA = 0x12

CONFIG1 = 0x01
CONFIG2 = 0x02
CONFIG3 = 0x03
CH1SET = 0x05
CH2SET = 0x06
CH3SET = 0x07
CH4SET = 0x08
CH5SET = 0x09
CH6SET = 0x0A
CH7SET = 0x0B
CH8SET = 0x0C

DATA_MASK = 0x7FFFFF

# -----------------------------
# Helper Functions
# -----------------------------
def send_command(cmd):
    cs_line.set_value(0)
    spi.xfer2([cmd])
    cs_line.set_value(1)

def write_register(register, value):
    cs_line.set_value(0)
    spi.xfer2([0x40 | register, 0x00, value])
    cs_line.set_value(1)

def read_data():
    """Read all 16 channels from 2 daisy-chained ADS1299 chips"""
    cs_line.set_value(0)
    raw = spi.xfer2([0]*54)  # 3 bytes per channel * 8 channels * 2 chips
    cs_line.set_value(1)

    results = []
    for chip_idx in range(2):
        chip_data = []
        offset = chip_idx * 27
        for ch in range(8):
            idx = offset + 3 + ch*3  # skip first 3 status bytes
            value = (raw[idx] << 16) | (raw[idx+1] << 8) | raw[idx+2]
            if value & 0x800000:  # negative number handling
                value -= 0x1000000
            voltage = value * 4.5 / 0x7FFFFF  # in volts
            chip_data.append(voltage)
        results.extend(chip_data)
    return results

# -----------------------------
# Initialize ADS1299
# -----------------------------
for cmd in [CMD_WAKEUP, CMD_STOP, CMD_RESET, CMD_SDATAC]:
    send_command(cmd)
    time.sleep(0.05)

# Example configuration (all channels enabled)
for ch in range(CH1SET, CH8SET+1):
    write_register(ch, 0x00)

# Config registers
write_register(CONFIG1, 0x96)
write_register(CONFIG2, 0xD4)
write_register(CONFIG3, 0xFF)

send_command(CMD_RDATAC)
send_command(CMD_START)

# -----------------------------
# Plot setup
# -----------------------------
sample_len = 250
fig, axes = plt.subplots(4, 4, figsize=(10, 8))
plt.subplots_adjust(hspace=0.5)
data_buffers = [[0]*sample_len for _ in range(16)]

# -----------------------------
# Main Loop
# -----------------------------
axis_x = 0
fps = 250
highcut = 1
lowcut = 10

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    b, a = signal.butter(order, [lowcut/nyq, highcut/nyq], btype='band')
    return signal.filtfilt(b, a, data)

print("Starting data acquisition... Press Ctrl+C to stop.")
try:
    while True:
        # Wait for DRDY falling edge
        if drdy_line.get_value() == 0:
            voltages = read_data()  # list of 16 channel voltages

            # update buffers
            for ch in range(16):
                data_buffers[ch].append(voltages[ch])
                if len(data_buffers[ch]) > sample_len:
                    data_buffers[ch].pop(0)

            # Plotting
            for ch in range(16):
                row = ch // 4
                col = ch % 4
                axes[row, col].cla()
                axes[row, col].plot(range(len(data_buffers[ch])), data_buffers[ch])
                axes[row, col].set_title(f"Ch {ch+1}")
                axes[row, col].set_ylim([-5,5])
            plt.pause(0.001)
            axis_x += 1

except KeyboardInterrupt:
    print("Stopping acquisition...")
    send_command(CMD_STOP)
    spi.close()
