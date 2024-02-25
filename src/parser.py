from ply.lex import lex, LexToken
from ply.yacc import yacc

tokens = (
  'DECL_FUNC',
  'DECL_VAR',
  'IDENTIFICADOR',
  'NUMERO',
  'STRING',
  'ASIGNACION',
  'ABRE_PAREN',
  'CIERRA_PAREN',
  'ABRE_LLAVE',
  'CIERRA_LLAVE',
  'PUNTO_Y_COMA',
  'SKIP'
)

reserved_map = {
  'function':'DECL_FUNC'
}

for k in ['let','const','var']:
  reserved_map[k] = 'DECL_VAR'

def t_IDENTIFICADOR(t):
  r'[A-Za-z_][\w_]*'
  t.type = reserved_map.get(t.value, "IDENTIFICADOR")
  return t
t_NUMERO = r'(\d*\.\d+)|\d+'
t_STRING = r'("[^"]*")|(\'[^\']*\')'
t_ASIGNACION = r'='
t_ABRE_PAREN = r'\('
t_CIERRA_PAREN = r'\)'
t_ABRE_LLAVE = r'{'
t_CIERRA_LLAVE = r'}'
t_PUNTO_Y_COMA = r';'
def t_SKIP(t):
  r'(\ |\t|\n)+'
  t.type = "SKIP"
  t.lexer.lineno += t.value.count('\n')
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

def p_error(p):
  print(f'Syntax error at {p.value!r}')

''' Un programa puede ser ...
    P -> PU     una lista de declaraciones        p(D) U {.}  : (AST_expresion|AST_decl_variable|AST_decl_funcion):[ P ]
    P -> SF PU  o empezar con skippeables antes   {skip}      : (AST_espacios):[ P ]
'''
def p_programa(p):
  '''
  programa : programa_util
           | sf programa_util
  '''
  p[0] = []
  if len(p) == 3:
    p[0] = p[2]
    p[0].insert(0, p[1])
  else:
    p[0] = p[1]

''' Un programa útil es una lista de declaraciones (no puede empezar con skippeables)
    PU -> .
    PU -> D PU
'''
def p_programa_util(p):
  '''
  programa_util : vacio
                | declaracion programa_util
  '''
  p[0] = []
  if len(p) > 2:
    p[0] = p[2]
    p[0].insert(0, p[1])

''' Un skippeable opcional puede ser ...
    S -> .    vacío                           {.}     : None
    S -> SF   o tener al menos un skippeable  {skip}  : AST_espacios
'''
def p_s(p):
  '''
  s : vacio
    | sf
  '''
  p[0] = p[1]

''' Un skippeable forzado debe tener al menos un skippeable
    SF -> skip    {skip}    : AST_espacios
'''
def p_sf(p):
  '''
  sf : SKIP
  '''
  p[0] = AST_espacios(p[1])

''' Una declaración debe contener algo válido (no puede empezar con skippeables). Puede ser ...
    D -> CMD    un comando                    {id, num, string} : AST_expresion
    D -> DVAR   una declaración de variable   {let, var, const} : AST_decl_variable
    D -> DFUNC  una declaración de función    {function}        : AST_decl_funcion
'''
def p_declaracion(p):
  '''
  declaracion : comando
              | decl_variable
              | decl_funcion
  '''
  p[0] = p[1]

''' Un comando es una expresión que puede tener un cierre (punto y coma y tal vez más skippeables)
    CMD -> E OPT_CIERRE   p(E) : AST_expresion
'''
def p_comando(p):
  '''
  comando : expresion opt_cierre
  '''
  p[0] = p[1]
  p[0].clausura(p[2])

''' Una declaración de variable empieza con un declarador sigue con un identificador y puede tener más cosas
    DVAR -> dvar id M   {dvar} : AST_decl_variable
'''
def p_declaracion_variable(p):
  '''
  decl_variable : DECL_VAR sf IDENTIFICADOR opt_variable1
  '''
  cierre = None
  s_init = None
  s_val = None
  init = p[4]
  if not (init is None):
    cierre = init[3]
    s_val = init[2]
    s_init = init[1]
    init = init[0]
  p[0] = AST_decl_variable(p[3], init, cierre, p[1], p[2], s_init, s_val)

