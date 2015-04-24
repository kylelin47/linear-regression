"""Usage:
    scale.py DATA_SET
    scale.py -h | --help
Options:
    -h --help    show this help message
"""
from docopt import docopt

def scale(filename, delim=','):
    """Returns a list, the first element being the list of minimum
    and the second being the list of maximum values of the attributes.

    The index of a nested list represents which attribute.
    """
    min_values = []
    max_values = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip('\n')
            line_separated = line.split(delim)
            for index, value in enumerate(line_separated):
                if len(min_values) <= index:
                    min_values.append(float('inf'))
                    max_values.append(float('-inf'))
                value = float(value)
                if value < min_values[index]:
                    min_values[index] = value
                if value > max_values[index]:
                    max_values[index] = value
    return [min_values, max_values]

if __name__ == "__main__":
    args = docopt(__doc__)
    print(scale(args['DATA_SET']))
