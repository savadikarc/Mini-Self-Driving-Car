'''
This class is used to train the Neural Network
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat, savemat

class NN(object):
    'Main class for NN'
    def __init__(self, X = 0, y = 0, XCross = 0, yCross = 0, y1 = 0, y1Cross = 0):
        self.X = X
        self.y = y
        self.XCross = XCross
        self.yCross = yCross
        self.y1Cross = y1Cross
        self.y1 = y1

    def sigmoid(self, z):
        return(1 / (1 + np.exp(-1*z)))

    def lossFunc(self, score2, m, y):
        score2 = score2.clip(min=0.0001)
        score2 = score2.clip(max=0.9999)
        return((-1*(np.sum(y * np.log(score2) + (1 - y)*np.log(1 - score2))))/m)

    def initWeights(self):
        w1 = np.sqrt(2.0/25344)*np.random.normal(loc = 0.0, scale = 1.0, size = (30, 25344))
        w1 = np.concatenate((0.01*np.ones((30, 1)), w1), axis = 1)#50x785
        w2 = np.sqrt(2.0/30)*np.random.normal(loc = 0.0, scale = 1.0, size = (5, 30))
        w2 = np.concatenate((0.01*np.ones((5, 1)), w2), axis = 1)#10x26
        return (w1, w2)

    def trainNN(self, w1, w2):
        '''
        plt.ion()
        plt.hold(True)
        plt.xlabel('Iteration')
        plt.ylabel('Accuracy')
        '''
        m = self.X.shape[0]
        mCross = self.XCross.shape[0]
        lam = 2.5
        alpha = 0.001
        i = 1
        score1 = np.zeros((m, 30))
        score1 = np.concatenate((np.ones((m, 1)), score1), axis = 1)
        score1Cross = np.zeros((mCross, 30))
        score1Cross = np.concatenate((np.ones((mCross, 1)), score1Cross), axis = 1)
        cache1 = np.zeros(w1.shape)
        cache2 = np.zeros(w2.shape)
        decay_rate = 0.9
        eps = 10**(-8)
        loss = 100
        maxiter = 1000
        decay_alpha = np.array([[77, 2.5], [81, 2], [83, 2], [90, 2], [95, 2]])
        last_index_alpha_decay = decay_alpha.shape[0] - 1
        ind = 0
        flag = 1
        lossCross = 100
        accCp = 0
        while loss > 0.01:

            #Regularization Terms
            reg1 = np.copy(w1)#30x25344
            reg1[:, 0] = 0#30x25344
            reg1s = np.sum(np.square(reg1))
            reg2 = np.copy(w2)#5x31
            reg2[:, 0] = 0#5x31
            reg2s = np.sum(np.square(reg2))

            #Forward Pass on Training Set
            a = np.dot(self.X, w1.T)#mx25344, 25344x30 = mx30
            score1[:, 1:] = self.sigmoid(a)#mx30
            b = np.dot(score1, w2.T)#mx31, 31x5 = mx5
            score2 = self.sigmoid(b)

            #Forward Pass on CV Set
            (score2Cross, accC) = self.forwardPass(w1, w2)

            #Store best value for CV set
            if accCp < accC:
                w1best = np.copy(w1)
                w2best = np.copy(w2)

            #Loss Function for Training Set
            loss = self.lossFunc(score2, m, self.y) + (lam*(reg1s + reg2s))/(2*m)
            #Loss Function for CV Set
            lossCross = self.lossFunc(score2Cross, mCross, self.yCross)

            #RMSProp
            grad2 = (-1*(self.y - score2))#mx10
            dw2 = np.dot(grad2.T, score1) + ((lam/(m))*reg2)#5xm, mx31 = 5x31
            grad1 = np.dot(grad2, w2[:, 1:])#mx5, 5x30 = mx30
            grad0 = grad1 * score1[:, 1:] *(1 - score1[:, 1:])#mx30, mx30
            dw1 = np.dot(grad0.T, self.X) + ((lam/(m))*reg1)#30xm, mx25344 = 30x25344

            #Weight Update
            cache1 = decay_rate*cache1 + (1 - decay_rate) * dw1**2
            cache2 = decay_rate*cache2 + (1 - decay_rate) * dw2**2
            w1 -= alpha*dw1 / (np.sqrt(cache1) + eps)
            w2 -= alpha*dw2 / (np.sqrt(cache2) + eps)

            #Print Everything
            print("Epoch:" ,i, "|Loss(Training):", loss, "|Acc(C):", accC, "|Loss(CV):", lossCross, "|alpha:", alpha)
            '''
            plt.subplot(2, 1, 1)
            plt.scatter(i, loss)
            plt.subplot(2, 1, 2)
            plt.scatter(i, accC)
            plt.pause(0.0001)
            '''
            
            if accCp < accC:
                accCp = accC
                epoch = i

            if (accC >= decay_alpha[(ind, 0)]) and flag == 1:
                if ind == last_index_alpha_decay:
                    alpha = alpha/decay_alpha[(ind, 1)]
                    flag = 0
                else:
                    alpha = alpha/decay_alpha[(ind, 1)]
                    ind += 1

            if i%100 == 0:
                print('Max accuracy achieved ', accCp, 'at epoch ', epoch)
                savemat('weights3.mat', {'W1':w1best, 'W2':w2best})
                savemat('parameters3.mat', {'lambda':lam, 'alpha':alpha, 'maxAcc':accCp})

            if i%maxiter == 0:
                print('Max accuracy achieved ', accCp, 'at epoch ', epoch)
                ch = input('Continue?')
                if ch != 'n':
                    maxiter = int(input('What number of iterations should be run?'))
                elif ch == 'n':
                    break
            i += 1

        return(w1best, w2best, lam, alpha)

    def forwardPass(self, w1, w2):
        m = self.XCross.shape[0]
        score1 = np.zeros((m, 30))
        score1 = np.concatenate((np.ones((m, 1)), score1), axis = 1)
        a = np.dot(self.XCross, w1.T)#mx25344, 25344x30 = mx30
        score1[:, 1:] = self.sigmoid(a)#mx30
        b = np.dot(score1, w2.T)#mx31, 31x5 = mx5
        score2 = self.sigmoid(b)
        pred = np.argmax(score2, axis = 1)
        val = np.zeros((m, 1))
        for i in range(m):
            val[i] = pred[i] == self.y1Cross[i]
        (row, col) = np.nonzero(val)
        acc = (len(row)/m)*100
        return(score2, acc)