''' Al identificador de la variable declarada puede seguirle ...
  M -> .    nada                                          {.}     : None
  M -> M2   un modificador (cierre y/o asignación)        {; =}   : Lista de 4 (init, None, s_val, cierre)
  M -> SF   al menos un espacio y después un modificador  {skip}  : Lista de 4 (init, s_init, s_val, cierre)
'''
def p_variable_opt1(p):
  '''
  opt_variable1 : vacio
                | opt_variable2
                | sf opt_variable2
  '''
  if p[1] is None:
    p[0] = None
  else:
    opt2 = p[1]
    s_init = None
    s_val = None
    if len(p) > 2:
      opt2 = p[2]
      s_init = p[1]
    p[0] = (opt2[0], s_init, opt2[1], opt2[2])

''' El modificador de la variable declarada puede ser ...
  M2 -> OPT_CIERRE        un cierre                                       {;} : Lista de 3 (None, None, cierre)
  M2 -> = S E OPT_CIERRE  una inicialización seguida (o no) de un cierre  {=} : Lista de 3 (init, s_val, cierre)
'''
def p_variable_opt2(p):
  '''
  opt_variable2 : cierre
                | ASIGNACION s expresion opt_cierre
  '''
  cierre = p[1]
  init = None
  s_val = None
  if len(p) > 2:
    s_val = p[2]
    init = p[3]
    cierre = p[4]
  p[0] = (init, s_val, cierre)

def p_declaracion_funcion(p):
  '''
  decl_funcion : DECL_FUNC sf IDENTIFICADOR s ABRE_PAREN s CIERRA_PAREN s ABRE_LLAVE cuerpo CIERRA_LLAVE
  '''
  p[0] = AST_decl_funcion(p[3], p[10], p[2], p[4], p[6], p[8])

def p_cuerpo_funcion(p):
  '''
  cuerpo : cuerpo_util
         | sf cuerpo_util
  '''
  p[0] = []
  if len(p) == 3:
    p[0] = p[2]
    p[0].insert(0, p[1])
  else:
    p[0] = p[1]

def p_cuerpo_funcion_util(p):
  '''
  cuerpo_util : vacio
              | declaracion cuerpo_util
  '''
  p[0] = []
  if len(p) > 2:
    p[0] = p[2]
    p[0].insert(0, p[1])

def p_expresion(p):
  '''
  expresion : expresion_sin_id
            | expresion_con_id
  '''
  p[0] = p[1]

def p_expresion_sin_id(p):
  '''
  expresion_sin_id : NUMERO s
                   | STRING s
  '''
  p[0] = AST_expresion(p[1])
  if len(p) > 2:
    p[0].clausura(p[2])

def p_expresion_con_id(p):
  '''
  expresion_con_id : IDENTIFICADOR opt_identificador1
  '''
  if (p[2] is None) or isinstance(p[2], AST_espacios):
    p[0] = AST_expresion(p[1], p[2])
  elif len(p[2]) == 4:
    p[0] = AST_invocacion(p[1], p[2][0], p[2][3], p[2][1], p[2][2])
  else:
    p[0] = AST_asignacion(p[1], p[2][0], p[2][1], p[2][2])

def p_opt_identificador1(p): # None, AST_espacios, lista de 3 (val, s_init, s_val) o lista de 4 (args, s_abre, s_cierra, s_fin)
  '''
  opt_identificador1 : vacio
                     | sf opt_identificador2
                     | opt_identificador3
  '''
  if p[1] is None:
    p[0] = None
  else:
    s_1 = None
    opt2 = p[1]
    if len(p) > 2:
      s_1 = p[1]
      opt2 = p[2]
    if opt2 is None:
      p[0] = s_1
    elif len(opt2) == 2:
      p[0] = (opt2[0], s_1, opt2[1]) # es una asignación
    else:
      p[0] = (opt2[0], s_1, opt2[1], opt2[2]) # es una invocación

def p_opt_identificador2(p): # None, lista de 3 (args, s_cierra, s_fin) o lista de 2 (val, s_val)
  '''
  opt_identificador2 : vacio
                     | opt_identificador3
  '''
  p[0] = p[1]

