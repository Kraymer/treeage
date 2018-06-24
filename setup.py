# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'pytree', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)
    
with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pytree',
    version=about['__version__'],
    description='list contents of directories in a tree-like format.',
    long_description=readme,
    author='Yan Qian',
    author_email='qianyan.lambda@gmail.com',
    url='https://github.com/qianyan/pytree',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')), #include all packages under pytree
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points = {
        'console_scripts': [
            'pytree = pytree.cli:main'
        ]
    },
    install_requires=['docopt==0.6.2']
)
