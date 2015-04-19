# linear-regression
A simple linear regression machine learning program, written in Python 3.4.1

## Dependencies
* Python: https://www.python.org/
* Numpy: http://www.numpy.org/
* Docopt: http://www.docopt.org/

## Data Formatting
Comma separated numbers, with category being the first number. For example, with 3 categories, represent each category as 1, 2, or 3.

Category must be an integer.

```
1,5.1,3.5,1.4,0.2
```

Example data are in iris and wine folders.

## Testing sets and training sets
The training set must contain at least one example of each category present in the testing set.

## Usage
```
> regress.py TRAINING_SET TESTING_SET

Accuracy: n%
```
