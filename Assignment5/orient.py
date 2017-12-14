#!/usr/bin/env python
import sys
from math import exp
import math
from random import seed
from random import random
import json


# Report
# I) Knn algorithm:
#   We are finding the euclidean distance between each and every pixel of the test image and with all the pixels of corresponding train images(10k).
#   Then we sort the all the errors in ascending order and pick the top 11.
#   We got an accuracy about 70%.
#   Findings:
#   1) We initially implemented using lists and the whole algorithm was taking about 26min to complete. Then we switched and used numpy to calculate the eculidiean distance
#   which reduced the time to 7mins.
#   2) We have experimented with values of k. We have tested with the following values of k = 5, 9, 11 and 21.
#   We observed that the accuracy and time where increasing as increase the value of K. We have decided using the k=11 as it is has accuracy about 70% and time is not as bad as k=21.
#
# II) Adaboost algorithm:
#   Training:
#   1) We have taken 191 * 192 decision stumps in our adaboost algorithm and we assigned random pixels (r,g,b) values to these decision stumps.
#   2) We then noticed the pattern of these decsion stumps for 0, 90, 180 and 270 orientation of images. Our pattern was to see if the pixel1 value is greater than pixel2.
#   3) After training we have saved decision stump weights for all the 4 classifiers in our adaboost_model.txt.
#   4) We have tried altering the number of decsion stumps to be taken and noticed if we take fewer stumps then the accuracy of predcition varies a lot with each run and pixels chosen are random.
#   5) We then decided to take almost all the decsion stump values close  to 192 * 192.
#
#   Testing:
#   1) We use the adabosst_model.txt to fetch the edge weights of all the 4 orientations. Check whether their corresponding random pixel (r,g,b) values match the condition.
#   2) If yes we add the decsion stump value and If no we subtract the decsion stump value then we pick the maximium value among the 4 and predcit the output.
#
# III) Neural Net algorithm:
#   Training:
#   1) Our neural network has one layer with 5 nodes and the output layer has 4 nodes as there are four classifiers.
#   2) We have implemented forward propagation algorithnm and adjust the weights using the backward propagation algorithm.
#   3) Each image in our train data uses forward algorithm uses fwd propagation and updates the weight for each neuron by calculating error.
#   4) We had to normalize our pixel data to make our sigmoid function return proper values.
#   5) We have stored all the weights for a neuron as a dictionary in the nnet_model.txt.
#   6) Our training took about 15 hours to generate a file.
#   7) We ran the code by changing the no.of nodes in hidden layer to 16 and reducing the no.of iterations to 100, 500 and 1000 and observed the best results are for no.of iteratoisn as 100.
#   8) We chose a high learning rate alpha as 0.5 and reduced the no.of iterations to 100.
#   9) At the end we chose 5 nodes in hidden layer, alpha = 0.5, iterations = 100.
#   Testing:
#   1) We use the weitghts calculated during training and run our feed forward algorithm. We then use the 4 answers from the output laywr and take the maximum from it.
#   2) We then print it to the output.txt file.
#
# IV) Best Algorithm:
#   Our best algorithm is neural network.
#

# Adaboost Algorithm
def trainAdaboost(model_file):
    print 'Training Data...'
    file = open("train-data.txt", 'r');
    trainList = []
    for line in file:
        l = line.split()
        l = l[1:]
        l = map(int, l)
        trainList.append(l)
    decision_stump = {}
    while (len(decision_stump) < 191 * 192):
        random_pixel1 = random.randint(1, 192)
        random_pixel2 = random.randint(1, 192)
        if random_pixel2 == random_pixel1:
            continue
        else:
            decision_stump['0' + '->' + str(random_pixel1) + '->' + str(random_pixel2)] = 1 / float(len(trainList))
            decision_stump['90' + '->' + str(random_pixel1) + '->' + str(random_pixel2)] = 1 / float(len(trainList))
            decision_stump['180' + '->' + str(random_pixel1) + '->' + str(random_pixel2)] = 1 / float(
                len(trainList))
            decision_stump['270' + '->' + str(random_pixel1) + '->' + str(random_pixel2)] = 1 / float(
                len(trainList))
    correct_zero = 0
    correct_90 = 0
    correct_180 = 0
    correct_270 = 0
    incorrect_zero = 0
    incorrect_90 = 0
    incorrect_180 = 0
    incorrect_270 = 0
    for row in trainList:
        for stump in decision_stump.keys():
            if row[int(stump.split('->')[1])] > row[int(stump.split('->')[2])] and stump.split('->')[0] == row[0]:
                if row[0] == 0:
                    correct_zero = correct_zero + 1
                elif row[0] == 90:
                    correct_90 = correct_90 + 1
                elif row[0] == 180:
                    correct_180 = correct_180 + 1
                else:
                    correct_270 = correct_270 + 1
            else:
                if row[0] == 0:
                    incorrect_zero = incorrect_zero + 1
                elif row[0] == 90:
                    incorrect_90 = incorrect_90 + 1
                elif row[0] == 180:
                    incorrect_180 = incorrect_180 + 1
                else:
                    incorrect_270 = incorrect_270 + 1
            if row[0] == 0:
                error = 0.5 / incorrect_zero
            elif row[0] == 90:
                error = 0.5 / incorrect_90
            elif row[0] == 180:
                error = 0.5 / incorrect_180
            elif row[0] == 270:
                error = 0.5 / incorrect_270
            decision_stump[stump] = 0.5 * math.log((1 - error) / (error))

    file = open(model_file, 'w');
    file.write(json.dumps(decision_stump))
    file.close()
    return decision_stump

