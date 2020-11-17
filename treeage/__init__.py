# -*- coding: utf-8 -*-
# !/usr/bin env python3

import os
import blessed
import click
from treeage import core


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="Lists contents of directories in a tree-like format with age metric indicated for each file",
)
@click.argument("directory", type=click.Path(exists=True), nargs=1)
def treeage_cli(directory):
    directory = os.path.abspath(directory)
    tree = core.tree_format("", directory)
    tree_rendered = core.render_tree(tree)
    tree_date = core.prefix_date(tree_rendered)
    print("\n".join(tree_date))


if __name__ == "__main__":
    treeage_cli()
