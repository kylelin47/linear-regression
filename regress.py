"""Usage:
    regress.py TRAINING_SET TESTING_SET [--verbose]
    regress.py -h | --help
Options:
    -h --help    show this help message
    --verbose    print the weight matrix
"""
from docopt import docopt
from numpy import argmax
from numpy import identity
from numpy import linalg
from numpy import matrix
from scale import scale

class DataMismatchError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def parse_matrix(line, min_values, max_values):
    """Returns the two vectors x_i and y_i needed for linear regression parsed
    from a line containing comma separated data with the first number
    representing the category as an integer.

    min_values should list in order the minimum value for each attribute.
    max_values should list in order the maximum value for each attribute.
    If your training data looks like:
        1,2,3,4
        0,4,1,5
    min_values should be [0, 2, 1, 4]
    max_values should be [1, 4, 3, 5]

    For x_i, each attribute 'a' is scaled according to the passed in lists.
    [min[a], max[a]] is scaled to [0, 1] and any particular 'a' is set to the
    representative value on that number line.
    x_i then becomes a vector of scaled attributes, with a 1 at the top
    for offset purposes.
    x_i = [1
           scaled_a1
           scaled_a2
           scaled_a3
           ...
           scaled_an]

    y_i is a vector of (max_values[0] - min_values[0] + 1) entries where
    every entry except line[0] equals 0, and the line[0] entry equals 1.
    For example, if min_values[0] == 1 and max_values[0] == 3 and line[0] == 2
    y_i = [0
           1
           0]
    """
    x_i = [1]
    line = line.rstrip('\n')
    line_separated = line.split(',')
    for index, value in enumerate(line_separated):
        if index == 0:
            try:
                value = int(value)
            except ValueError:
                raise DataMismatchError('Category must be an integer')
            y_i = []
            for i in range( int(min_values[0]), int(max_values[0]) + 1 ):
                y_i.append(0)
            try:
                y_i[value-1] = 1
            except:
                raise DataMismatchError('More testing set categories than ' +
                                        'training set categories')
        else:
            value = float(value)
            try:
                scaled_value = ( (value - min_values[index]) /
                                 (max_values[index] - min_values[index]) )
            except ZeroDivisionError:
                scaled_value = 1
            x_i.append(scaled_value)

    return matrix(x_i).T, matrix(y_i).T

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
    except linalg.LinAlgError:
        W = (sum_xi + 0.00001*identity(sum_xi.shape[0])).I * sum_yi
    if (args['--verbose']):
        print('W =\n{0}'.format(W))

    with open(args['TESTING_SET'], 'r') as testing_file:
        correct = 0
        total = 0
        for line in testing_file:
            x_i, y_i = parse_matrix(line, min_values, max_values)
            prediction = W.T * x_i
            if argmax(prediction) == argmax(y_i):
                correct += 1
            total += 1

    print('Results:  {0}/{1}'.format(correct, total))
    print('Accuracy: {0:.2f}%'.format(correct/total * 100))
