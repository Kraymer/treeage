.. image:: http://travis-ci.com/Kraymer/treeage.svg
   :target: http://travis-ci.com/Kraymer/treeage
   
.. image:: https://coveralls.io/repos/github/Kraymer/treeage/badge.svg?branch=main
   :target: https://coveralls.io/github/Kraymer/treeage

treeage
=======

    **/ˈtreeage/**
    
    | 1. *n.* a process in which things are ranked in terms of importance or priority.
    | 2. *n.* software that lists contents of directories in a tree-like format with age metric indicated for each file

``treeage`` display is typically used to shed some light on antiquated parts of a codebase and identify candidates for a refactoring.

Usage
-----

::

    Usage: treeage.py [OPTIONS] DIRECTORY   

      Lists contents of directories in a tree-like format with age metric
      indicated for each file   

    Options:
      --maxdepth LEVELS  Descend at most LEVELS (a non-negative integer) levels of
                         directories below the seed DIRECTORY   

      --include GLOB     Search only files whose base name matches GLOB (using
                         wildcard matching)
