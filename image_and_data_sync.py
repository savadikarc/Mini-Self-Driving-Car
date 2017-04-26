'''
Code for Data Acquisition
'''
import serial
import signal
import sys
from time import sleep
from io import BytesIO
from PIL import Image
import urllib.request as url
import numpy as np
from scipy.io import savemat


ser = serial.Serial('COM4', 9600 )
urlConnect = 'http://192.168.43.149:8080/video?.mjpeg'
stream = url.urlopen(urlConnect)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    savemat('training25.mat', {'X':X, 'ymat':ymat})
    print('Done.')
    ser.write(b'3')
    sys.exit(0)
    #ser.close()

signal.signal(signal.SIGINT, signal_handler)

X = np.zeros((1, 25344))
ymat = np.zeros((1, 5))
ycomp = np.array([102, 100, 108, 114, 115])#f b l r s
ycomp = np.reshape(ycomp, (1, 5))
cnt = 0
fromBoard = 1


while True:
    ser.write(b'1')
    if ser.inWaiting()>0 and fromBoard == 1:
        c = ser.readline()
        if c == b'Start\r\n':
            byte = stream.read(76)
            c = byte.decode("UTF-8")
            length = int(c[68:73])
            b = BytesIO(stream.read(length))
            i = Image.open(b)
            ia = i.convert('L')
            i1 = np.array(ia)
            avg_inten = np.sum(i1)/25344
            i1 = i1 > avg_inten
            x = np.reshape(i1, (1, 25344))
            X = np.concatenate((X, x), axis = 0)
            fromBoard = 0
            ser.write(b'2')
        while fromBoard == 0:
            if ser.inWaiting()>0:
                d = ser.readline()

                if d == b'Sending\r\n':
                    fromBoard = 2
                    while fromBoard == 2:
                        if ser.inWaiting()>0:
                            e = ser.readline()
                            g = e.decode("UTF-8")

                            g = int(g[0:3])
                            y = ycomp == g
                            print(cnt, g, sep = ' ')
                            ymat = np.concatenate((ymat, y), axis = 0)
                            fromBoard = 1
            else:
                fromBoard = 0
    m = X.shape
    if m[0]%100 == 0:
        savemat('training25.mat', {'X':X, 'ymat':ymat})
    sleep(0.01)
    cnt+=1