from setuptools import setup

setup(
    name='regress',
    version='0.1',
    install_requires=[
        'numpy ==1.9.2',
        'docopt ==0.6.2',
    ],
    scripts=[
        'linear-regression/regress.py',
        'linear-regression/scale.py',
    ],
)
