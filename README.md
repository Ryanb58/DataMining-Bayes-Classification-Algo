# Normal and Naive Bayes Algorithms
By: Taylor Brazelton

## Generating Model Files:
    python Naive1.py -d First50.csv
or

    python Normal1.py -d First50.csv

These commands generate the model files for each algorithm. You must do one of these first before trying classification.
First50.csv must be formatted like so:

    7.2,3.2,6,1.8,Iris-virginica
    5.4,3,4.5,1.5,Iris-versicolor
    5.7,2.9,4.2,1.3,Iris-versicolor
    etc...

The Naive will output to 'naive_model.csv'. Whereas the Normal Bayes will output to just 'model.csv'.

**Make sure you delete model.csv and/or naive_model.csv before re-running.

## Classification:

    python Naive2.py -d Second50.csv

or

    python Normal2.py -d Second50.csv

  These commands output the predicted values along with the recal, precision, and fmeasure.

  'Naive2.py' will read from a file called 'naive_model.csv' that should be located in the same directory as the program.

  'Normal2.py' will read from a file called 'model.csv' that should be located in the same directory as the program.

  Second50.csv in this situation is formatted exactly like the training data we used to generate the model files. However this time it will be used for predictions.
