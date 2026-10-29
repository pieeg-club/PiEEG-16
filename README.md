<div align="center">

# PiEEG-16

**16 channels of EEG on a Raspberry Pi.**

Open-source Raspberry Pi shield for measuring EEG, EMG and ECG with two TI ADS1299 chips.

[📖 Documentation](https://docs.pieeg.com/hardware/devices/pieeg-16/) ·
[🚀 How to Start](https://docs.pieeg.com/hardware/devices/pieeg-16/setup/) ·
[🛒 Buy](https://pieeg.com/) ·
[💬 Discord](https://discord.gg/5Ps24p47)

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_on_pi.jpg" alt="PiEEG-16 shield on a Raspberry Pi" width="420">

</div>

> [!WARNING]
> PiEEG-16 is **not a medical device** and has not been certified by any regulator for use with the human body. It is a tool for research, education and engineering. You use it at your own risk.

> [!CAUTION]
> **Battery only.** The Raspberry Pi, the shield and everything cabled to them (monitor, keyboard) must run from a **5 V power bank** while electrodes are on a person. Never use a wall charger or a mains-powered monitor or computer. The board has **no isolation**. Read the [Safety page](https://docs.pieeg.com/hardware/devices/pieeg-16/safety/) and the [liability notice](https://pieeg.com/liability/).

## At a glance

| | |
|---|---|
| **Channels** | 16 biosignal inputs, plus reference and bias |
| **Converters** | 2 × TI ADS1299, 24-bit, 8 channels each |
| **Sample rate** | 250 SPS (default) |
| **Signals** | EEG, EMG, ECG |
| **Host** | Raspberry Pi 4 or Raspberry Pi 5 |
| **Link to the Pi** | SPI0, one chip select and one DRDY line per chip |
| **Electrodes** | Dry or wet Ag/AgCl, 2.54 mm headers |
| **Power** | 5 V power bank, 3 A, up to 10,000 mAh |
| **Software** | [PiEEG Server](https://github.com/pieeg-club/PiEEG-server) (default device), Python SDK (this repo) |

## How it works

```
 Electrodes 1–8  ─► ADS1299 #1 ─┐
 Electrodes 9–16 ─► ADS1299 #2 ─┼─SPI─► Raspberry Pi ─► PiEEG Server
 Reference + bias (ear clips) ──┘       4 or 5          ├ dashboard :1617
                                          ▲             ├ WebSocket :1616
                  5 V power bank ─────────┘             └ CSV · LSL · OSC
```

The two ADS1299 chips share one SPI bus, each with its own chip select and data-ready line (they are not daisy-chained). PiEEG Server joins them into one 16-channel stream.

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_setup.jpg" alt="PiEEG-16 with a 16-electrode cap" width="500">

## Quick start

1. **Mount** the shield on the Raspberry Pi's 40-pin header (Pi switched off).
2. **Connect** 16 electrodes to channels 1–16, a reference ear clip and a bias ear clip.
3. **Power** the Pi from a 5 V power bank. The LEDs on the shield light up.
4. **Install and run** [PiEEG Server](https://github.com/pieeg-club/PiEEG-server). PiEEG-16 is its default device:

```bash
curl -sSL https://raw.githubusercontent.com/pieeg-club/PiEEG-server/main/install.sh | bash
sudo reboot                          # first time only: enables SPI
pieeg-server                         # same as: pieeg-server --device pieeg16
```

5. **Open** `http://raspberrypi.local:1617`, click **Connect**, close your eyes and watch the alpha rhythm rise at the back of the head.

Full walkthrough: **[docs.pieeg.com → PiEEG-16 → How to Start](https://docs.pieeg.com/hardware/devices/pieeg-16/setup/)**

## Wiring

| Input | Electrode | Purpose |
|---|---|---|
| **Channels 1–8** | EEG electrodes in a cap (read by ADS1299 #1) | Signal |
| **Channels 9–16** | EEG electrodes in a cap (read by ADS1299 #2) | Signal |
| **Reference** | Ear clip on one earlobe | Common 0 µV point for all 16 channels |
| **Bias** | Ear clip on the other earlobe | Cancels common-mode noise (mains hum) |

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_connection.png" alt="Wiring of channels 1–16, reference and bias" width="700">

### Suggested montage

| Ch | Position | Ch | Position |
|---|---|---|---|
| 1 | Fp1 | 9 | F7 |
| 2 | Fp2 | 10 | F8 |
| 3 | C3 | 11 | F3 |
| 4 | C4 | 12 | F4 |
| 5 | P7 | 13 | T7 |
| 6 | P8 | 14 | T8 |
| 7 | O1 | 15 | P3 |
| 8 | O2 | 16 | P4 |

### Raspberry Pi pinout

| Header pin | GPIO | Signal | Chip |
|---|---|---|---|
| 19 | GPIO 10 | SPI0 MOSI | Both |
| 21 | GPIO 9 | SPI0 MISO | Both |
| 23 | GPIO 11 | SPI0 SCLK | Both |
| 24 | GPIO 8 | SPI0 CE0 | #1 (ch 1–8) |
| 35 | GPIO 19 | Chip select, driven by software | #2 (ch 9–16) |
| 37 | GPIO 26 | DRDY 1 | #1 |
| 33 | GPIO 13 | DRDY 2 | #2 |

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_pinout.png" alt="PiEEG-16 SPI, chip-select and DRDY pins on the 40-pin header" width="600">

## Software

| | Best for |
|---|---|
| **[PiEEG Server](https://github.com/pieeg-club/PiEEG-server)** (recommended) | Browser dashboard, recording, WebSocket, LSL, VRChat OSC, webhooks |
| **Python SDK** (this repo) | Learning how two ADS1299 chips work together, raw data, custom register settings |

> [!NOTE]
> BrainFlow's `PIEEG_BOARD` supports the 8-channel PiEEG only. To use PiEEG-16 with OpenViBE, MNE or BCI2000, stream it from PiEEG Server over LSL (`pieeg-server --lsl`).

### Python SDK scripts

| Script | What it does |
|---|---|
| [`GUI/pieeg16_drdy_only.py`](GUI/pieeg16_drdy_only.py) | **Start here.** Live 16-channel graph, each chip read on its own DRDY line |
| [`GUI/2.Graph_Gpio_D _1_5_4_OS.py`](GUI) | Alternative live graph that opens `/dev/gpiochip4` |
| [`Save_data/Save_data_OS.py`](Save_data/Save_data_OS.py) | Save raw µV for all 16 channels to Excel |
| [`Save_data/1.Save_Data.py`](Save_data/1.Save_Data.py) | Save to Excel with a live graph |
| [`Save_data/command_line/pieeg_to_csv.py`](Save_data/command_line) | Command-line CSV recorder (duration, rate, gain) |
| [`Save_data/dataset_visualisation`](Save_data/dataset_visualisation) | Plot saved files; alpha-band wavelet view |
| [`Dataset/Remove_Spikes.py`](Dataset/Remove_Spikes.py) | Remove SPI glitch spikes from a saved file |

**Install** (recent Raspberry Pi OS needs a virtual environment):

```bash
python3 -m venv --system-site-packages ~/pieeg-env
source ~/pieeg-env/bin/activate
pip install spidev matplotlib scipy pandas openpyxl gpiod==1.5.4
```

**Run:**

```bash
cd GUI
python pieeg16_drdy_only.py
```

> [!TIP]
> `pieeg16_drdy_only.py` opens GPIO chip `"0"`. On a Raspberry Pi 5, run `gpiodetect` and use the chip labelled `pinctrl-rp1` (`gpiochip0` on current Raspberry Pi OS, `gpiochip4` on older releases). Change the `gpiod.chip(...)` line if needed.

Details, troubleshooting and the data format: **[Software docs](https://docs.pieeg.com/hardware/devices/pieeg-16/software/)** · **[Specification](https://docs.pieeg.com/hardware/devices/pieeg-16/specification/)**

## Example signals

All recorded with **dry electrodes, no gel**, at 250 SPS.

**EEG: alpha test** (eyes closed 5 s / open 5 s, filtered 8–12 Hz) · [dataset](Dataset/3.Alpha_test.xlsx)

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_alpha.png" alt="16 channels of alpha-band EEG" width="700">

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_alpha_wavelet.png" alt="Alpha test with wavelet transform" width="700">

**EEG: chewing and blinking** (4-3-2-1 times, filtered 1–40 Hz) · [dataset](Dataset/2.Chewing_Blinking.xlsx)

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_artifacts.png" alt="Chewing and blinking artifacts on 16 channels" width="700">

## Where to use

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_applications.jpg" alt="PiEEG-16 applications: robotic arm, computer, exoskeleton, drone, toy car" width="700">

## 3D-printed headset case

A case for **Raspberry Pi 5 + PiEEG-16** that mounts on the 3D-printable IronBCI headset. Files and print settings in [`3D_Print_Headset_Case`](3D_Print_Headset_Case).

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_case_open.jpg" alt="Raspberry Pi 5 and PiEEG-16 in the printed case" width="300"> <img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/pieeg16_case_mounted.jpg" alt="Case mounted on the headset" width="300">

## What's in this repository

| Folder | Content |
|---|---|
| [`GUI`](GUI) | Live 16-channel graphs (older versions in `arxive`) |
| [`Save_data`](Save_data) | Save to Excel, command-line CSV recorder, visualisation scripts |
| [`Dataset`](Dataset) | Chewing/blinking and alpha-test recordings (16 ch, dry electrodes, 250 SPS), spike-removal script |
| [`ML_Application`](ML_Application) | Machine-learning example: record → alpha power → classifier; OpenClaw home brain-station project |
| [`3D_Print_Headset_Case`](3D_Print_Headset_Case) | STL files for a Pi 5 + PiEEG-16 headset case |
| [`User_Projects`](User_Projects) | Share your own project here |
| [`images`](images) | Images used in the original README |
| [`PiEEG_quick_start.pdf`](PiEEG_quick_start.pdf) | Printable quick-start manual |

## Documentation

| Page | |
|---|---|
| [PiEEG-16 Intro](https://docs.pieeg.com/hardware/devices/pieeg-16/) | Overview, comparison with PiEEG-8 |
| [What's in the Box](https://docs.pieeg.com/hardware/devices/pieeg-16/required-equipment/) | What you need besides the shield, 3D case |
| [How to Start](https://docs.pieeg.com/hardware/devices/pieeg-16/setup/) | Step-by-step setup and first signal checks |
| [Electrodes & Pinout](https://docs.pieeg.com/hardware/devices/pieeg-16/connections/) | Wiring, 16-channel montage, GPIO pins |
| [Software](https://docs.pieeg.com/hardware/devices/pieeg-16/software/) | PiEEG Server, Python SDK, data tools |
| [Signals & Datasets](https://docs.pieeg.com/hardware/devices/pieeg-16/examples/) | Example recordings, datasets, ML example |
| [Specification](https://docs.pieeg.com/hardware/devices/pieeg-16/specification/) | Data frames, µV conversion, ADS1299 registers |
| [Troubleshooting](https://docs.pieeg.com/hardware/devices/pieeg-16/troubleshooting/) | Fixes for SPI, GPIO, software and noise |
| [Safety](https://docs.pieeg.com/hardware/devices/pieeg-16/safety/) | Battery-only operation and responsible use |

## Citation

If you use PiEEG-16 in research, please cite:

```
I. Rakhmatulin. PiEEG-16 to Measure 16 EEG Channels with Raspberry Pi for
Brain-Computer Interfaces and EEG devices. arXiv:2409.07491, 2024.
```

## Contact

- 🌐 [pieeg.com](https://pieeg.com/)
- 📖 [docs.pieeg.com](https://docs.pieeg.com/)
- 💬 [Discord](https://discord.gg/5Ps24p47)
- ✉️ [pieeg@pieeg.com](mailto:pieeg@pieeg.com)
