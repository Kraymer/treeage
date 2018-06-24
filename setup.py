# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pytree',
    version='1.0.0',
    description='list contents of directories in a tree-like format.',
    long_description=readme,
    author='Yan Qian',
    author_email='qianyan.lambda@gmail.com',
    url='https://github.com/qianyan/pytree',
    license=license,
    packages=find_packages('pytree', exclude=('tests', 'docs')), #include all packages under pytree
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    package_dir={'': 'pytree'},  #tell distutils packages are under pytree
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points = {
        'console_scripts': [
            'pytree = cli:main'
        ]
    },
    install_requires=['docopt==0.6.2']
)
