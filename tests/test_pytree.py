"""
test_pytree.py
"""
import pytree.core as pytree

def test_tree_format():
    assert pytree.tree_format('tests', 'fixtures') == {'name': 'fixtures', 'children': []}
