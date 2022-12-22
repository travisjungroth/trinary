from __future__ import annotations

from operator import and_, eq, ge, gt, le, lt, ne, or_, xor

import pytest

from trinary import Trinary, Unknown, UnknownClass, strictly, weakly

ops = [eq, ne, and_, or_, xor, gt, ge, lt, le]
set_to_trinary = {
    frozenset([True]): True,
    frozenset([False]): False,
    frozenset([True, False]): Unknown,
}
trinary_to_set = {v: k for k, v in set_to_trinary.items()}


@pytest.mark.parametrize("p", trinary_to_set)
@pytest.mark.parametrize("q", trinary_to_set)
@pytest.mark.parametrize("op", ops)
def test_logic(op, p, q):
    """
    Test the trinary logic is isomorphic to non-empty sets of bools.
    """
    p_set, q_set = trinary_to_set[p], trinary_to_set[q]
    expected_set = frozenset(op(a, b) for a in p_set for b in q_set)
    expected = set_to_trinary[expected_set]
    actual = op(p, q)
    assert actual is expected


def test_hash():
    tri = [True, False, Unknown, UnknownClass, Trinary]
    d = {k: repr(k) for k in tri}
    for k in tri:
        assert d[k] == repr(k)


def test_invert():
    assert ~Unknown is Unknown


def test_str():
    assert str(Unknown) == "Unknown"
    assert repr(Unknown) == "Unknown"


def test_singleton():
    assert UnknownClass() is Unknown


def test_is_instance():
    for tri in [True, False, Unknown]:
        assert isinstance(tri, Trinary)


@pytest.mark.parametrize("val", ["", 0, 0.0, [], (), {}, set()])
def test_not_is_instance(val):
    assert not isinstance(val, Trinary)


@pytest.mark.parametrize("op", [and_, or_, xor, gt, ge, lt, le])
def test_op_not_implemented(op):
    with pytest.raises(TypeError):
        op(None, Unknown)
    with pytest.raises(TypeError):
        op(Unknown, None)


def test_bool_raises():
    with pytest.raises(TypeError):
        bool(Unknown)


@pytest.mark.parametrize("val", [True, False, [], [0]])
def test_strictly_and_weakly_known(val):
    assert strictly(val) == bool(val)
    assert weakly(val) == bool(val)


def test_strictly_and_weakly():
    assert strictly(Unknown) is False
    assert weakly(Unknown) is True
