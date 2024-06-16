from ply.lex import lex, LexToken
from ply.yacc import yacc

tokens = (
  'DECL_FUNC',
  'DECL_VAR',
  'IDENTIFICADOR',
  'NUMERO',
  'STRING',
  'COMENTARIO_UL',
  'COMENTARIO_ML',
  'ASIGNACION',
  'ABRE_PAREN',
  'CIERRA_PAREN',
  'ABRE_LLAVE',
  'CIERRA_LLAVE',
  'PUNTO_Y_COMA',
  'PUNTO',
  'COMA',
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
t_COMENTARIO_UL = r'//[^\n\r]*'
def t_COMENTARIO_ML(t):
  r'/\*([^\*]|\*[^/])*\*/'
  t.type = "COMENTARIO_ML"
  t.lexer.lineno += t.value.count('\n')
  return t
t_ASIGNACION = r'='
t_ABRE_PAREN = r'\('
t_CIERRA_PAREN = r'\)'
t_ABRE_LLAVE = r'{'
t_CIERRA_LLAVE = r'}'
t_PUNTO_Y_COMA = r';'
t_PUNTO = r'\.'
t_COMA = r','
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
  print(f'Error en línea {p.lineno} {p.value!r}')
  exit(1)

''' Un programa puede ser ...
    P -> PU     una lista de declaraciones        p(D) U {.}  : ( AST_expresion
                                                                | AST_invocacion
                                                                | AST_asignacion
                                                                | AST_decl_variable
                                                                | AST_decl_funcion
                                                                | AST_funcion
                                                                | AST_comentario
                                                                ):[ P ]
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
    D -> CMD    un comando (sin function)     {id, num, string} : AST_expresion | AST_invocacion | AST_asignacion
    D -> DVAR   una declaración de variable   {let, var, const} : AST_decl_variable
    D -> DFUNC  una declaración de función    {function}        : AST_decl_funcion | AST_funcion
    D -> REM    un comentario                 {// | /*}         : AST_comentario
'''
def p_declaracion(p):
  '''
  declaracion : comando
              | decl_variable
              | decl_funcion
              | comentario
  '''
  p[0] = p[1]

''' Un comando es una expresión (que no empiece con function) que puede tener un cierre (punto y coma y tal vez más skippeables)
    CMD -> E OPT_CIERRE   p(E) : AST_expresion | AST_invocacion | AST_asignacion
'''
def p_comando(p):
  '''
  comando : expresion_no_function opt_cierre
  '''
  p[0] = p[1]
  p[0].clausura(p[2])

''' Una declaración de variable empieza con un declarador sigue con un identificador y puede tener más cosas
    DVAR -> dvar id M   {dvar} : AST_decl_variable
'''
def p_declaracion_variable(p):
  '''
  decl_variable : DECL_VAR sf identificador_declarable opt_variable1
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
  decl_funcion : DECL_FUNC s funcion opt_invocacion opt_cierre
  '''
  if len(p[3]) == 5:
    p[0] = AST_decl_funcion(p[3][0], p[3][1], p[2], p[3][2], p[3][3], p[3][4])
  else:
    p[0] = AST_funcion(p[3][0], p[2], p[3][1], p[3][2])
    if not (p[4] is None):
      p[0] = AST_invocacion(p[0], p[4][0], p[4][1], p[4][2], p[4][3])
  if not (p[5] is None):
    p[0].clausura(p[5])

def p_funcion(p): # Lista de 5 si es una definición (id, cuerpo, s_id, s_abre, s_cierra) y de 3 si es una expresión (cuerpo, s_abre, s_cierra)
  '''
  funcion : funcion_no_decl
          | IDENTIFICADOR s ABRE_PAREN s CIERRA_PAREN s ABRE_LLAVE cuerpo CIERRA_LLAVE
  '''
  if len(p) == 2: # Es una expresión del tipo function(){}
    p[0] = p[1]
  else:           # es una definición
    p[0] = (p[1], p[8], p[2], p[4], p[6])

def p_funcion_no_decl(p): # Lista de 3 (cuerpo, s_abre, s_cierra)
  '''
  funcion_no_decl : ABRE_PAREN s CIERRA_PAREN s ABRE_LLAVE cuerpo CIERRA_LLAVE
  '''
  p[0] = (p[6], p[2], p[4])

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

def p_expresion(p): # AST_expresion | AST_invocacion | AST_asignacion | AST_funcion
  '''
  expresion : DECL_FUNC sf funcion_no_decl opt_invocacion
            | expresion_no_function
  '''
  if len(p) == 5: # Es una expresión del tipo function(){}
    p[0] = AST_funcion(p[3][0], p[2], p[3][1], p[3][2])
    if not (p[4] is None):
      p[0] = AST_invocacion(p[0], p[4][0], p[4][1], p[4][2], p[4][3])
  else:
    p[0] = p[1]


def p_expresion_no_function(p): # AST_expresion | AST_invocacion | AST_asignacion
  '''
  expresion_no_function : expresion_sin_id
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
  expresion_con_id : identificador_asignable opt_identificador1
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
  opt_identificador3 : ABRE_PAREN s argumentos CIERRA_PAREN s
                     | ASIGNACION s expresion
  '''
  if p[1] == '=':
    p[0] = (p[3], p[2])
  else:
    p[0] = (p[3], p[2], p[5])

def p_opt_invocacion(p): # None o lista de 3 (args, s_cierra, s_fin)
  '''
  opt_invocacion : vacio
                 | s ABRE_PAREN s argumentos CIERRA_PAREN s
  '''
  if len(p) == 2:
    p[0] = None
  else:
    p[0] = (p[4], p[6], p[1], p[3])

def p_identificador_asignable(p): # AST_identificador
  '''
  identificador_asignable : IDENTIFICADOR opt_identificador_asignable
  '''
  p[0] = AST_identificador(p[1])
  p[0].extender(p[2])

def p_opt_identificador_asignable(p): # None o AST_identificador
  '''
  opt_identificador_asignable : vacio
                              | PUNTO IDENTIFICADOR opt_identificador_asignable
  '''
  if p[1] is None:
    p[0] = None
  else:
    p[0] = AST_identificador(p[2], 'PUNTO')
    p[0].extender(p[3])

def p_identificador_declarable(p): # AST_identificador
  '''
  identificador_declarable : IDENTIFICADOR
                           | ABRE_LLAVE IDENTIFICADOR identificadores CIERRA_LLAVE
  '''
  if len(p) == 2:
    p[0] = AST_identificador(p[1])
  else:
    p[0] = AST_identificador('{' + p[2] + p[3] + '}')

def p_identificadores(p): # String
  '''
  identificadores : vacio
                  | COMA s IDENTIFICADOR identificadores
  '''
  p[0] = ''
  if len(p) > 2:
    p[0] = ',' + str(p[2]) + p[3] + p[4]

def p_argumentos(p): # Lista de AST_expresion
  '''
  argumentos : vacio
             | mas_argumentos
  '''
  if p[1] is None:
    p[0] = []
  else:
    p[0] = p[1]

def p_opt_mas_argumentos(p): # Lista de AST_expresion (puede ser vacía)
  '''
  opt_mas_argumentos : vacio
                     | COMA s mas_argumentos
  '''
  if p[1] is None:
    p[0] = []
  else:
    p[0] = p[3]
    p[0][0].apertura(p[2])

def p_mas_argumentos(p): # Lista de AST_expresion (NO puede ser vacía)
  '''
  mas_argumentos : expresion opt_mas_argumentos
  '''
  p[0] = p[2]
  p[0].insert(0, p[1])

def p_comentario(p):
  '''
  comentario : COMENTARIO_UL s
             | COMENTARIO_ML s
  '''
  p[0] = AST_comentario(p[1], p[2])

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

class AST_nodo(object):
  def __init__(self, cierre=None):
    self.cierre = cierre
    self.abre = None
  def apertura(self, c):
    self.abre = texto_con(self.abre, c)
  def clausura(self, c):
    self.cierre = texto_con(self.cierre, c)
  def restore(self,contenido=''):
    return f"{restore(self.abre)}{contenido}{restore(self.cierre)}"

class AST_espacios(AST_nodo):
  def __init__(self, espacios):
    super().__init__()
    self.espacios = espacios
  def __str__(self):
    return self.espacios
  def restore(self):
    return self.espacios

class AST_decl_variable(AST_nodo):
  def __init__(self, variable, asignacion=None, cierre=None, decl='let', s_var=None, s_init=None, s_val=None):
    super().__init__(cierre)
    self.decl = decl
    self.s_var = s_var
    self.variable = variable
    self.s_init = s_init
    self.s_val = s_val
    self.asignacion = asignacion
  def __str__(self):
    return f"Variable-{self.variable} : {show(self.asignacion)}"
  def restore(self):
    init = ''
    if not (self.asignacion is None):
      init = f"{restore(self.s_init)}={restore(self.s_val)}{restore(self.asignacion)}"
    return f"{self.decl}{restore(self.s_var)}{self.variable}{init}{restore(self.cierre)}"

class AST_decl_funcion(AST_nodo):
  def __init__(self, funcion, cuerpo, s_id=None, s_abreParen=None, s_cierraParen=None, s_abreLlave=None):
    self.s_id = s_id
    self.funcion = funcion
    self.s_abreParen = s_abreParen
    self.s_cierraParen = s_cierraParen
    self.s_abreLlave = s_abreLlave
    self.cuerpo = cuerpo
    super().__init__()
  def __str__(self):
    cuerpo = '\n\t'.join(list(map(str, self.cuerpo)))
    return f"Función-{self.funcion}\n\t{cuerpo}\n"
  def restore(self):
    cuerpo = "{" + ''.join(list(map(restore, self.cuerpo))) + "}"
    return super().restore(f"function{restore(self.s_id)}{self.funcion}{restore(self.s_abreParen)}({restore(self.s_cierraParen)}){restore(self.s_abreLlave)}{cuerpo}")

class AST_funcion(AST_nodo):
  def __init__(self, cuerpo=None, s_abreParen=None, s_cierraParen=None, s_abreLlave=None):
    self.s_abreParen = s_abreParen
    self.s_cierraParen = s_cierraParen
    self.s_abreLlave = s_abreLlave
    self.cuerpo = cuerpo
    super().__init__()
  def __str__(self):
    return "Función"
  def restore(self):
    cuerpo = ''
    if not (cuerpo is None):
      cuerpo = "{" + ''.join(list(map(restore, self.cuerpo))) + "}"
    return super().restore(f"function{restore(self.s_abreParen)}({restore(self.s_cierraParen)}){restore(self.s_abreLlave)}{cuerpo}")

class AST_invocacion(AST_nodo):
  def __init__(self, invocacion, args=[], cierre=None, s_abreParen=None, s_cierraParen=None):
    self.invocacion = invocacion
    self.args = args
    self.s_abreParen = s_abreParen
    self.s_cierraParen = s_cierraParen
    super().__init__(cierre)
  def __str__(self):
    return f"Invocación-{str(self.invocacion)} {show(self.args)}"
  def restore(self):
    return super().restore(f"{restore(self.invocacion)}{restore(self.s_abreParen)}({restore(self.s_cierraParen)}{restore(self.args)})")

class AST_asignacion(AST_nodo):
  def __init__(self, variable, expresion, s_init=None, s_val=None):
    self.variable = variable
    self.s_init = s_init
    self.s_val = s_val
    self.expresion = expresion
    super().__init__()
  def __str__(self):
    return f"Asignación-{show(self.variable)} {show(self.expresion)}"
  def restore(self):
    return super().restore(f"{restore(self.variable)}{restore(self.s_init)}={restore(self.s_val)}{restore(self.expresion)}")

class AST_identificador(AST_nodo):
  def __init__(self, identificador, clase='ATOM'):
    self.clase = clase
    self.identificador = identificador
    self.extension = None
    super().__init__()
  def extender(self, e):
    self.extension = e
  def __str__(self):
    m = self.identificador
    if self.clase == 'PUNTO':
      m = '.' + m
    if not (self.extension is None):
      m += str(self.extension)
    return m
  def restore(self):
    m = self.identificador
    if self.clase == 'PUNTO':
      m = '.' + m
    if not (self.extension is None):
      m += self.extension.restore()
    return super().restore(f"{m}")

class AST_expresion(AST_nodo):
  def __init__(self, expresion, cierre=None):
    self.expresion = expresion
    super().__init__(cierre)
  def __str__(self):
    return f"Expresión-{self.expresion}"
  def restore(self):
    return super().restore(f"{self.expresion}")

class AST_comentario(AST_nodo):
  def __init__(self, contenido, cierre=None):
    self.contenido = contenido
    super().__init__(cierre)
  def __str__(self):
    return f"Comentario-{self.contenido}"
  def restore(self):
    return super().restore(f"{self.contenido}")

def show(x):
  if x is None:
    return ''
  if type(x) == type([]):
    return f"[{' '.join(list(map(show,x)))}]"
  return str(x)

def restore(x):
  if x is None:
    return ''
  if type(x) == type(''):
    return x
  if type(x) == type([]):
    return ','.join(list(map(restore,x)))
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