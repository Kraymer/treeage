#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import logging
import os
import math
import re
import functools as fp
from pathlib import Path
from statistics import mean

import arrow
from git import Repo

from treeage import terminal

I_branch = "│   "
T_branch = "├── "
L_branch = "└── "
SPACER = "    "

logger = logging.getLogger(__name__)
term = terminal.Terminal()


def repo_path_for(filename):
    """Go up filename path and returns path of first repository met."""

    current_path = filename
    while current_path != "/":
        if os.path.exists(os.path.join(current_path, ".git")):
            return current_path
        current_path = os.path.dirname(current_path)

    logger.error("'{}' is not tracked by a git repository".format(filename))
    exit(1)


def list_paths(root_tree, path=Path(".")):
    """Return paths contained in a git repo tree"""
    for blob in root_tree.blobs:
        yield path / blob.name
    for tree in root_tree.trees:
        yield from list_paths(tree, path / tree.name)


def path_depth(root, filepath):
    """Get the depth of filepath from the root"""
    depth = 0
    if filepath:
        rel_path = os.path.relpath(filepath, root)
        if rel_path != ".":
            depth += 1
        depth += rel_path.count(os.path.sep)
    return depth


def abbr_date(date):
    """Convert date to human abbreviated format"""
    date_human = arrow.get(date).humanize(only_distance=True)
    # date_human = re.sub(r"years?", "y", date_human)
    date_human = re.sub(r"months?", "mon", date_human)
    # date_human = re.sub(r"minutes?", "min", date_human)
    date_human = re.sub(r"^an? ", "1 ", date_human)
    return date_human


class TreeageCore:
    def __init__(self, root, maxdepth, include_glob, before, after):
        """Render aged tree for dirpath"""
        self.all_dates = {}
        self.maxdepth = maxdepth
        self.before = before
        self.after = after
        self.root = root
        self.repo_path = repo_path_for(self.root)
        self.repo = Repo(self.repo_path)
        self.glob = include_glob
        self.repo_files = set(
            os.path.join(self.repo_path, str(x)) for x in list_paths(self.repo.tree())
        )
        self.repo_files |= set([os.path.dirname(x) for x in self.repo_files])
        tree = self.tree_format("", self.root)
        tree_rendered = self.render_tree(tree)
        self.rendering = self.prefix_date(tree_rendered)

    def dump(self):
        print(term.clear_last)
        print("\n".join(self.rendering))

    def _children(self, path):
        """Return list of trees for path children"""
        if os.path.isfile(path):
            return []
        children = set(
            [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
        )
        children |= set(
            glob.iglob(os.path.join(path, self.glob)) if self.glob else os.listdir(path)
        )
        paths = set(os.path.join(path, fname) for fname in children) & self.repo_files
        return [
            self.tree_format(path, os.path.basename(fname)) for fname in sorted(paths)
        ]

    def _date(self, path):
        """Return estimated date of filepath by averaging editing dates of each
        line.
        """
        print(u"processing {}".format(path), end="")
        print(term.clear_last)
        if os.path.isfile(path) and path in self.repo_files:
            lines_dates = []
            try:
                for commit, lines in self.repo.blame("HEAD", path):
                    if any(lines):
                        lines_dates.extend([commit.committed_date] * len(lines))
            except Exception as e:
                print(e)
                pass
            if lines_dates:
                filedate = mean(lines_dates)
            else:  # time of most recent content modification.
                filedate = os.stat(path).st_mtime
            self.all_dates[path] = filedate
            return filedate

    def tree_format(self, parent, dir_name):
        """Return tree for dir_name"""
        depth = path_depth(self.root, parent)
        path = os.path.join(parent, dir_name)
        children = []
        if not parent or self.maxdepth < 0 or depth < self.maxdepth:
            children = self._children(path)
        res = {"name": dir_name, "children": children, "date": self._date(path)}
        return res

    def render_tree(self, tree):
        """Render tree"""
        name = tree["name"]
        children = tree["children"]
        if self.after:
            children = [x for x in children if not x["date"] or x["date"] > self.after]
            self.all_dates = {
                k: v for (k, v) in self.all_dates.items() if v > self.after
            }
        if self.before:
            children = [x for x in children if not x["date"] or x["date"] < self.before]
            self.all_dates = {
                k: v for (k, v) in self.all_dates.items() if v < self.before
            }
        res = [name] + fp.reduce(
            lambda l, r: l + r,
            map(lambda arg: self.render(len(children))(*arg), enumerate(children)),
            [],
        )
        return res

    def render(self, length):
        def prefix(index, child):
            """Render a tree element"""
            is_last = index == length - 1
            prefix_first = L_branch if is_last else T_branch
            prefix_rest = SPACER if is_last else I_branch
            tr = self.render_tree(child)
            head = prefix_first + tr[0]
            tail = [prefix_rest + t for t in tr[1:]]
            res = [head] + tail
            return res

        return prefix

    def render_date(self, date):
        """Return color for dates based on all dates"""
        if not date:
            return ""
        rgb_max = 255
        min_date = min(self.all_dates.values())
        max_date = max(self.all_dates.values())

        step_lin = (max_date - min_date) / rgb_max
        try:
            gray_level_lin = int((date - min_date) / step_lin)
            gray_level = int(
                gray_level_lin * math.log(gray_level_lin) / math.log(rgb_max)
            )
        except ValueError:
            gray_level = 0
        except ZeroDivisionError:
            gray_level = rgb_max

        font_color = term.white if gray_level < rgb_max / 2.0 else term.black

        date_abbr = abbr_date(date)[:6].rjust(6)
        return font_color(
            term.on_color_rgb(gray_level, gray_level, gray_level)(date_abbr)
        )

    def prefix_date(self, tree):
        """Return rendered tree obtained by prefixing each element by its color"""
        walk = {}
        res = []

        for line in tree:
            m = re.search(r"(\w|\.|/)+", line)
            index = m.start()
            filename = line[index:]
            walk[m.start()] = filename
            fullpath = ""
            for i in range(0, index + 1, 4):
                fullpath = os.path.join(fullpath, walk[i])
            if fullpath in self.all_dates:
                res.append(
                    "{} {}".format(self.render_date(self.all_dates[fullpath]), line)
                )
            else:
                res.append("       " + line)
        return res
