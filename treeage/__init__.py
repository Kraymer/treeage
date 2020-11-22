# -*- coding: utf-8 -*-
# !/usr/bin env python3

import os
import click
from treeage.core import TreeageCore


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="Lists contents of directories in a tree-like format with age metric indicated for each file",
)
@click.argument("directory", type=click.Path(exists=True), nargs=1)
@click.option("--fast/--no-fast", default=False)
@click.option("--maxdepth", default=-1)
def treeage_cli(directory, fast, maxdepth):
    directory = os.path.abspath(directory)

    TreeageCore(directory, fast, maxdepth)


if __name__ == "__main__":
    treeage_cli()
