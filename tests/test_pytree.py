"""
test_pytree.py
"""
import pytree.core as pytree

def test_tree_format():
    actual_tree = pytree.tree_format('tests', 'fixtures') 
    expected_tree = {'name': 'fixtures', 'children': [{'name': 'child', 'children': []}]}
    assert actual_tree == expected_tree
