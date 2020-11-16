# -*- coding: utf-8 -*-
# !/usr/bin env python3

import blessed
from treeage import core


def main():
    """
    main entry point
    """
    tree = core.tree_format("", "../../jlmcc/apps")
    tree_rendered = core.render_tree(tree)
    tree_date = core.prefix_date(tree_rendered)
    print("\n".join(tree_date))


if __name__ == "__main__":
    main()
    # for x in range(100):
    #     print(term.on_color_rgb(x, x, x)("a"))
