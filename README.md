# PiEEG-16
Easy way to neuroscience with low-cost shield PiEEG-16 that allows converting Raspberry Pi to brain-computer interface (EEG device) with opportunity measure 16 channels.     

[Manual](https://pieeg.com/docs/docs/pieeg-16/) for device   
[Manual](https://github.com/pieeg-club/PiEEG-16/blob/main/PiEEG_quick_start.pdf) for quick start  


Measure 16 EEG channels with Shield PiEEG-16 and RaspberryPi

Connect PiEEG-16 and just launch the [script](https://github.com/pieeg-club/PiEEG-16/blob/main/GUI/Graph_Gpio_D%20_1_5_4_not_spike.py) for graph visualization in real-time and the [script](https://github.com/pieeg-club/PiEEG-16/blob/main/Save_data/1.Save_Data.py) to save data.   
and [script](https://github.com/pieeg-club/PiEEG-16/blob/main/Save_data/dataset_visualisation/2.Data_Vis_Graph_All_in_one.py) for saved data for graph visualization (not real-time)   


This project is the result of several years of work on the development of BCI. We believe that the easiest way to get started with biosignals is to use a shield. We will try to reveal the process of reading EEG signals as fully and clearly as possible.

<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/pieeg.jpeg" width="50%" height="50%" alt="generals view">
</p>

#### Warnings
>[!WARNING]
> You are fully responsible for your personal decision to purchase this device and, ultimately, for its safe use. PiEEG is not a medical device and has not been certified by any government regulatory agency for use with the human body. Use it at your own risk.  

>[!CAUTION]
> The device (and all connected equipment as Moniror, RaspberryPI etc ) must operate only from a battery - 5 V. Complete isolation from the mains power is required.! The device MUST not be connected to any kind of mains power, via USB or otherwise.   
> Power supply - only battery 5V, please read the datasheet!!!!!  

Connect the shield to PiEEG and after that connect the device to a battery (power supply) and connect electrodes. Full galvanic isolation from mains is required.
Electrodes are positioned according to the International 10-20 system ​

<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/all.png" width="50%" height="50%" alt="generals view">
</p>

 Artifact test (Dry Electrodes, no Gel) with [Dataset](https://github.com/pieeg-club/PiEEG-16/blob/main/Dataset/2.Chewing_Blinking.xlsx)  

The process of measuring chewing and blinking artifacts using dry electrodes (Fz). Chewing occurred in the following sequence: 4 times, 3 times, 2, and 1 time, and the same for the blinking process. The y-axis is the processed EEG signal after passing filter bands of 1-40 Hz in microvolts and with 250 samples per second
<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/1chewing.bmp" width="50%" height="50%" alt="generals view">
</p>

Alpha test (Dry Electrodes, no Gel, 5-sec eyes closed, 5-sec eyes closed and again) with [Dataset](https://github.com/pieeg-club/PiEEG-16/blob/main/Dataset/3.Alpha_test.xlsx)
     
The process of recording an EEG signal from an electrode (Fz) with eyes open and closed. The y-axis is the processed EEG signal after passing filter bands of 8-12Hz in microvolts and with 250 samples per second

<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/1alpha.bmp" width="50%" height="50%" alt="generals view">
</p>

Alpha test with wavelet (Dry Electrodes, no Gel, 5-sec eyes closed, 5-sec eyes closed and again) with [Dataset](https://github.com/pieeg-club/PiEEG-16/blob/main/Dataset/3.Alpha_test.xlsx)  
<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/alpha.bmp" width="50%" height="50%" alt="generals view">
</p>



Where to use
<p align="center">
  <img src= "https://github.com/pieeg-club/PiEEG-16/blob/main/images/Connection.jpeg" width="80%" height="80%" alt="generals view">
</p>

How to connect  
<p align="center">
  <img src= "https://github.com/pieeg-club/PiEEG-16/blob/main/images/Connection.bmp" width="80%" height="80%" alt="generals view">
</p>

Pins 
<p align="center">
  <img src= "https://github.com/pieeg-club/PiEEG-16/blob/main/images/pins2.bmp" width="80%" height="80%" alt="generals view">
</p>




YouTube video presentation  
<a href="https://youtu.be/tjCazk2Efqs">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/youtube.jpg" width="50%" height="50%" alt="generals view">
</a>



 
#### Citation   
https://pieeg.com/news/pieeg-16-is-availabe-in-the-market/  
arxive paper https://arxiv.org/abs/2409.07491  
Cite: Rakhmatulin, I. (2024). PiEEG-16 to Measure 16 EEG Channels with Raspberry Pi for Brain-Computer Interfaces and EEG devices. arXiv:2409.07491  

#### Contacts
Full support in the [Forum](https://pieeg.com/forum-pieeg-low-cost-brain-computer-interface/)   

[LinkedIn](https://www.linkedin.com/company/96475004/admin/feed/posts/)   
