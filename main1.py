import numpy as np
from scipy.io import loadmat, savemat
import nnClass1

#Import and preprocess Training Data
contents = loadmat('trainingFinalTrain.mat')
X = contents['X']
X -= 0.5
m = X.shape[0]
print(m)
X = np.concatenate((np.ones((m, 1)), X), axis = 1)
ymat = contents['ymat']
y1 = np.argmax(ymat, axis = 1)
y = np.reshape(y1, (m, 1))
print(y.shape)
(row, col) = np.nonzero(y == 0*np.ones((m, 1)))

#Import and preprocess Cross Validation Data
contents = loadmat('trainingFinalCross.mat')
XCross = contents['X']
XCross -= 0.5
m = XCross.shape[0]
print(m)
XCross = np.concatenate((np.ones((m, 1)), XCross), axis = 1)
ymatCross = contents['ymat']
y1Cross = np.argmax(ymatCross, axis = 1)
yCross = np.reshape(y1Cross, (m, 1))
print(yCross.shape)

net = nnClass1.NN(X, ymat, XCross, ymatCross, y, yCross)
(w1, w2) = net.initWeights()
(W1, W2, lam, alpha) = net.trainNN(w1, w2)

savemat('weights3.mat', {'W1':W1, 'W2':W2})
savemat('parameters3.mat', {'lambda':lam, 'alpha':alpha})
