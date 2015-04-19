"""
Usage:
    regress.py TRAINING_SET TESTING_SET
    regress.py -h | --help
Options:
    -h --help    show this help message
"""
import sys

from docopt import docopt
from numpy import argmax
from numpy import identity
from numpy import matrix
from scale import scale

class DataMismatchError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def parse_matrix(line, min_values, max_values):
    """Returns the two matrices x_i and y_i needed for linear regression parsed
    from a line containing comma separated data with the first number
    representing the category as an integer.
    """
    x_i = [1]
    line = line.strip('\n')
    line_separated = line.split(',')

    for index, value in enumerate(line_separated):
        if index == 0:
            value = int(value)
            y_i = []
            for i in range(0, int(max_values[0])):
                y_i.append(0)
            try:
                y_i[value-1] = 1
            except:
                raise DataMismatchError('Category in testing set not found in\
                                         training set')
        else:
            value = float(value)
            #scales from [0, 1]
            try:
                scaled_value = ( (value - min_values[index]) /
                               (max_values[index] - min_values[index]) )
            except ZeroDivisionError:
                scaled_value = 1
            x_i.append(scaled_value)

    x_i = matrix(x_i).T
    y_i = matrix(y_i).T
    return x_i, y_i

if __name__ == "__main__":
    args = docopt(__doc__)
    min_values, max_values = scale(args['TRAINING_SET'])

    with open(args['TRAINING_SET'], 'r') as training_file:
        for line in training_file:
            x_i, y_i = parse_matrix(line, min_values, max_values)
            try:
                sum_xi += x_i * x_i.T
                sum_yi += x_i * y_i.T
            except NameError:
                sum_xi = x_i * x_i.T
                sum_yi = x_i * y_i.T
    try:
        W = (sum_xi).I * sum_yi # will raise exception if no inverse
    except:
        W = (sum_xi + 0.00001*identity(sum_xi.shape[0])).I * sum_yi

    with open(args['TESTING_SET'], 'r') as testing_file:
        correct = 0
        total = 0
        for line in testing_file:
            x_i, y_i = parse_matrix(line, min_values, max_values)
            prediction = W.T * x_i
            if argmax(prediction) == argmax(y_i):
                correct += 1
            total += 1
    print('Accuracy: {0}%'.format(correct/total * 100))