def p_opt_identificador3(p): # Lista de 3 (args, s_cierra, s_fin) o de 2 (val, s_val)
  '''
  opt_identificador3 : ABRE_PAREN s CIERRA_PAREN s
                     | ASIGNACION s expresion
  '''
  if p[1] == '=':
    p[0] = (p[3], p[2])
  else:
    p[0] = (None, p[2], p[4])

def p_vacio(p):
  'vacio :'
  p[0] = None

def p_cierre(p):
  '''
  cierre : PUNTO_Y_COMA s
  '''
  p[0] = p[1] + restore(p[2])

def p_opt_cierre(p):
  '''
  opt_cierre : cierre
             | vacio
  '''
  p[0] = p[1]

class AST_espacios(object):
  def __init__(self, espacios):
    self.espacios = espacios
  def __str__(self):
    return self.espacios
  def restore(self):
    return self.espacios

class AST_decl_variable(object):
  def __init__(self, variable, asignacion=None, cierre=None, decl='let', s_var=None, s_init=None, s_val=None):
    self.decl = decl
    self.s_var = s_var
    self.variable = variable
    self.s_init = s_init
    self.s_val = s_val
    self.asignacion = asignacion
    self.cierre = cierre
  def __str__(self):
    return f"Variable-{self.variable}{show(self.asignacion)}"
  def restore(self):
    init = ''
    if not (self.asignacion is None):
      init = f"{restore(self.s_init)}={restore(self.s_val)}{restore(self.asignacion)}"
    return f"{self.decl}{restore(self.s_var)}{self.variable}{init}{restore(self.cierre)}"

class AST_decl_funcion(object):
  def __init__(self, funcion, cuerpo, s_id=None, s_abreParen=None, s_cierraParen=None, s_abreLlave=None):
    self.s_id = s_id
    self.funcion = funcion
    self.s_abreParen = s_abreParen
    self.s_cierraParen = s_cierraParen
    self.s_abreLlave = s_abreLlave
    self.cuerpo = cuerpo
  def __str__(self):
    cuerpo = '\n\t'.join(list(map(str, self.cuerpo)))
    return f"Fución-{self.funcion}\n\t{cuerpo}\n"
  def restore(self):
    cuerpo = "{" + ''.join(list(map(restore, self.cuerpo))) + "}"
    return f"function{restore(self.s_id)}{self.funcion}{restore(self.s_abreParen)}({restore(self.s_cierraParen)}){restore(self.s_abreLlave)}{cuerpo}"

class AST_invocacion(object):
  def __init__(self, invocacion, args=None, cierre=None, s_abreParen=None, s_cierraParen=None):
    self.invocacion = invocacion
    self.s_abreParen = s_abreParen
    self.s_cierraParen = s_cierraParen
    self.cierre = cierre
  def clausura(self, c):
    self.cierre = texto_con(self.cierre, c)
  def __str__(self):
    return f"Invocación-{self.invocacion}"
  def restore(self):
    return f"{self.invocacion}{restore(self.s_abreParen)}({restore(self.s_cierraParen)}){restore(self.cierre)}"

class AST_asignacion(object):
  def __init__(self, variable, expresion, s_init=None, s_val=None):
    self.variable = variable
    self.s_init = s_init
    self.s_val = s_val
    self.expresion = expresion
  def clausura(self, c):
    self.expresion.clausura(c)
  def __str__(self):
    return f"Asignación-{show(self.variable)} {str(self.expresion)}"
  def restore(self):
    return f"{restore(self.variable)}{restore(self.s_init)}={restore(self.s_val)}{restore(self.expresion)}"

class AST_expresion(object):
  def __init__(self, expresion, cierre=None):
    self.expresion = expresion
    self.cierre = cierre
  def clausura(self, c):
    self.cierre = texto_con(self.cierre, c)
  def __str__(self):
    return f"Expresión-{self.expresion}"
  def restore(self):
    return f"{self.expresion}{restore(self.cierre)}"

def show(x):
  if x is None:
    return ''
  return str(x)

def restore(x):
  if x is None:
    return ''
  if type(x) == type(''):
    return x
  return x.restore()

def texto_con(s1, s2):
  s = ''
  if not (s1 is None):
    s += restore(s1)
  if not (s2 is None):
    s += restore(s2)
  return s

parser = yacc()

def parsear(contenido):
  return parser.parse(contenido)