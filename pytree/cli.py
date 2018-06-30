# -*- coding: utf-8 -*-
# !/usr/bin env python3
"""list contents of directories in a tree-like format.
  Usage:
    pytree <dir>
    pytree -h | --help | --version
"""
import pytree.core as pytree
import pytree.__version__ as version


def main():
    """
    main entry point
    """
    from docopt import docopt
    arguments = docopt(__doc__, version=version.__version__)
    dir_name = arguments['<dir>']
    print('\n'.join(pytree.render_tree(pytree.tree_format('', dir_name))))


if __name__ == "__main__":
    main()
