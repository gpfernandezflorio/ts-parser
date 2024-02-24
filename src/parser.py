from ply.lex import lex, LexToken
from ply.yacc import yacc

tokens = (
  'IDENTIFICADOR',
  'ABRE_PAREN',
  'CIERRA_PAREN',
  'PUNTO_Y_COMA',
  'ESPACIO',
  'TAB',
  'SALTO_DE_LINEA'
)

t_IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ABRE_PAREN = r'\('
t_CIERRA_PAREN = r'\)'
t_PUNTO_Y_COMA = r';'
t_ESPACIO = r'\ '
t_TAB = r'\t'
def t_SALTO_DE_LINEA(t):
  r'\n'
  t.lexer.lineno += 1
  return t

def t_error(t):
  t.value = t.value[0]
  t.lexer.skip(1)
  return t

def tokenizar(contenido):
  lexer = lex()
  lexer.input(contenido)
  resultado = []
  while True:
    t = lexer.token()
    if not t:
        break
    resultado.append(t)
  return resultado

def token(tipo, valor, linea, pos):
  t = LexToken()
  t.type = tipo
  t.value = valor
  t.lineno = linea
  t.lexpos = pos
  return t

precedence = (
  ('right', 'ESPACIO', 'TAB', 'SALTO_DE_LINEA'),
)

def p_error(p):
  print(f'Syntax error at {p.value!r}')

def p_programa(p):
  '''
  programa : declaracion programa
           | vacio
  '''
  if len(p) > 2:
    p[0] = p[2]
    p[0].insert(0, p[1])
  else:
    p[0] = []

def p_declaracion_comando(p):
  '''
  declaracion : comando
  '''
  p[0] = p[1]

def p_declaracion_espacios(p):
  '''
  declaracion : ESPACIO espacios
              | TAB espacios
              | SALTO_DE_LINEA espacios
  '''
  p[0] = AST_espacios(p[1] + p[2])

def p_espacios(p):
  '''
  espacios : espacios ESPACIO
           | espacios TAB
           | espacios SALTO_DE_LINEA
           | vacio
  '''
  p[0] = p[1]
  if len(p) > 2:
    p[0] += p[2]

def p_comando_invocacion(p):
  '''
  comando : invocacion opt_punto_y_coma
  '''
  p[0] = AST_comando(p[1], p[2])

def p_opt_punto_y_coma(p):
  '''
  opt_punto_y_coma : PUNTO_Y_COMA
                   | vacio
  '''
  p[0] = p[1]

def p_invocacion(p):
  '''
  invocacion : IDENTIFICADOR ABRE_PAREN CIERRA_PAREN
  '''
  p[0] = AST_invocacion(p[1])

def p_vacio(p):
  'vacio :'
  p[0] = ''

class AST_espacios(object):
  def __init__(self, espacio):
    self.espacio = espacio
  def __str__(self):
    return 'Espacio-' + self.espacio.replace('\n','\\n').replace('\t','\\t')

class AST_comando(object):
  def __init__(self, comando, cierre):
    self.comando = comando
    self.cierre = cierre
  def __str__(self):
    return 'Comando-' + str(self.comando) + self.cierre

class AST_invocacion(object):
  def __init__(self, invocacion):
    self.invocacion = invocacion
  def __str__(self):
    return 'Invocación-' + self.invocacion

parser = yacc()

def parsear(contenido):
  return parser.parse(contenido)