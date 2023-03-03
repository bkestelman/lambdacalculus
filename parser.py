'''
Credit to https://stackoverflow.com/a/15171626/4542084 for an unambiguous
grammar for lambda calculus
'''
import copy
import ply.yacc as yacc

from lexer import tokens

class LambdaTerm():
    def __init__(self):
        pass

class Variable(LambdaTerm):
    def __init__(self, name):
        self.name = name

    def substitute(self, bound_arg, replacement_term):
        if bound_arg.name == self.name:
            return copy.deepcopy(replacement_term)
        return self

    def beta_reduce(self):
        return self

    def is_reducible(self):
        return False

    def __str__(self):
        return self.name

class Abstraction(LambdaTerm):
    def __init__(self, bound_arg, expr):
        self.bound_arg = bound_arg
        self.expr = expr

    def applyTo(self, other):
        return self.substitute(self.bound_arg, other)

    def substitute(self, bound_arg: Variable, replacement_term):
        self.expr = self.expr.substitute(bound_arg, replacement_term)
        return self.expr

    def beta_reduce(self):
        self.expr = self.expr.beta_reduce()
        return self

    def is_reducible(self):
        return self.expr.is_reducible()

    def __str__(self):
        return '(L' + str(self.bound_arg) + '.' + str(self.expr) + ')'

class Application(LambdaTerm):
    def __init__(self, lterm, rterm):
        self.lterm = lterm
        self.rterm = rterm

    def beta_reduce(self):
        print('beta reducing', self)
        if isinstance(self.lterm, Variable):
            return self
        if isinstance(self.lterm, Abstraction):
            return self.lterm.applyTo(self.rterm)
        if isinstance(self.lterm, Application):
            self.lterm = self.lterm.beta_reduce()
            return self

    def is_reducible(self):
        return (
            self.lterm.is_reducible() or 
            self.rterm.is_reducible() or 
            isinstance(self.lterm, Abstraction)
            )

    def substitute(self, bound_arg, replacement_term):
        self.lterm = self.lterm.substitute(bound_arg, replacement_term)
        self.rterm = self.rterm.substitute(bound_arg, replacement_term)
        return self

    def __str__(self):
        return '(' + str(self.lterm) + str(self.rterm) + ')'

def p_term_application(p):
    '''term : application
            | abstraction'''
    p[0] = p[1]

def p_abstraction(p):
    'abstraction : LAMBDA VARIABLE DOT term'
    p[0] = Abstraction(bound_arg=Variable(p[2]), expr=p[4])

def p_application(p):
    'application : application atomic'
    p[0] = Application(p[1], p[2])

def p_application_atomic(p):
    'application : atomic'
    p[0] = p[1]

def p_atomic(p):
    'atomic : VARIABLE'
    p[0] = Variable(p[1])

def p_atomic_closed(p):
    'atomic : LPAREN term RPAREN'
    p[0] = p[2]

def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")

parser = yacc.yacc(debug=True)

if __name__ == '__main__':
    while True:
        try:
            s = input('lambda > ')
        except EOFError:
            break
        if not s: 
            continue
        result = parser.parse(s)
        print(result)
        print(result.value)