def testAdabooost(model_file,output_file):
    print 'Testing Data...'
    file = open("test-data.txt", 'r');
    testList = []
    for line in file:
        l = line.split()
        imageName = l[0]
        l = l[1:]
        l = map(int, l)
        l.insert(0, imageName)
        testList.append(l)
    file = open(model_file, 'r');
    decision_stump = json.load(file)

    file1 = open(output_file,'w');
    noOfCorrect = 0
    for row in testList:
        correct_zero = 0
        correct_90 = 0
        correct_180 = 0
        correct_270 = 0
        for stump in decision_stump.keys():
            if row[int(stump.split('->')[1])] > row[int(stump.split('->')[2])]:
                if int(stump.split('->')[0]) == 0:
                    correct_zero = correct_zero + decision_stump[stump]
                else:
                    correct_zero = correct_zero - decision_stump[stump]
                if int(stump.split('->')[0]) == 90:
                    correct_90 = correct_90 + decision_stump[stump]
                else:
                    correct_90 = correct_90 - decision_stump[stump]
                if int(stump.split('->')[0]) == 180:
                    correct_180 = correct_180 + decision_stump[stump]
                else:
                    correct_180 = correct_180 - decision_stump[stump]
                if int(stump.split('->')[0]) == 270:
                    correct_270 = correct_270 + decision_stump[stump]
                else:
                    correct_270 = correct_270 - decision_stump[stump]
        errorMap = {'0': correct_zero, '90': correct_90, '180': correct_180, '270': correct_270}
        maximum = max(errorMap, key=errorMap.get)
        # print(maximum, errorMap[maximum])
        if int(maximum) == row[1]:
            noOfCorrect = noOfCorrect + 1
        file1.write(row[0] + " " + str(maximum) + '\n')
    file1.close()

    print 'Adaboost Accuracy: ' + str(float(noOfCorrect)/len(testList)*100)

# Neural Net Start
# Calculate neuron activation for an input
def sigmoidFn(weightsOfNeurons, inputs):
    sigmoidValue = weightsOfNeurons[-1]
    for i in range(len(weightsOfNeurons)-1):
        sigmoidValue += weightsOfNeurons[i] * float(inputs[i])
    return sigmoidValue

# Transfer neuron activation
def correctingSigmoidError(currentValue):
    return 1.0 / (1.0 + exp(-currentValue))

# Forward propagate input to a network output
def fwdpropagation(neuralNetwork, imgData):
    imgDataCopy = imgData
    for layer in neuralNetwork:
        new_inputs = []
        for neuron in layer:
            activation = sigmoidFn(neuron['listOfWeights'], imgDataCopy)
            neuron['neuronOutput'] = correctingSigmoidError(activation)
            new_inputs.append(neuron['neuronOutput'])
        imgDataCopy = new_inputs
    return imgDataCopy

# Calculate the derivative of an neuron output
def transfer_derivative(neuronOutput):
    return neuronOutput * (1.0 - neuronOutput)

# Backpropagate error and store in neurons
def backPropagate(neuralNetwork, actualOutput):
    for i in reversed(range(len(neuralNetwork))):
        networkLayer = neuralNetwork[i]
        errorData = list()
        if i != len(neuralNetwork)-1:
            for j in range(len(networkLayer)):
                error = 0.0
                for neuron in neuralNetwork[i + 1]:
                    error += (neuron['listOfWeights'][j] * neuron['deviation'])
                errorData.append(error)
        else:
            for j in range(len(networkLayer)):
                neuron = networkLayer[j]
                errorData.append(actualOutput[j] - neuron['neuronOutput'])
        for j in range(len(networkLayer)):
            neuron = networkLayer[j]
            neuron['deviation'] = errorData[j] * transfer_derivative(neuron['neuronOutput'])

# Update network weights with error
def updateNetworkWeights(neuralNetwork, imgData, alpha):
    for i in range(len(neuralNetwork)):
        inputs = imgData[:-1]
        if i != 0:
            inputs = [neuron['neuronOutput'] for neuron in neuralNetwork[i - 1]]
        for neuron in neuralNetwork[i]:
            for j in range(len(inputs)):
                neuron['listOfWeights'][j] += alpha * neuron['deviation'] * float(inputs[j])
            neuron['listOfWeights'][-1] += alpha * neuron['deviation']


