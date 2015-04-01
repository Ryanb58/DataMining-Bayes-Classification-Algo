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
    #Loop through each new data
    for index, item in enumerate(data):
        probMultiPrios = []
        #Loop through each classifier
        for ind, classifier in enumerate(classifiers):
            probs = 1
            #Loop through each dim in the 4dim point.
            for id, point in enumerate(item.getPoints()):
                pt = eval(point) + 0.0
                cvm = eval(covarianceMatrixes[ind][id][id]) + 0.0
                #print means[ind][id]
                mn = eval(means[ind][id]) + 0.0
                #Do math stuff here.
                #print "point value:" , point
                #print type(point)
                #print type(pt)
                #print " Standard Dev: " , covarianceMatrixes[ind][id][id]
                #print type(covarianceMatrixes[ind][id][id])
                #print type(cvm)
                probs = probs * ( (1/(math.sqrt(2*math.pi)*math.sqrt(cvm))) * math.exp(-((pt - mn)**2 / (2 * cvm)**2)))
                #print probs
            probMultiPrios.append(probs)

        #Set the predicted classifier variable.
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
            if item.getPredictedClassifier() == item.getClassifier():
                matrix[ind][classifiers.index(item.getPredictedClassifier())] += 1

    return matrix

if __name__ == "__main__":
    readInModelFile('naive_model.csv')
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
    print confusionMatrix()

    print ""
    print ""
    print "---------- Percision, Accuracy, and F-Measure: ---------- "
    for index, item in enumerate(classifiers):
        pass
