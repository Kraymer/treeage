# -*- coding: utf-8 -*-

import arrow
import blessed
import os
import math
import re
import functools as fp

I_branch = "│   "
T_branch = "├── "
L_branch = "└── "
SPACER = "    "

term = blessed.Terminal()
all_dates = {}


def _children(path):
    if os.path.isfile(path):
        return []
    return [tree_format(path, fname) for fname in os.listdir(path)]


def _date(path):
    if os.path.isfile(path):
        filedate = os.stat(path).st_ctime
        all_dates[path] = filedate
        return filedate


def tree_format(parent, dir_name):
    path = os.path.join(parent, dir_name)
    return {"name": dir_name, "children": _children(path), "date": _date(path)}


def render_tree(tr):
    name = tr["name"]
    children = tr["children"]
    # res = ["{}{}".format(render_date(tr["date"]), name)] + fp.reduce(
    res = [name] + fp.reduce(
        lambda l, r: l + r,
        map(lambda arg: render(len(children))(*arg), enumerate(children)),
        [],
    )
    return res


def render(length):
    def prefix(index, child):
        is_last = index == length - 1
        # prefix_first = prefix_rest = render_date(child["date"])
        prefix_first = L_branch if is_last else T_branch
        prefix_rest = SPACER if is_last else I_branch
        tr = render_tree(child)
        head = prefix_first + tr[0]
        tail = [prefix_rest + t for t in tr[1:]]
        res = [head] + tail
        # import ipdb

        # ipdb.set_trace()
        return res

    return prefix


def render_date(date):
    if not date:
        return ""
    rgb_max = 255.0
    min_date = min(all_dates.values())
    max_date = max(all_dates.values())

    step_lin = (max_date - min_date) / rgb_max
    gray_level_lin = int((date - min_date) / step_lin)

    try:
        gray_level = int(gray_level_lin * math.log(gray_level_lin) / math.log(rgb_max))
    except ValueError:
        gray_level = 0

    date_human = arrow.get(date).humanize(only_distance=True)
    return term.on_color_rgb(gray_level, gray_level, gray_level)(date_human[:4])


def prefix_date(tree):
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
            res.append("{} {}".format(render_date(all_dates[fullpath]), line))
        else:
            res.append("     " + line)
    return res
