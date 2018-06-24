import os
import functools as fp

I_branch = "│   "
T_branch = "├── "
L_branch = "└── "
SPACER   = "    "

def _children(path):
    return map(lambda filename: tree_format(path, filename), os.listdir(path))

def tree_format(parent, dir_name):
    path = os.path.join(parent, dir_name)
    is_file = os.path.isfile(path) 
    children = [] if is_file else _children(path)
    return {'name': dir_name, 'children': list(children)}

def render_tree(tr):
    name = tr['name']
    children = tr['children']
    return [name] + fp.reduce(lambda l, r: l + r, 
                           map(lambda arg: render(len(children))(*arg), enumerate(children)), 
                           [])

def render(length):
    def prefix(index, child):
        is_last = (index == length - 1)
        prefix_first = L_branch if is_last else T_branch
        prefix_rest = SPACER if is_last else I_branch
        tr = render_tree(child)
        head = prefix_first + tr[0]
        tail = [prefix_rest + t for t in tr[1:]]
        return [head] + tail
    return prefix
