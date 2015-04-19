"""Usage:
    scale.py DATA_SET
    scale.py -h | --help
Options:
    -h --help    show this help message
"""

from docopt import docopt

def scale(filename):
    """Returns two lists, the first containing the minimum and the second
    containing the maximum values of the attributes.

    The index represents which attribute.
    """
    min_values = []
    max_values = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip('\n')
            line_separated = line.split(',')
            for index, value in enumerate(line_separated):
                if len(min_values) <= index:
                    min_values.append(float('inf'))
                    max_values.append(float('-inf'))
                value = float(value)
                if value < min_values[index]:
                    min_values[index] = value
                if value > max_values[index]:
                    max_values[index] = value
    return min_values, max_values

if __name__ == "__main__":
    args = docopt(__doc__)
    print(scale(args['DATA_SET']))
