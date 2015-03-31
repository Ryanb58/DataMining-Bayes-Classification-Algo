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
