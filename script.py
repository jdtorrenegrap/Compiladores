import ply.lex as lex
import ply.yacc as yacc

# Tabla de símbolos para almacenar variables
symbol_table = {}

# ------------------- LÉXICO -------------------

tokens = (
    'ID', 'ASSIGN', 'NUMBER', 'STRING',
    'PLUS', 'TIMES', 'LPAREN', 'RPAREN', 'COMMA', 'SEMICOLON',
    'MENSAJE', 'PUNTO', 'TEXTO',
)

t_ASSIGN    = r'='
t_PLUS      = r'\+'
t_TIMES     = r'\*'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMMA     = r','
t_SEMICOLON = r';'
t_PUNTO     = r'\.'
t_ignore    = ' \t'

def t_MENSAJE(t):
    r'Mensaje'
    return t

def t_TEXTO(t):
    r'Texto'
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value.strip('"')
    return t

def t_NUMBER(t):
    r'\d+(,\d+)?'
    t.value = float(t.value.replace(',', '.'))
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Caracter ilegal:", t.value[0])
    t.lexer.skip(1)

# ------------------- SINTAXIS -------------------

def p_sentencias(p):
    '''sentencias : sentencias sentencia
                  | sentencia'''

def p_sentencia_asignacion(p):
    'sentencia : ID ASSIGN expresion SEMICOLON'
    symbol_table[p[1]] = p[3]
    print(f"Asignación: {p[1]} = {p[3]}")

def p_sentencia_mensaje(p):
    'sentencia : MENSAJE PUNTO TEXTO LPAREN STRING RPAREN SEMICOLON'
    print(f"Mensaje mostrado: {p[5]}")

def p_expresion_binaria(p):
    '''expresion : expresion PLUS expresion
                 | expresion TIMES expresion'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]

def p_expresion_paren(p):
    'expresion : LPAREN expresion RPAREN'
    p[0] = p[2]

def p_expresion_num(p):
    'expresion : NUMBER'
    p[0] = p[1]

def p_expresion_string(p):
    'expresion : STRING'
    p[0] = p[1]

def p_expresion_id(p):
    'expresion : ID'
    if p[1] in symbol_table:
        p[0] = symbol_table[p[1]]
    else:
        print(f"Error: variable '{p[1]}' no definida")
        p[0] = 0

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis")

# ------------------- EJECUCIÓN -------------------

lexer = lex.lex()
parser = yacc.yacc()

print("MiniIntérprete (escribe tus comandos):")
while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    if not s:
        continue
    parser.parse(s)
