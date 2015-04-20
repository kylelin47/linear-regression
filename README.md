# linear-regression
A simple linear regression machine learning program, written in Python 3.4.1

## Dependencies
* Python: https://www.python.org/
* Numpy: http://www.numpy.org/
* Docopt: http://www.docopt.org/

## Data Formatting
Comma separated numbers, with category being the first number. For example, with 3 categories, represent each category as 1, 2, or 3. Each entry should be on a new line.

Category must be an integer.

The following data

```
1,5.1,3.5,1.4,0.2
2,3.1,1.5,2.4,0.4
```

represents two entries, the first of category 1 and the second of category 2.

Example data are in iris and wine folders.

## Testing sets and training sets
The training set must contain at least one example of each category present in the testing set.

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
