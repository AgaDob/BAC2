from setuptools import setup, find_packages

setup(
    name='bac',

    version='0.0.1.dev1',

    description='Binding affinity calculator',

    long_description='Copy from README file',

    url='http://ccs.chem.ucl.ac.uk',

    author='CCS',

    requires=['yaml'],

    packages=find_packages(),
)
