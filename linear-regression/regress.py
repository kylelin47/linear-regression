"""Usage:
    regress.py TRAINING_SET TESTING_SET [-w | --weight] [-v | --verbose]
    regress.py -h | --help
Options:
    -h --help     show this help message
    -w --weight   print the weight matrix
    -v --verbose  print per-class accuracy
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

def parse_vectors(line, data_scale):
    """Returns the two vectors x_i and y_i needed for linear regression parsed
    from a line containing comma separated data with the first number
    representing the category as an integer.

    data_scale should be a list [min_values, max_values]
    min_values should be a list of the minimum values for each attribute.
    max_values should be a list of the maximum values for each attribute.
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
    min_values, max_values = data_scale
    x_i = [1]
    line = line.rstrip('\n')
    line_separated = line.split(',')
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
                raise DataMismatchError('More testing set categories than ' +
                                        'training set categories')
            y_i[offset] = 1                
        else:
            value = float(value)
            try:
                scaled_value = ( (value - min_values[index]) /
                                 (max_values[index] - min_values[index]) )
            except ZeroDivisionError:
                scaled_value = 1
            x_i.append(scaled_value)

    return matrix(x_i).T, matrix(y_i).T

def test_model(testing_filename, weight_matrix, data_scale):
    """Returns the amount of correct predictions and the total number of
    data entries along with a dictionary containing as keys the categories
    and as values a list containing [correct_per_class, total_per_class]

    First argument should be a matrix representing the result of minimizing
    the least squares function over some data.

    The second argument should be the name of the data file to test.

    The third argument should be a list [min_values, max_values] to scale to.
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
            x_i, y_i = parse_vectors(line, data_scale)
            prediction = argmax(W.T * x_i)
            actual = argmax(y_i)
            if prediction == actual:
                correct += 1
                per_class[actual + min_category][0] += 1
            per_class[actual + min_category][1] += 1
            total += 1

    return correct, total, per_class

def weight_matrix(training_filename, get_scale=False):
    """Returns the weight matrix built from the data in the file
    at the filename given as the first argument, scaled according to
    the values in the file.

    Optionally, you can set get_scale=True to also have the scale returned.
    """
    training_scale = scale(training_filename)
    with open(training_filename, 'r') as training_file:
        for line in training_file:
            x_i, y_i = parse_vectors(line, training_scale)
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
    if get_scale:
        return W, training_scale
    return W

if __name__ == '__main__':
    args = docopt(__doc__)

    W, training_scale = weight_matrix(args['TRAINING_SET'], get_scale=True)
    if args['--weight']:
        print('W =\n{0}'.format(W))

    correct, total, d = test_model(args['TESTING_SET'], W, training_scale)
    if args['--verbose']:
        for key in sorted(d):
            print('Category {0}: {1}/{2}, {3:.2f}%'
                  .format(key, d[key][0], d[key][1], d[key][0]/d[key][1]*100))
    print('Results:  {0}/{1}'.format(correct, total))
    print('Accuracy: {0:.2f}%'.format(correct/total * 100))
