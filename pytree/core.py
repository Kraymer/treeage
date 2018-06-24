import os

def _children(path):
    return map(lambda filename: tree_format(path, filename), os.listdir(path))

def tree_format(parent, dir_name):
    path = os.path.join(parent, dir_name)
    is_file = os.path.isfile(path) 
    children = [] if is_file else _children(path)
    return {'name': dir_name, 'children': list(children)}
