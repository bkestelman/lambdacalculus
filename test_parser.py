import pytest
from parser import parser, LambdaTerm, Variable, Abstraction, Application

def test_parse_variable():
    expr = 'x'
    result = parser.parse(expr)
    assert isinstance(result, LambdaTerm)
    assert isinstance(result, Variable)
    assert str(result) == expr

def test_parse_abstraction():
    expr = '(Lx.x)'
    result = parser.parse(expr)
    assert isinstance(result, LambdaTerm)
    assert isinstance(result, Abstraction)
    assert str(result) == expr
    assert str(result.bound_arg) == 'x'
    assert str(result.expr) == 'x'
    assert result.bound_arg.name == 'x'
    assert result.expr.name == 'x'

def test_parse_application():
    expr = '(xy)'
    result = parser.parse(expr)
    assert isinstance(result, LambdaTerm)
    assert isinstance(result, Application)
    assert str(result) == expr
    assert isinstance(result.lterm, Variable)
    assert isinstance(result.rterm, Variable)
    assert str(result.lterm) == 'x'
    assert str(result.rterm) == 'y'
    assert result.lterm.name == 'x'
    assert result.rterm.name == 'y'

def test_parse_nested_expression():
    expr = '( Lx.( ( Ly.y ) z ) )'
    result = parser.parse(expr)
    assert isinstance(result, LambdaTerm)
    assert isinstance(result, Abstraction)
    assert str(result) == expr.replace(' ', '')
    assert result.bound_arg.name == 'x'
    assert isinstance(result.expr, Application)
    assert str(result.expr) == '((Ly.y)z)'
    assert isinstance(result.expr.lterm, Abstraction)
    assert str(result.expr.lterm) == '(Ly.y)'
    assert isinstance(result.expr.lterm.bound_arg, Variable)
    assert str(result.expr.lterm.bound_arg) == 'y'
    assert isinstance(result.expr.lterm.expr, Variable)
    assert str(result.expr.lterm.expr) == 'y'
    assert isinstance(result.expr.rterm, Variable)
    assert str(result.expr.rterm) == 'z'

def test_parse_left_association():
    expr = 'xy'
    result = parser.parse(expr)
    assert isinstance(result, LambdaTerm)
    assert isinstance(result, Application)
    assert str(result) == f'({expr})'
    expr = '(Lx.x)y'
    result = parser.parse(expr)
    assert isinstance(result, LambdaTerm)
    assert isinstance(result, Application)
    assert str(result) == f'({expr})' 

def test_parse_consecutive_applications():
    expr = '(((ab)c)d)'
    result1 = parser.parse(expr)
    expr = 'abcd'
    result2 = parser.parse(expr)
    assert str(result1) == str(result2)

def test_parse_unknown_symbol():
    expr = '$'
    result = parser.parse(expr)
    assert result is None

