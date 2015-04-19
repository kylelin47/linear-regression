"""
Usage:
    regress.py TRAINING_SET TESTING_SET
    regress.py -h | --help
Options:
    -h --help    show this help message
"""
import sys

from docopt import docopt
from numpy import matrix
from numpy import linalg
if __name__ == "__main__":
    args = docopt(__doc__)
    training_file = open(args['TRAINING_SET'], 'r')
    training_file.close()

    testing_file = open(args['TESTING_SET'], 'r')
    testing_file.close()
