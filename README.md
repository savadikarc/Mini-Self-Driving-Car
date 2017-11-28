# Mini-Self-Driving-Car
Python version 3.4.3
Dependencies
--NumPy version 1.11.2

--Pillow version 3.4.2

--PyBluez version 0.22

--PySerial version 3.2.1

Hardware Used:

  1. Arduino Uno
  2. HC05 Bluetooth Module
  3. TowerPro MG995 Servo Motor
  4. BO type DC motor
  5. Power derived from 1000mAh Lithium Polymer Battery
  6. L298 Motor Driver module

The codes have been written in Python 3.4.3 

A free Android app called 'IPWebcam' has been used to capture images. IPWebcam captures images via the mobile camera and sends them as a bytestream to requesting device.

Specifications of FNN:

1. Number of input units - 25344 + bias = 25355.
2. Number of hidden layer(s) - 1 having 30 neurons.
3. Number of output classes - 5 (Forward, Backward, Left, Right, Stop).

Codes:

1. Data Acquisition:
	1. ard_training.ino contains the code for Arduino during the training phase
	2. image_and_data_sync.py contains the Python code for acquiring data (Images through WiFi and command through Serial Communication).
2. Training:
	1. main1.py contains the code for training the FNN by importing NN class from nnClass1.py
	2. nnClass1.py contains the NN class, wg\hich contains the functions sigmoid, lossFunc, initWeights, trainNN, forwadPass.
3. Driving:
	1. usingBluetooth contains the code for autonomous driving using Bluetooth. It imports the class NN from nnClass1.py and uses the 				 function forwardPass to get the output class.

Due to the size of the datasets, they could not be uploaded. 3000 images were captured but due to limitaions of RAM (4 GB), only 1200 could be used for training and 200 for cross validation.
