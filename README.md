# PiEEG-16
Measure 16 EEG channels with Shield PiEEG-16 and RaspberryPi

Connect PiEEG-16 and just launch the [script](https://github.com/pieeg-club/PiEEG-16/blob/main/GUI/1.Graph.Py) for graph visualization in real-time and the [script](https://github.com/pieeg-club/PiEEG-16/blob/main/Save_data/1.Save_Data.py) to save data.   
and [script](https://github.com/pieeg-club/PiEEG-16/blob/main/Save_data/2.Data_Vis_Graph_All_in_one.py ) for graph visualization   


This project is the result of several years of work on the development of BCI. We believe that the easiest way to get started with biosignals is to use a shield. We will try to reveal the process of reading EEG signals as fully and clearly as possible.

<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/pieeg.jpeg" width="50%" height="50%" alt="generals view">
</p>

#### Warnings
>[!WARNING]
> You are fully responsible for your personal decision to purchase this device and, ultimately, for its safe use. PiEEG is not a medical device and has not been certified by any government regulatory agency for use with the human body. Use it at your own risk.  

>[!CAUTION]
> The device must operate only from a battery - 5 V. Complete isolation from the mains power is required.! The device MUST not be connected to any kind of mains power, via USB or otherwise.   
> Power supply - only battery 5V, please read the datasheet!!!!!  

#### Artifact test
The process of measuring chewing and blinking artifacts using dry electrodes (Fz). Chewing occurred in the following sequence: 4 times, 3 times, 2, and 1 time, and the same for the blinking process. The y- axis is the processed EEG signal after passing filter bands of 1-40 Hz in microvolts and with 250 samples per second
<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/1chewing.bmp" width="50%" height="50%" alt="generals view">
</p>

####Alpha test
The process of recording an EEG signal from an electrode (Fz) with eyes open and closed. The y- axis is the processed EEG signal after passing filter bands of 8-12Hz in microvolts and with 250 samples per second

<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/1alpha.bmp" width="50%" height="50%" alt="generals view">
</p>


