# linear-regression
A simple linear regression machine learning program, written in Python 3.4.1

## Dependencies
* Python: https://www.python.org/
* Numpy: http://www.numpy.org/
* Docopt: http://www.docopt.org/

## Installation
Install [setuptools](https://pypi.python.org/pypi/setuptools) then do the following:
```
> setup.py install
```
## Usage
```
> regress.py TRAINING_SET TESTING_SET
Results:  correct/total
Accuracy: n%

> regress.py TRAINING_SET TESTING_SET --verbose
W =
[[W1]
 [W2]
  .
  .
  .
 [Wm]]
Results:  correct/total
Accuracy: n%
```
## Data Format
Comma separated numbers, with category being the first number. For example, with 3 categories,
you can represent each category as 1, 2, or 3. Each entry should be on a new line.

Category must be an integer.

The following data

```
1,5.1,3.5,1.4,0.2
2,3.1,1.5,2.4,0.4
```

represents two entries, the first of category 1 and the second of category 2.

Example data are in the data/iris and data/wine folders.

## Training Sets and Testing Sets
regress.py will use the training set to learn a weight matrix that it will apply to the attributes
of each entry in the testing set to predict that entry's category. It will compare its prediction to
the actual category and see if its prediction is correct. After all entries are processed, it will report
its overall accuracy.

The training set must contain at least one example of every category present in the testing set.
