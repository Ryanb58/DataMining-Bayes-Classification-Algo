#IMPORTS
import numpy as np
import sys
import random
import timeit
import csv
import copy
import getopt

data = []

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


if __name__ == "__main__":
    getInputs();

    #Have each instance print itself to the console.
    for point in data:
        point.printPoint()
