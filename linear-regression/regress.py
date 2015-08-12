"""Usage:
    regress.py TRAINING_SET TESTING_SET [-w | --weight] [-v | --verbose]
                                        [--delimiter=<str>]
    regress.py -h | --help
Options:
    -h --help          show this help message
    -w --weight        print the weight matrix
    -v --verbose       print per-class accuracy
    --delimiter=<str>  delimiter to split at [default: ,]
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

def parse_vectors(line, data_scale, delim=','):
    """
    Returns the two vectors x_i and y_i needed for linear regression from
    a data line

    data_scale should be a scale. See scale.py
    """
    min_values, max_values = data_scale
    x_i = [1]
    line = line.rstrip('\n')
    line_separated = line.split(delim)
    for index, value in enumerate(line_separated):
        if index == 0:
            try:
                offset = int(value) - int(min_values[0])
            except ValueError:
                raise DataMismatchError('Category must be an integer')
            y_i = []
            for i in range( int(min_values[0]), int(max_values[0]) + 1 ):
                y_i.append(0)
            if offset < 0 or offset >= len(y_i):
                raise DataMismatchError('More testing set categories than '
                                        'training set categories')
            y_i[offset] = 1                
        else:
            value = float(value)
            try:
                scaled_value = ( (value - min_values[index]) /
                                 (max_values[index] - min_values[index]) )
            except ZeroDivisionError:
                scaled_value = 1
            except IndexError:
                scaled_value = value # too many attributes to scale.
            except TypeError:
                scaled_value = value # None/other invalid given as scale
            x_i.append(scaled_value)

    return matrix(x_i).T, matrix(y_i).T

def test_model(testing_filename, weight_matrix, data_scale, delim=','):
    """
    Returns the amount of correct predictions and the total number of
    data entries along with a dictionary containing as keys the categories
    and as values a list containing [correct_per_class, total_per_class]
    """
    with open(testing_filename, 'r') as testing_file:
        per_class = {}
        min_category = int(data_scale[0][0])
        max_category = int(data_scale[1][0])
        for i in range( min_category, max_category + 1 ):
            per_class[i] = [0, 0]
        correct = 0
        total = 0
        for line in testing_file:
            x_i, y_i = parse_vectors(line, data_scale, delim)
            try:
                prediction = argmax(W.T * x_i)
                actual = argmax(y_i)
                if prediction == actual:
                    correct += 1
                    per_class[actual + min_category][0] += 1
                per_class[actual + min_category][1] += 1
                total += 1
            except ValueError:
                pass

    return correct, total, per_class

def weight_matrix(training_filename, get_scale=False, delim=','):
    """
    Returns the weight matrix built from the data in the file
    at the filename given as the first argument, scaled according to
    the values in the file.
    """
    training_scale = scale(training_filename, delim)
    with open(training_filename, 'r') as training_file:
        for line in training_file:
            x_i, y_i = parse_vectors(line, training_scale, delim)
            try:
                sum_xi += x_i * x_i.T
                sum_yi += x_i * y_i.T
            except NameError:
                sum_xi = x_i * x_i.T
                sum_yi = x_i * y_i.T
            except ValueError: # row has differing number of attributes
                if sum_xi.shape[0] < x_i.shape[0]:
                    # more attributes, use this as the standard
                    sum_xi = x_i * x_i.T
                    sum_yi = x_i * y_i.T
                else:
                    # less attributes, ignore it
                    pass
    try:
        W = sum_xi.I * sum_yi # will raise exception if no inverse
    except linalg.LinAlgError:
        W = (sum_xi + 0.00001*identity(sum_xi.shape[0])).I * sum_yi
    if get_scale:
        return W, training_scale
    return W

if __name__ == '__main__':
    args = docopt(__doc__)
    delimiter = args['--delimiter']

    W, training_scale = weight_matrix(args['TRAINING_SET'], get_scale=True,
                                      delim=delimiter)
    if args['--weight']:
        print('W =\n{0}'.format(W))

    correct, total, d = test_model(args['TESTING_SET'], W, training_scale,
                                   delim=delimiter)
    if args['--verbose']:
        for key in sorted(d):
            print('Category {0}: {1}/{2}, {3:.2%}'.format(
                key, d[key][0], d[key][1], d[key][0]/d[key][1]))
    print('Results:  {0}/{1}'.format(correct, total))
    print('Accuracy: {0:.2%}'.format(correct/total))
