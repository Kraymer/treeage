#!/usr/bin env python3
"""list contents of directories in a tree-like format.
  Usage: 
    pytree <dir>
    pytree -h | --help | --version
"""
__version__ = '1.0.0'
import core as tree

def main():
    from docopt import docopt
    arguments = docopt(__doc__, version=__version__)
    dir_name = arguments['<dir>'] 
    print('\n'.join(tree.render_tree(tree.tree_format('', dir_name))))

if __name__ == "__main__":
    main()
