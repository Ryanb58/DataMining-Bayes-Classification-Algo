#IMPORTS
import numpy as np
import sys
import random
import timeit
import csv
import copy
import getopt
import math
from scipy.stats import multivariate_normal

data = []

classifiers = []
priorProbabilities = []
means = []
covarianceMatrixes = [[],[],[]]

class Instance:
    'Common base class for all points'

    def __init__(self, points, classifier):
      self.Points = points
      self.Classifier = classifier
      self.PredictedClassifier = None

    def getPoints(self):
        return self.Points

    def getClassifier(self):
        return self.Classifier

    def getPredictedClassifier(self):
        return self.PredictedClassifier

    def setPredictedClassifier(self, classifier):
        self.PredictedClassifier = classifier

    def printPoint(self):
        print "Predicted Classifier: " + self.PredictedClassifier
        print "Classifier: "+ self.Classifier + " - Point : " + " - ".join(self.Points)


def readInModelFile(fn):
    with open(fn, "rb") as f:
        csvFile = csv.reader(f)
        count = 0
        classifierCount = 0
        priorCount = 1
        meanCount = 2
        covarianceCount1 = 3
        covarianceCount2 = 4
        covarianceCount3 = 5
        covarianceCount4 = 6
        covarianceMatrixCount = 0
        for line in csvFile:
            #print line
            #print "---------------------"
            #print count
            #print classifierCount
            #print priorCount
            #print meanCount
            #print covarianceCount1
            #print covarianceCount2
            #print covarianceCount3
            #print covarianceCount4
            #print covarianceMatrixCount
            #print "---------------------"
            if count == classifierCount:
                classifiers.append(line[0])
                classifierCount +=7
            elif count == priorCount:
                priorProbabilities.append(line[0])
                priorCount += 7
            elif count == meanCount:
                means.append(line)
                meanCount += 7
            elif count == covarianceCount1:
                covarianceMatrixes[covarianceMatrixCount].append(line)
                covarianceCount1 += 7
            elif count == covarianceCount2:
                covarianceMatrixes[covarianceMatrixCount].append(line)
                covarianceCount2 += 7
            elif count == covarianceCount3:
                covarianceMatrixes[covarianceMatrixCount].append(line)
                covarianceCount3 += 7
            elif count == covarianceCount4:
                covarianceMatrixes[covarianceMatrixCount].append(line)
                covarianceCount4 += 7
                covarianceMatrixCount += 1

            count += 1

def getInputs():
    optlist, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in optlist:
        if o == "-d":
            loadDataFromFile(a)

def loadDataFromFile(fn):
    with open(fn, "rb") as f:
        csvFile = csv.reader(f)
        for line in csvFile:
            data.append(Instance(line[:(len(line) - 1)], line[-1]))

def getDataInThisClasifier(classifier):
    return [x for x in data if x.getClassifier() == classifier]

def calPredictions():

    #Loop through each
    for index, item in enumerate(data):
        probMultiPrios = []
        for ind, classifier in enumerate(classifiers):

            #print classifier
            #print item.getPoints()
            #print means[ind]
            #print covarianceMatrixes[ind][ind]
            #Calulate Likelyhood

            probability = multivariate_normal.pdf(item.getPoints(), means[ind], covarianceMatrixes[ind][ind], True)
            #Multiply by the priorprobability.
            probMultiPrios.append(priorProbabilities[ind] * probability)
        #Get the max value from the array and set the predicted classifier for the item.
        item.setPredictedClassifier(classifiers[probMultiPrios.index(max(probMultiPrios))])

def confusionMatrix():
    matrix = [[0,0,0],[0,0,0],[0,0,0]]

    for ind, classifier in enumerate(classifiers):
        #print "IN"
        #print classifier
        #print getDataInThisClasifier(classifier)
        for index, item in enumerate(getDataInThisClasifier(classifier)):
            #print "IN"
            #print item.getPredictedClassifier()
            #print item.getClassifier()
            #if item.getPredictedClassifier() == item.getClassifier():
            matrix[ind][classifiers.index(item.getPredictedClassifier())] += 1

    return matrix

if __name__ == "__main__":
    readInModelFile('model.csv')
    getInputs()
    #DEBUG STUFF:
    #print classifiers[0]
    #print priorProbabilities[0]
    #print means[0]
    #print covarianceMatrixes[0]
    print ""
    print ""
    print "---------- Doing calculations! ---------- "
    calPredictions()

    print "Length: " , len(data)
    print ""
    print ""
    print "---------- Predicted Classification: ---------- "
    for index, x in enumerate(data):
        #x.printPoint()
        print index , ") " , x.getPredictedClassifier()
    print ""
    print ""
    print "---------- Confusion Matrix: ---------- "
    confusMatrix = confusionMatrix()
    print confusMatrix

    print ""
    print ""
    print "---------- Precision, Accuracy, and F-Measure: ---------- "
    for index, classifier in enumerate(classifiers):
        print classifier , ":"
        print ""

        #Max of row / total of row
        #print max(confusMatrix[index])
        #print sum(confusMatrix[index])
        recal = round(((max(confusMatrix[index]) + 0.0) / (sum(confusMatrix[index]) + 0.0)), 2)
        print "Recal: " , recal

        #Max of column / total of column
        #print confusMatrix
        #Transpose the confusion matrix
        matrxForPrecision = np.array(confusMatrix).T
        #print matrxForPrecision
        precision = round(((max(matrxForPrecision[index]) + 0.0) / (sum(matrxForPrecision[index]) + 0.0)), 2)
        print "Precision: " , precision


        fmeasure = round(((precision * recal)/(2*(precision+recal))), 2)
        print "F-Measure: " , fmeasure

        print ""
