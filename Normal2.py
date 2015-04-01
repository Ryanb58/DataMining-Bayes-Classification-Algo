#IMPORTS
import numpy as np
import sys
import random
import timeit
import csv
import copy
import getopt
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
        print "Classifier: "+ self.Classifier + " - Point : " + " - ".join(self.Points)

def getInputs():
    optlist, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in optlist:
        if o == "-d":
            fileName = a
            loadDataFromFile(fileName)


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


def loadDataFromFile(fn):
    with open(fn, "rb") as f:
        csvFile = csv.reader(f)
        for line in csvFile:
            data.append(Instance(line[:(len(line) - 1)], line[-1]))

def calPredictions():
    #Loop through each
    for index, item in enumerate(data):
        probMultiPrios = []
        for ind, classifier in enumerate(classifiers):

            print classifier
            print item.getPoints()
            print means[ind]
            print covarianceMatrixes[ind][ind]
            probability = multivariate_normal.pdf(item.getPoints(), means[ind], covarianceMatrixes[ind][ind])
            probMultiPrios.append(priorProbabilities[ind] * probability)
        item.setPredictedClassifier(classifiers[probMultiPrios.index(max(probMultiPrios))])

if __name__ == "__main__":
    readInModelFile('model.csv')
    getInputs()
    #DEBUG Stuff:
    print classifiers
    print priorProbabilities
    print means
    print covarianceMatrixes

    calPredictions()
    for item in data:
        print "--"
        print item.getPredictedClassifier()
