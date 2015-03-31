#IMPORTS
import numpy as np
import sys
import random
import timeit
import csv
import copy
import getopt

data = []
classifiers = []

class Instance:
    'Common base class for all points'

    def __init__(self, points, classifier):
      self.Points = points
      self.Classifier = classifier

    def getPoints(self):
        return self.Points

    def getClassifier(self):
        return self.Classifier

    def printPoint(self):
        print "Classifier: "+ self.Classifier + " - Point : " + " - ".join(self.Points)

def getInputs():
    optlist, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in optlist:
        if o == "-d":
            fileName = a
            loadDataFromFile(fileName)

def loadDataFromFile(fn):
    with open(fn, "rb") as f:
        csvFile = csv.reader(f)
        for line in csvFile:
            data.append(Instance(line[:(len(line) - 1)], line[-1]))

    #Go ahead and gen the list of unique classifiers
    genListOfClassifiers()

#extra functions based upon the data array of objects.

def genListOfClassifiers():
    global classifiers
    lst = []
    for item in data:
        lst.append(item.getClassifier())
    classifiers = set(lst)

def getDataInThisClasifier(classifier):
    return [x for x in data if x.getClassifier() == classifier]

#Generate Model File from Data:

def saveModelFile():
    pass

def priorProbabilities():
    #loop through each classifier and gen prior probability.

    prior = []

    for index, classifier in enumerate(classifiers):

        #Hack to force values as floats: + 0.0 on the end.
        dataInClassifierLength = len(getDataInThisClasifier(classifier)) + 0.0
        dataLength = len(data) + 0.0

        #Calculation
        prior.append(dataInClassifierLength / dataLength)

    #Pass back the three prior probabilties.
    return prior

def mean():
    means = []
    for index, classifier in enumerate(classifiers):
        #print len(data[0].getPoints())
        amount = [0.0]*(len(data[0].getPoints()))
        #print amount
        for point in getDataInThisClasifier(classifier):
            amount = np.array(amount, float) + np.array(point.getPoints(), float)
        means.append(amount / len(getDataInThisClasifier(classifier)))
    return means

def covarianceMatrix():
    pass


if __name__ == "__main__":
    getInputs();

    #Have each instance print itself to the console.
    #for point in data:
    #    point.printPoint()

    #print classifiers

    #for classifier in classifiers:
    #    for point in getDataInThisClasifier(classifier):
    #        point.printPoint()

    print priorProbabilities()
    print mean()
    print covarianceMatrix()