# Make a prediction with a network
def predict(network, row):
    outputs = fwdpropagation(network, row)
    return outputs.index(max(outputs))


def trainingNeuralNet(noOfClassifiers, noOfNeuronsInHidden, noOfPixels, model_file, iterationLength, alpha):

    print 'training data...'
    trainMapNew = []
    # Reading test files
    file = open("train-data.txt", 'r');
    trainMap = []

    for line in file:
        l = line.split()
        trainMap.append(l)

    for row in trainMap:
        tempRow = []
        tempRow = row[2:]
        total = sum(map(int, tempRow))
        newList = [float(x) / float(total) for x in tempRow]
        newList.append(row[1])
        trainMapNew.append(newList)

    neuralNet = []
    hidden_layer = [{'listOfWeights': [random() for i in range(noOfPixels + 1)]} for i in range(noOfNeuronsInHidden)]
    neuralNet.append(hidden_layer)
    output_layer = [{'listOfWeights': [random() for i in range(noOfNeuronsInHidden + 1)]} for i in
                    range(noOfClassifiers)]
    neuralNet.append(output_layer)
    for i in range(0, iterationLength):
        sum_error = 0
        for row in trainMapNew:
            outputs = fwdpropagation(neuralNet, row)
            actualValue = [0 for j in range(noOfClassifiers)]
            actualValue[ansMap[row[-1]]] = 1
            sum_error += sum([(actualValue[j] - outputs[j]) ** 2 for j in range(len(actualValue))])
            backPropagate(neuralNet, actualValue)
            updateNetworkWeights(neuralNet, row, alpha)

    with open(model_file, 'w') as file:
        file.write(json.dumps(neuralNet))

def testingNeuralNet(model_file, outputfile):

    print 'testing data...'
    # Reading train files
    file = open("test-data.txt", 'r');
    testMap = []
    for line in file:
        l = line.split()
        testMap.append(l)

    neuralNet = json.load(open(model_file))
    testMapNew = []
    for row in testMap:
        tempRow = []
        tempRow = row[2:]
        total = sum(map(int, tempRow))
        newList = [float(x) / float(total) for x in tempRow]
        newList.append(row[1])
        newList.append(row[0])
        testMapNew.append(newList)

    matches = 0
    file1 = open(outputfile, 'w');
    for row in testMapNew:
        imgName = row[-1]
        row = row[:-1]
        prediction = predict(neuralNet, row)
        if row[-1] == revAnsMap[prediction]:
            matches = matches + 1
        file1.write(imgName + " " + str(revAnsMap[prediction]) + '\n')

    file1.close()
    print 'Neural network Accuracy: ' + str(float(matches)/len(testMapNew)*100)

# - Program starts here
    # - option stores either "test" or "train"
    # - train_test_file stores "train_file.txt" or "test_file.txt"
    # - model_file stores "model_file.txt"
    # - model_used stores the model we are using
if __name__ == '__main__':
    # Test training backprop algorithm
    seed(1)
    ansMap = {'0': 0, '90': 1, '180': 2, '270': 3}
    revAnsMap = {0: '0', 1: '90', 2: '180', 3: '270'}
    option = sys.argv[1]
    train_test_file = sys.argv[2]
    model_file = sys.argv[3]
    model_used = sys.argv[4]
    allImages = {}
    allImagesList = {}
    trainList = {}
    modelList = {}

    if(option == 'train'):

        if(model_used == 'adaboost'):
            trainAdaboost(model_file)

        elif(model_used == 'nearest'):
            print "undecided"

        elif(model_used == 'nnet'):
            noOfClassifiers = 4
            noOfPixels = 192
            noOfNeuronsInHidden = 5
            iterationLength = 100
            alpha = 0.5
            trainingNeuralNet(noOfClassifiers, noOfNeuronsInHidden, noOfPixels, model_file, iterationLength, alpha)

        elif(model_used == 'best'):
            noOfClassifiers = 4
            noOfPixels = 192
            noOfNeuronsInHidden = 5
            iterationLength = 100
            alpha = 0.5
            trainingNeuralNet(noOfClassifiers, noOfNeuronsInHidden, noOfPixels, model_file, iterationLength, alpha)

    elif(option == 'test'):

        if(model_used == 'adaboost'):
            testAdabooost(model_file,'output.txt')

        elif(model_used == 'nearest'):
            print 'K nearest comes here'

        elif(model_used == 'nnet'):
            testingNeuralNet(model_file, 'output.txt')

        elif(model_used == 'best'):
            model_file = 'nnet_model.txt'
            testingNeuralNet(model_file, 'output.txt')
