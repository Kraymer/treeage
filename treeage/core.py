# -*- coding: utf-8 -*-

import arrow
import blessed
import os
import math
import re
import functools as fp

from pathlib import Path
from git import Repo

I_branch = "│   "
T_branch = "├── "
L_branch = "└── "
SPACER = "    "

term = blessed.Terminal()
all_dates = {}


def repo_path_for(filename):
    """Go up filename path and returns path of first repository met."""
    while filename:
        filename = os.path.dirname(filename)
        if os.path.exists(os.path.join(filename, ".git")):
            return filename


def list_paths(root_tree, path=Path(".")):
    for blob in root_tree.blobs:
        yield path / blob.name
    for tree in root_tree.trees:
        yield from list_paths(tree, path / tree.name)


class TreeageCore():
    def __init__(self, dirpath):
        """Render aged tree for dirpath
        """
        self.repo_path = repo_path_for(dirpath)
        self.repo = Repo(self.repo_path)
        self.repo_files = [str(x) for x in list_paths(self.repo.tree())]
        tree = self.tree_format("", dirpath)
        tree_rendered = self.render_tree(tree)
        tree_aged_rendered = self.prefix_date(tree_rendered)
        print("\n".join(tree_aged_rendered))

    def _children(self, path):
        """Return list of trees for path children"""
        if os.path.isfile(path):
            return []
        return [self.tree_format(path, fname) for fname in os.listdir(path)]

    def _date(self, path):
        """Return estimated date of filepath by averaging editing dates of each
           line.
        """
        if os.path.isfile(path) and path.endswith(".py"):
            lines_dates = []
            relative_filename = path.split(self.repo_path)[-1].strip("/")
            if relative_filename in self.repo_files:

                try:
                    for commit, lines in self.repo.blame('HEAD', path):
                        if any(lines):
                            lines_dates.extend([commit.committed_date] * len(lines))
                except Exception as e:
                    print(e)
                    pass
            if lines_dates:
                filedate = sum(lines_dates) / len(lines_dates)
            else:
                filedate = os.stat(path).st_ctime
            all_dates[path] = filedate
            return filedate

    def tree_format(self, parent, dir_name):
        """Return tree for dir_name
        """
        path = os.path.join(parent, dir_name)
        return {"name": dir_name, "children": self._children(path), "date": self._date(path)}

    def render_tree(self, tree):
        """Render tree
        """
        name = tree["name"]
        children = tree["children"]
        res = [name] + fp.reduce(
            lambda l, r: l + r,
            map(lambda arg: self.render(len(children))(*arg), enumerate(children)),
            [],
        )
        return res

    def render(self, length):
        def prefix(index, child):
            """Render a tree element
            """
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
        """Return color for dates based on all dates
        """
        if not date:
            return ""
        rgb_max = 255
        min_date = min(all_dates.values())
        max_date = max(all_dates.values())

        step_lin = (max_date - min_date) / rgb_max
        try:
            gray_level_lin = int((date - min_date) / step_lin)
            gray_level = int(gray_level_lin * math.log(gray_level_lin) / math.log(rgb_max))
        except ValueError:
            gray_level = 0
        except ZeroDivisionError:
            gray_level = rgb_max

        date_human = arrow.get(date).humanize(only_distance=True)
        font_color = term.white if gray_level < rgb_max / 2.0 else term.black
        date_shortcut = " ".join([x[:3] for x in date_human.split()]).ljust(6)
        return font_color(term.on_color_rgb(gray_level, gray_level, gray_level)(date_shortcut))

    def prefix_date(self, tree):
        """Return rendered tree obtained by prefixing each element by its color
        """
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
            if fullpath in all_dates:
                res.append("{} {}".format(self.render_date(all_dates[fullpath]), line))
            else:
                res.append("       " + line)
        return res
