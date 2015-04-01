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

def priorProbabilities(classifier):
    #loop through each classifier and gen prior probability.

    #prior = []

    #for index, classifier in enumerate(classifiers):

    #Hack to force values as floats: + 0.0 on the end.
    dataInClassifierLength = len(getDataInThisClasifier(classifier)) + 0.0
    dataLength = len(data) + 0.0

    #Calculation
    return dataInClassifierLength / dataLength

    #Pass back the three prior probabilties.
    #for x in prior:
    #    prior[x] = round(prior[x], 2)

    #return np.array(prior, float)

def mean(classifier):
    means = []
    #for index, classifier in enumerate(classifiers):
    #print len(data[0].getPoints())
    amount = [0.0]*(len(data[0].getPoints()))
    #print amount
    for point in getDataInThisClasifier(classifier):
        amount = np.array(amount, float) + np.array(point.getPoints(), float)
    means.append(amount / len(getDataInThisClasifier(classifier)))
    #return amount / len(getDataInThisClasifier(classifier))

    #round to 2 past the decimal.
    #for x in range(len(means)):
    #    for y in range(len(means[x])):
    #        means[x][y] = round(means[x][y], 2)
    #return means
    #print means[0]
    for x in range(len(means[0])):
        means[0][x] = round(means[0][x], 2)
    return means

def covarianceMatrix(classifier):

    #Store the current matrix of points here.
    matrix = []
    #matrix = np.array(getDataInThisClasifier(classifier)).T
    #loop through each point in the classifier
    #print getDataInThisClasifier(classifier)
    for point in getDataInThisClasifier(classifier):
        #Append each points to the matrix.
        matrix.append(point.getPoints())
    #Print this classifiers covariance matrix
    #print np.array(matrix).T
    covarianceMatrix = np.cov(np.array(matrix, float).T)

    #Round to hundreths place
    for x in range(len(covarianceMatrix)):
        for y in range(len(covarianceMatrix[x])):
            if x == y:
                covarianceMatrix[x][y] = round(covarianceMatrix[x][y], 2)
            else:
                covarianceMatrix[x][y] = 0.0
    return covarianceMatrix

def saveModelFile():
    with open('naive_model.csv', 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        for classifier in classifiers:
            a.writerow([classifier])
            a.writerow([priorProbabilities(classifier)])
            a.writerow(mean(classifier)[0])
            for row in covarianceMatrix(classifier):
                a.writerow(row)


if __name__ == "__main__":
    getInputs();

    #Have each instance print itself to the console.
    #for point in data:
    #    point.printPoint()

    #print classifiers

    #for classifier in classifiers:
    #    for point in getDataInThisClasifier(classifier):
    #        point.printPoint()


    for classifier in classifiers:
        print priorProbabilities(classifier)
        print mean(classifier)
        print covarianceMatrix(classifier)

    saveModelFile()
    print "Model file save successful!"
