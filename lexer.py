import ply.lex as lex

tokens = (
        'LAMBDA',
        'DOT',
        'LPAREN',
        'RPAREN',
        'VARIABLE',
        'NUMBER',
        )

t_LAMBDA = r'L'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_VARIABLE = r'[a-z]'
t_NUMBER = r'[0-9]+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

