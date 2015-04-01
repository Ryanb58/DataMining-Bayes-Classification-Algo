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
covarianceMatrixes = []

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


def readInModelFile(fn):
    with open(fn, "rb") as f:
        csvFile = csv.reader(f)
        count = 0
        classifierCount = 0
        priorCount = 1
        meanCount = 2
        covarianceCount =3
        for line in csvFile:
            #print line
            if count == classifierCount:
                classifiers.append(line[0])
                classifierCount +=4
            elif count == priorCount:
                priorProbabilities.append(line[0])
                priorCount += 4
            elif count == meanCount:
                means.append(line[0])
                meanCount += 4
            elif count == covarianceCount:
                covarianceMatrixes.append(line)
                covarianceCount += 4
            count += 1

    #Now convert to the correct formats.

def loadDataFromFile(fn):
    with open(fn, "rb") as f:
        csvFile = csv.reader(f)
        for line in csvFile:
            data.append(Instance(line[:(len(line) - 1)], line[-1]))

def calPredictions():
    #Loop through each
    for index, item in enumerate(data):
        probMultiPrios = []
        for classifier in classifiers:
            probability = multivariate_normal.pdf(point, mean[index], covarianceMatrix[index])
            probMultiPrios.append(priorProbabilities[index] * probability)
        item.setPredictedClassifier(classifiers[probMultiPrios.index(max(probMultiPrios))])

if __name__ == "__main__":
    readInModelFile('model.csv')
    print classifiers
    print priorProbabilities
    print means
    print covarianceMatrixes
