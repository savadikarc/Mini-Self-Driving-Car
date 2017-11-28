'''
Code for Autonomous Driving using Bluetooth
'''

import signal
import sys
from time import sleep
from io import BytesIO
from PIL import Image
import urllib.request as url
import numpy as np
import bluetooth
import nnClass1
from scipy.io import loadmat

score1 = np.zeros((1, 30))
score1 = np.concatenate((np.ones((1, 1)), score1), axis = 1)

urlConnect = 'http://192.168.43.149:8080/video?.mjpeg'
stream = url.urlopen(urlConnect)
add = '98:D3:35:00:B6:10'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((add, port))

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    #s.send(b'7')
    s.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

cnt = 0
contents = loadmat('weights2.mat')
w1 = contents['W1']
w2 = contents['W2']
net = nnClass1.NN()
while True:
    cnt += 1
    
    byte = stream.read(76)
    c = byte.decode("UTF-8")
    print(c)
    length = int(c[68:73])
    b = BytesIO(stream.read(length))
    i = Image.open(b)
    ia = i.convert('L')
    i1 = np.array(ia)
    avg_inten = np.sum(i1)/25344
    i1 = i1 > avg_inten
    print(cnt)
    img = np.reshape(i1, (1, 25344))
    img = np.concatenate((np.ones((1, 1)), img), axis = 1)
    a = np.dot(img, w1.T)
    score1[:, 1:] = net.sigmoid(a)
    b = np.dot(score1, w2.T)
    score2 = net.sigmoid(b)
    cmmd = np.argmax(score2)
    command = str(cmmd)
    s.send(command)
    sleep(0.7)
