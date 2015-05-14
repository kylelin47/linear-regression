# linear-regression
A simple linear regression machine learning program, written in Python 3.4.1

## Dependencies
* Python: https://www.python.org/
* Numpy: http://www.numpy.org/
* Docopt: http://www.docopt.org/

You should not have to install these manually if you follow the instructions under 'Installation'.
## Installation
Install [setuptools](https://pypi.python.org/pypi/setuptools) then do the following:
```
> setup.py install
```
## Training Sets and Testing Sets
regress.py will use the training set to learn a weight matrix that it will apply to the attributes
of each entry in the testing set to predict that entry's category. It will compare its prediction to
the actual category and see if its prediction is correct. After all entries are processed, it will report
its overall accuracy.

The training set must contain at least one example of every category present in the testing set.

## Data Format
Delimiter separated numbers (as specified with the --delimiter flag. defaults to a comma),
with category being the first number. For example, with 3 categories,
you can represent each category as 1 2 or 3. Each entry should be on a new line.

Category must be an integer. Categories should be in sequence, though they do not have to start
from 1.

The following data

```
1,5.1,3.5,1.4,0.2
2,3.1,1.5,2.4,0.4
```

represents two entries, the first of category 1 and the second of category 2.

Example data are in the data/iris and data/wine folders.

Entries with a different number of attributes than the maximum in the training dataset are ignored. For example,

Training
```
1,5.1,3.5,1.4
1,5.1,3.5,1.4,0.2
2,3.1,1.5,2.4
```
Testing
```
1,5.7,4.4,1.5
1,5.4,3.9,1.3,0.4
1,5.1,3.5,1.4,0.3,0.7
```
will be interpreted as

Training
```
1,5.1,3.5,1.4,0.2
```
Testing
```
1,5.4,3.9,1.3,0.4
```

## Example Usage
```
> regress.py TRAINING_SET TESTING_SET
Results:  correct/total
Accuracy: n%

> regress.py TRAINING_SET TESTING_SET --weight
W =
[[W1]
 [W2]
  .
  .
  .
 [Wm]]
Results:  correct/total
Accuracy: n%

> regress.py TRAINING_SET TESTING_SET --verbose
Category 1: correct/total, %
Category 2: correct/total, %
.
.
.
Category N: correct/total, %
Results:  correct/total
Accuracy: n%

> regress.py TRAINING_SET TESTING_SET --delimiter=" : "
Results:  correct/total
Accuracy: n%
```
--delimiter=" : " means your data looks like
```
1 : 0.7 : 0.9 : 2.5
```
--delimiter=, means your data looks like
```
1,0.7,0.9,2.5
```
