from setuptools import find_packages, setup

setup(
    name='linear-regression',
    version='0.1',
    install_requires=[
        'Numpy ==1.8.1',
        'Docopt ==0.6.1',
    ],
    packages=find_packages(),
    scripts=[
        'linear-regression/regress.py',
        'linear-regression/scale.py',
    ],
)
