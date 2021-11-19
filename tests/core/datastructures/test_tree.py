import pytest

from core.datastructures import Tree


@pytest.fixture
def tree_single() -> Tree[int]:
    return Tree(1, [])


@pytest.fixture
def tree_multi() -> Tree[int]:
    return Tree(1, [
        Tree(21, [
            Tree(31, []),
            Tree(32, [])
        ]),
        Tree(22, [
            Tree(33, [])
        ]),
        Tree(23, [
            Tree(34, []),
            Tree(35, [])
        ])
    ])


def test_contains_single(tree_single: Tree[int]):
    assert 1 in tree_single
    assert 2 not in tree_single
    assert 10 not in tree_single


def test_iter_single(tree_single: Tree[int]):
    assert [1] == list(tree_single)


def test_len_single(tree_single: Tree[int]):
    assert len(tree_single) == 1


def test_contains_multi(tree_multi: Tree[int]):
    for num in [1, 21, 22, 23, 31, 32, 33, 34, 35]:
        assert num in tree_multi
    assert 2 not in tree_multi
    assert 10 not in tree_multi
    assert 100 not in tree_multi


def test_iter_multi(tree_multi: Tree[int]):
    assert [1, 21, 31, 32, 22, 33, 23, 34, 35] == list(tree_multi)


def test_len_multi(tree_multi: Tree[int]):
    assert len(tree_multi) == 9
