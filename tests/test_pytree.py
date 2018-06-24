"""
test_pytree.py
"""
import pytree.core as pytree

def test_tree_format():
    actual_tree = pytree.tree_format('tests', 'fixtures') 
    expected_tree = {'name': 'fixtures', 'children': [{'name': 'child', 'children': []}]}
    assert actual_tree == expected_tree

def test_render_tree():
    tree_format = {'name': 'fixtures', 'children': [{'name': 'child', 'children': []}]}
    actual_render_tree = pytree.render_tree(tree_format)
    expected_render_tree = ['fixtures', '└── child']
    assert actual_render_tree == expected_render_tree
