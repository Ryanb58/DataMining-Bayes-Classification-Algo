#IMPORTS
import numpy as np
import sys
import random
import timeit
import csv
import copy
import getopt
import math

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

        #Convert from string to int
        #for index, x in enumerate(priorProbabilities):
        #    priorProbabilities[index] = priorProbabilities[index])


def loadDataFromFile(fn):
    with open(fn, "rb") as f:
        csvFile = csv.reader(f)
        for line in csvFile:
            data.append(Instance(line[:(len(line) - 1)], line[-1]))

def calPredictions():
    #Loop through each new data
    for index, item in enumerate(data):
        probMultiPrios = []
        #Loop through each classifier
        for ind, classifier in enumerate(classifiers):
            probs = []
            #Loop through each dim in the 4dim point.
            for id, point in enumerate(item.getPoints()):
                #Do math stuff here.
                print "point value:" + item.getPoints()
                print " Standard Dev: " + covarianceMatrixes[ind][id][id]
                probs.append( 1/(math.sqrt((2*math.pi))* math.sqrt(covarianceMatrixes[ind][id][id])) * math.exp(-((item.getPoints()[id] - means[ind])**2 / (2 * covarianceMatrixes[ind][id][id])**2)))
                print probs

        #item.setPredictedClassifier()

if __name__ == "__main__":
    readInModelFile('naive_model.csv')
    readInModelFile('Last50.iris.csv')
    print classifiers[0]
    print priorProbabilities[0]
    print means[0]
    print covarianceMatrixes[0]

    print "Doing calculations!"
    calPredictions()
