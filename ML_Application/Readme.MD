# How to Use Machine Learning to Stress Control 

If you want to create an EEG-based classifier for machine learning, here’s a short guide:

#### 1. Collect EEG Datasets:

Use Script [1.Save_Data.py](https://github.com/pieeg-club/PiEEG-16/blob/main/ML_Application/1.Save_Data.py)  to collect raw EEG data.





Data has the next Format in the Excel File (example of dataset)

<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/Collected_dataset.jpg" alt="generals view">
</p>

You need (as an example), gather 50 datasets (1 minute or more each) for stress and 50 datasets (1 minute or more each) for no stress conditions.  

#### 2. Compute Power in Key Frequency Bands:
It is not good to just use raw data for ML, so via the next script [2.Convert_to_Power_Alpha.py](https://github.com/pieeg-club/PiEEG-16/blob/main/ML_Application/2.Convert_to_Power_Alpha.py) you can convert all your dataset. 

You need calculate power in the alpha (or beta, delta, and theta) frequency for all 100 datasets. 
We chose a 1 sec length to calculate power in alpha. 
Now we have 50 dataset Power in Alpha with stress and 50 dataset Power in Alpha - not stress 

#### 3. Prepare the Data for ML
Combine the 100 datasets and create two separate Excel files for stress and not stress. But the most important moment here is that we should indicate that we should add an additional column that will indicate the record number (entry number or subject number)
It should looks like that 


#### 4. Train the Classifier:

Use the ML script [3.ML.py](https://github.com/pieeg-club/PiEEG-16/blob/main/ML_Application/3.ML.py) to train a model and classify stress levels based on EEG data.

🚀 Enjoy building your classifier!







