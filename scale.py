"""
Usage:
    scale.py DATA_SET
    scale.py -h | --help
Options:
    -h --help    show this help message
"""

from docopt import docopt

def scale(filename):
    min_values = []
    max_values = []
    f = open(filename, 'r')
    for line in f:
        line = line.strip('\n')
        line_separated = line.split(',')
        for index, value in enumerate(line_separated[1:]):
            if len(min_values) <= index:
                min_values.append(float('inf'))
                max_values.append(float('-inf'))
            value = float(value)
            if value < min_values[index]:
                min_values[index] = value
            if value > max_values[index]:
                max_values[index] = value
    f.close()
    return min_values, max_values

if __name__ == "__main__":
    args = docopt(__doc__)
    print(scale(args['DATA_SET']))
