import tensorflow as tf
import numpy as np
ttlReward = 0
rewardList = []
circuitData = []
stateList = []
weightedRewardList = []
keys = ['P','L','Z','Q','S','D']
class RNN:
    def __init__(self, inputsNbr, trainingDataWidth):
        N, D, H = trainingDataWidth, inputsNbr, 1000
        self.N, self.D, self.H = N,D,H
        self.x = tf.placeholder(tf.float32, shape = (N,D))
        self.y = tf.placeholder(tf.float32,shape = (N, 1))
        self.w1 = tf.placeholder(tf.float32, shape = (D,H))
        self.w2 = tf.placeholder(tf.float32, shape = (H,H))
        self.w3 = tf.placeholder(tf.float32, shape = (H,1))
        self.h = tf.maximum(tf.matmul(self.x, self.w1),0)
        self.h2 = tf.maximum(tf.matmul(self.h, self.w2),0)
        self.y_pred = tf.matmul(self.h2,self.w3)
        self.diff = self.y_pred - self.y
        self.loss = tf.reduce_mean(tf.reduce_sum(self.diff ** 2, axis = 1))
        self.grad_w1, self.grad_w2, self.grad_w3 = tf.gradients(self.loss, [self.w1, self.w2, self.w3])
    def train(self, x, y):
        with tf.Session() as sess:
            values = {self.x: x,
                      self.w1: np.random.randn(self.D, self.H),
                      self.w2: np.random.randn(self.H, self.H),
                      self.w3: np.random.randn(self.H, 1),
                      self.y: y}
            learning_rate = 10 ** (-11.7875)
            for x in range(2000):
                out = sess.run([self.loss, self.grad_w1, self.grad_w2, self.grad_w3], feed_dict = values)
                loss_val, grad_w1_val, grad_w2_val, grad_w3_val = out
                print(loss_val)
                values[self.w1] -= learning_rate * grad_w1_val
                values[self.w2] -= learning_rate * grad_w2_val
                values[self.w3] -= learning_rate * grad_w3_val

class DataSet:
    def __init__(self):
        self.x = []     
        self.y = []
    def addData(self,inputs, outputs):
        if len(inputs) != len(outputs): raise ValueError('Inputs length != output length')
        self.x += inputs
        self.y += outputs
    def convert(self):
        r = ''
        for x in range(len(self.x)):
            r += str(self.x[x])+':'
            r += str(self.y[x])+"\n"
        return r
dataset = DataSet()         
def computeTtlReward(carPos, stPos, Timer):
    reward = (carPos[0] - stPos[0])**2 + 2*((carPos[1] - stPos[1])**2) - (Timer * 2)
    if carPos[1] > 700: reward += 10000
    return reward

def computeNewReward(carPos, stPos, Timer):
    global ttlReward
    newTtlReward = computeTtlReward(carPos, stPos, Timer)
    newReward = newTtlReward - ttlReward
    if newReward < 0: newReward = 0
    rewardList.append(newReward)
    ttlReward = newTtlReward
    return newReward

def getWeightedFutureReward(t):
    global weightedRewardList
    weightedFutureReward = 0
    weight = 500
    for reward in rewardList[t:t+500]:
        weightedFutureReward += (reward * weight / 500)
        weight -= 1
    weightedRewardList.append([weightedFutureReward])
    return weightedFutureReward

def storeCircuitData(circuit):
    for line in circuit.didgets:
        for didget in line:
            try:
                circuitData.append(int(didget))
            except: pass

def storeState(car, pressedKey, Timer):
    state = [car.lenght,
             car.height,
             car.poid,
             car.vitesseMax,
             car.maniabilite,
             car.freins,
             car.vitesse,
             car.inertie,
             car.pos[0],
             car.pos[1],
             car.orientation,
             ]
    state += circuitData
    state.append(Timer)
    for k in keys:
        if k in pressedKey:
            state.append(1)
        else:
            state.append(0)
    stateList.append(state)

def storeData(car, stPos, pressedKey, Timer):
    reward = computeNewReward(car.pos, stPos, Timer)
    storeState(car, pressedKey, Timer)
    return int(reward)
def genDataset():
    global rewardList, dataset, ttlReward, circuitData, stateList, weightedRewardList
    for x in range(len(rewardList)):
        getWeightedFutureReward(x)
    dataset.addData(stateList, weightedRewardList)
    ttlReward = 0
    rewardList = []
    circuitData = []
    stateList = []
    weightedRewardList = []

def trainModel():
    model = RNN(len(dataset.x[0]), len(dataset.x))
    model.train(dataset.x, dataset.y)
    return model
