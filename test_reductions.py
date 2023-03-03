import pytest
from parser import parser, LambdaTerm, Variable, Abstraction, Application

def test_identity_reduction():
    expr = '((Lx.x)y)'
    result = parser.parse(expr)
    assert result.is_reducible()
    result = result.beta_reduce()
    assert not result.is_reducible()
    assert isinstance(result, Variable)
    assert str(result) == 'y'

def test_simple_reduction():
    expr = '((Lx.(xx))y)'
    result = parser.parse(expr)
    assert result.is_reducible()
    result = result.beta_reduce()
    assert not result.is_reducible()
    assert isinstance(result, Application)
    assert str(result) == '(yy)'

def test_reduce_abstraction():
    expr = '(Lx.((Ly.y)x))'
    result = parser.parse(expr)
    assert result.is_reducible()
    result = result.beta_reduce()
    assert not result.is_reducible()
    assert isinstance(result, Abstraction)
    assert str(result) == '(Lx.x)'

def test_reduce_constant_function():
    expr = '((Lx.(yz))a)'
    result = parser.parse(expr)
    assert result.is_reducible()
    result = result.beta_reduce()
    assert not result.is_reducible()
    assert str(result) == '(yz)'

def test_reduction_loop():
    expr = '(Lx.((Ly.y)x))'
    result = parser.parse(expr)
    while result.is_reducible():
        result = result.beta_reduce()
    assert str(result) == '(Lx.x)'

def test_reduce_left_association():
    expr = 'xy'
    result = parser.parse(expr)
    assert not result.is_reducible()
    expr = '(Lx.xx)y'
    result = parser.parse(expr)
    assert result.is_reducible()
    result = result.beta_reduce()
    assert not result.is_reducible()
    assert str(result) == '(yy)'

