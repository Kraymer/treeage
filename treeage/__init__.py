#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Lists contents of directories in a tree-like format with age metric indicated for each file.
"""

import logging
import os

import click
import click_log
import dateparser

from treeage.core import TreeageCore

__version__ = "0.2.0"

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def parse_date(text):
    """Return POSIX timestamp obtained from parsing date and time from given
    date string.

    Return None if no text given.
    """
    if text:
        return dateparser.parse(text).timestamp()


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help=__doc__,
    epilog=(
        """\b\nExamples:
treeage --maxdepth 2 --before "01 jan 2018"../qifqif
treeage --include "*.py" --after "3 month ago" .
        """
    ),
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
    help=("List only files whose base name matches GLOB (using wildcard matching)"),
)
@click.option(
    "--before", metavar="DATE", help=("List only files whose age is older than DATE")
)
@click.option(
    "--after", metavar="DATE", help=("List only files whose age is lower than DATE")
)
@click_log.simple_verbosity_option(logger)
@click.version_option(__version__)
def treeage_cli(directory, maxdepth, include_glob, before, after):
    directory = os.path.abspath(directory)
    TreeageCore(
        directory, maxdepth, include_glob, parse_date(before), parse_date(after)
    ).dump()
