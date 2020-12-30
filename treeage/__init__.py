# -*- coding: utf-8 -*-

"""Lists contents of directories in a tree-like format with age metric indicated for each file.
"""

import os
import click
from treeage.core import TreeageCore

__version__ = "0.0.1"


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help=__doc__,
)
@click.argument("directory", type=click.Path(exists=True), nargs=1)
@click.option(
    "--maxdepth",
    default=-1,
    metavar="LEVELS",
    help=(
        "Descend at most LEVELS (a non-negative integer) levels of "
        "directories below the seed DIRECTORY"
    ),
)
@click.option(
    "--include",
    "include_glob",
    metavar="GLOB",
    help=("Search only files whose base name matches GLOB (using wildcard matching)"),
)
def treeage_cli(directory, maxdepth, include_glob):
    directory = os.path.abspath(directory)

    TreeageCore(directory, maxdepth, include_glob).dump()
