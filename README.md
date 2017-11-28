# Mini-Self-Driving-Car
Python version 3.4.3
Dependencies
--NumPy version 1.11.2

--Pillow version 3.4.2

--PyBluez version 0.22

--PySerial version 3.2.1

--Additionally, Android app 'IPWebcam'

Hardware Used:

  1. Arduino Uno
  2. HC05 Bluetooth Module
  3. TowerPro MG995 Servo Motor
  4. BO type DC motor
  5. Power derived from 1000mAh Lithium Polymer Battery
  6. L298 Motor Driver module

Codes:

1. Data Acquisition:
	1. ard_training.ino contains the code for Arduino during the training phase
	2. image_and_data_sync.py contains the Python code for acquiring data (Images through WiFi and command through Serial Communication).
2. Training:
	1. main1.py contains the code for training the FNN by importing NN class from nnClass1.py
	2. nnClass1.py contains the NN class, wg\hich contains the functions sigmoid, lossFunc, initWeights, trainNN, forwadPass.
3. Driving:
	1. usingBluetooth contains the code for autonomous driving using Bluetooth. It imports the class NN from nnClass1.py and uses the 				 function forwardPass to get the output class.
