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

def concatenar(a, b):
  if type(a) != type([]):
    a = [a]
  if type(b) != type([]):
    b = [b]
  resultado = []
  for x in a:
    resultado.append(x)
  for x in b:
    resultado.append(x)
  return resultado

def p_error(p):
  print(f'Error en línea {p.lineno} {p.value!r}')
  exit(1)

# PROGRAMA : [AST_nodo] #############################################################################
''' Un programa puede ser ...
    P -> PU     ... una lista de declaraciones      p(D) U {lambda}    : (AST_declaracion) : [ P ]
    P -> SF PU  ... o empezar con skippeables antes {skip, comentario} : (AST_skippeable) : [ P ]
''' #################################################################################################
def p_programa_que_no_empieza_con_skip(p):
  '''
  programa : programa_util
  '''
  p[0] = p[1]

def p_programa_que_empieza_con_skip(p):
  '''
  programa : sf programa_util
  '''
  p[0] = concatenar(p[1], p[2])

# PROGRAMA_ÚTIL : [AST_nodo] ########################################################################
''' Un programa útil es una lista de declaraciones (no puede empezar con skippeables)
    PU -> lambda                                    {lambda}
    PU -> D PU                                      p(D)
''' #################################################################################################
def p_programa_util_vacio(p):
  '''
  programa_util : vacio
  '''
  p[0] = []

def p_programa_util_no_vacio(p):
  '''
  programa_util : declaracion programa_util
  '''
  p[0] = concatenar(p[1], p[2])

# SKIPPEABLE_FORZADO : [AST_skippeable] #############################################################
''' Un skippeable forzado debe tener al menos un skippeable y puede seguir con más skippeables
    SF -> skip S       {skip}         : AST_espacios
    SF -> comentario S {comentario}   : AST_comentario
''' #################################################################################################
def p_sf_espacios(p):
  '''
  sf : SKIP s
  '''
  p[0] = concatenar(AST_espacios(p[1]), p[2])

def p_sf_comentario(p):
  '''
  sf : COMENTARIO_UL s
     | COMENTARIO_ML s
  '''
  p[0] = concatenar(AST_comentario(p[1]), p[2])

# SKIPPEABLE_OPCIONAL : [AST_skippeable] ############################################################
''' Un skippeable opcional puede ser ...
    S -> lambda   vacío                           {lambda}
    S -> SF       o tener al menos un skippeable  {skip, comentario}
''' #################################################################################################
def p_skippeable_vacio(p):
  '''
  s : vacio
  '''
  p[0] = []

def p_skippeable_no_vacio(p):
  '''
  s : sf
  '''
  p[0] = p[1]

# DECLARACIÓN : AST_declaracion #####################################################################
''' Una declaración debe contener algo válido (no puede empezar con skippeables). Para saber qué es, hay que ver cómo empieza.
    D -> function       D_FUNCTION
    D -> let|var|const  D_VAR
    D -> id             D_ID
    D -> num|string     D_LITERAL
''' #################################################################################################

# DECLARACIÓN : FUNCIÓN (declaración de función o función anónima)
 #################################################################################################
def p_declaracion_function(p): # AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion
  '''
  declaracion : DECL_FUNC s declaracion_function
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])      # [AST_skippeable]
  rec = p[3]                            # AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion
  rec.apertura(s)
  p[0] = rec

def p_declaracion_function_decl(p): # AST_declaracion_funcion
  '''
  declaracion_function : IDENTIFICADOR s definicion_funcion
  '''
  nombre = AST_identificador(p[1])
  s = p[2]              # [AST_skippeable]
  rec = p[3]            # AST_expresion_funcion | AST_invocacion
  # Si la estoy declarando, no debería haber una invocación
  if type(rec) is AST_invocacion:
    print("ERROR p_declaracion_function_decl")
    exit(0)
  nombre.clausura(s)
  p[0] = AST_declaracion_funcion(nombre, rec.parametros, rec.cuerpo)
  p[0].imitarEspacios(rec)

def p_declaracion_function_anon(p): # AST_expresion_funcion | AST_invocacion
  '''
  declaracion_function : definicion_funcion
  '''
  rec = p[1]            # AST_expresion_funcion | AST_invocacion
  p[0] = rec

def p_definicion_funcion(p): # AST_expresion_funcion | AST_invocacion
  '''
  definicion_funcion : parametros s cuerpo opt_modificador_funcion
  '''
  parametros = p[1]           # AST_parametros
  s = p[2]                    # [AST_skippeable]
  cuerpo = p[3]               # AST_cuerpo
  modificador_funcion = p[4]  # AST_argumentos | [AST_skippeable]
  parametros.clausura(s)
  expresion = AST_expresion_funcion(parametros, cuerpo)
  p[0] = aplicarModificadorFuncion(expresion, modificador_funcion)

def p_opt_modificador_funcion_vacio(p): # [AST_skippeable]                      {lambda}
  '''
  opt_modificador_funcion : vacio
  '''
  p[0] = []

def p_opt_modificador_funcion_con_skip(p): # AST_argumentos | [AST_skippeable]  {skip, comentario}
  '''
  opt_modificador_funcion : sf modificador_funcion
  '''
  s = p[1]                          # [AST_skippeable]
  modificador_funcion = p[2]        # AST_argumentos | [AST_skippeable]
  if type(modificador_funcion) == type([]):
    modificador_funcion[0].apertura(s)
  else:
    modificador_funcion.apertura(s)
  p[0] = modificador_funcion

def p_opt_modificador_funcion_sin_skip(p): # AST_argumentos | [AST_skippeable]  {(, ;}
  '''
  opt_modificador_funcion : modificador_funcion
  '''
  modificador_funcion = p[1]    # AST_argumentos | [AST_skippeable]
  p[0] = modificador_funcion

def p_modificador_funcion_modificador_expresion(p): # AST_argumentos
  '''
  modificador_funcion : modificador_expresion
  '''
  modificador_expresion = p[1]  # AST_argumentos
  p[0] = modificador_expresion

def p_modificador_funcion_cierre(p): # [AST_skippeable]
  '''
  modificador_funcion : cierre
  '''
  cierre = p[1]                 # [AST_skippeable]
  p[0] = cierre

def p_parametros(p): # AST_parametros
  '''
  parametros : ABRE_PAREN s identificadores CIERRA_PAREN
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  parametros = p[3]           # [AST_identificador]
  cierra = AST_sintaxis(p[4])
  p[0] = AST_parametros(parametros)
  p[0].apertura(s)
  p[0].clausura(cierra)

def p_cuerpo(p): # AST_cuerpo
  '''
  cuerpo : ABRE_LLAVE programa CIERRA_LLAVE
  '''
  abre = AST_sintaxis(p[1])
  programa = p[2]               # [AST_nodo]
  cierra = AST_sintaxis(p[3])
  if len(programa) == 0:
    programa = [abre]
  else:
    programa[0].apertura(abre)
  programa[-1].clausura(cierra)
  p[0] = programa

def p_identificadores_vacio(p): # [AST_identificador]
  '''
  identificadores : vacio
  '''
  p[0] = []

def p_identificadores_no_vacio(p): # [AST_identificador]
  '''
  identificadores : IDENTIFICADOR s mas_identificadores
  '''
  identificador = AST_identificador(p[1])
  s = p[2]                  # [AST_skippeable]
  rec = p[3]                # [AST_identificador]
  identificador.clausura(s)
  rec.insert(0, identificador)
  p[0] = rec

def p_mas_identificadores_fin(p): # [AST_identificador]
  '''
  mas_identificadores : vacio
  '''
  p[0] = []

def p_mas_identificadores(p): # [AST_identificador]
  '''
  mas_identificadores : COMA s IDENTIFICADOR s mas_identificadores
  '''
  coma = AST_sintaxis(p[1])
  s1 = concatenar(coma, p[2]) # [AST_skippeable]
  identificador = AST_identificador(p[3])
  s2 = p[4]                   # [AST_skippeable]
  rec = p[3]                  # [AST_identificador]
  identificador.apertura(s1)
  identificador.clausura(s2)
  rec.insert(0, identificador)
  p[0] = rec

# DECLARACIÓN : VARIABLE (declaración de variable)
 #################################################################################################
def p_declaracion_var(p): # AST_declaracion_variable
  '''
  declaracion : DECL_VAR sf IDENTIFICADOR opt_modificador_variable
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])  # [AST_skippeable]
  nombre = AST_identificador(p[3])
  modificador_variable = p[4]       # AST_expresion | [AST_skippeable]
  decl_var = AST_declaracion_variable(nombre)
  decl_var.apertura(s)
  p[0] = aplicarModificadorVariable(decl_var, modificador_variable)

def p_opt_modificador_variable_vacio(p): # [AST_skippeable]         {lambda}
  '''
  opt_modificador_variable : vacio
  '''
  p[0] = []

def p_opt_modificador_variable_con_skip(p): # AST_expresion         {skip, comentario}
  '''
  opt_modificador_variable : sf modificador_variable
  '''
  s = p[1]                          # [AST_skippeable]
  modificador_variable = p[2]       # AST_expresion | [AST_skippeable]
  if type(modificador_variable) == type([]):
    modificador_variable[0].apertura(s)
  else:
    modificador_variable.apertura(s)
  p[0] = modificador_variable

def p_opt_modificador_variable_sin_skip(p): # AST_expresion         {=, ;}
  '''
  opt_modificador_variable : modificador_variable
  '''
  modificador_variable = p[1]       # AST_expresion | [AST_skippeable]
  p[0] = modificador_variable

def p_modificador_variable_asignacion(p): # AST_expresion
  '''
  modificador_variable : asignacion
  '''
  asignacion = p[1]       # AST_expresion
  p[0] = asignacion

def p_modificador_variable_cierre(p): # [AST_skippeable]
  '''
  modificador_variable : cierre
  '''
  cierre = p[1]           # [AST_skippeable]
  p[0] = cierre

# DECLARACIÓN : IDENTIFICADOR (asignación o invocación)
 #################################################################################################
def p_declaracion_id(p): # AST_invocacion | AST_asignacion
  '''
  declaracion : IDENTIFICADOR opt_modificador_identificador
  '''
  identificador = AST_identificador(p[1])
  modificador_identificador = p[2]      # AST_argumentos | AST_expresion | [AST_skippeable]
  p[0] = aplicarModificadorIdentificador(identificador, modificador_identificador)

def p_opt_modificador_identificador_vacio(p): # [AST_skippeable]         {lambda}
  '''
  opt_modificador_identificador : vacio
  '''
  p[0] = []

def p_opt_modificador_identificador_con_skip(p): # AST_argumentos | AST_expresion         {skip, comentario}
  '''
  opt_modificador_identificador : sf modificador_identificador
  '''
  s = p[1]                          # [AST_skippeable]
  modificador_identificador = p[2]       # AST_argumentos | AST_expresion | [AST_skippeable]
  if type(modificador_identificador) == type([]):
    modificador_identificador[0].apertura(s)
  else:
    modificador_identificador.apertura(s)
  p[0] = modificador_identificador

def p_opt_modificador_identificador_sin_skip(p): # AST_argumentos | AST_expresion         {=, (, ;}
  '''
  opt_modificador_identificador : modificador_identificador
  '''
  modificador_identificador = p[1]       # AST_argumentos | AST_expresion | [AST_skippeable]
  p[0] = modificador_identificador

def p_modificador_identificador_asignacion(p): # AST_expresion
  '''
  modificador_identificador : asignacion
  '''
  asignacion = p[1]       # AST_expresion
  p[0] = asignacion

def p_modificador_identificador_invocacion(p): # AST_argumentos
  '''
  modificador_identificador : invocacion
  '''
  invocacion = p[1]       # AST_argumentos
  p[0] = invocacion

def p_asignacion(p): # AST_expresion
  '''
  asignacion : ASIGNACION s expresion opt_modificador_asignacion
  '''
  asignacion = AST_sintaxis(p[1])
  s = concatenar(asignacion, p[2])    # [AST_skippeable]
  expresion = p[3]                    # AST_expresion
  modificador_asignacion = p[4]       # [AST_skippeable]
  expresion.apertura(s)
  p[0] = aplicarModificadorAsignacion(expresion, modificador_asignacion)

def p_opt_modificador_asignacion_vacio(p): # [AST_skippeable]             {lambda}
  '''
  opt_modificador_asignacion : vacio
  '''
  p[0] = []

def p_opt_modificador_asignacion_con_skip(p): # [AST_skippeable]          {skip, comentario}
  '''
  opt_modificador_asignacion : sf modificador_asignacion
  '''
  s = p[1]                                      # [AST_skippeable]
  modificador_asignacion = p[2]                 # [AST_skippeable]
  if type(modificador_asignacion) == type([]):
    modificador_asignacion[0].apertura(s)
  else:
    modificador_asignacion.apertura(s)
  p[0] = modificador_asignacion

def p_opt_modificador_asignacion_sin_skip(p): # [AST_skippeable]          {;}
  '''
  opt_modificador_asignacion : modificador_asignacion
  '''
  modificador_asignacion = p[1]                 # [AST_skippeable]
  p[0] = modificador_asignacion

def p_modificador_asignacion_cierre(p): # [AST_skippeable]
  '''
  modificador_asignacion : cierre
  '''
  cierre = p[1]                                 # [AST_skippeable]
  p[0] = cierre

def p_expresion_literal(p): # AST_expresion_literal
  '''
  expresion : NUMERO
            | STRING
  '''
  p[0] = AST_expresion_literal(p[1])

def p_expresion_identificador(p): # AST_expresion_identificador
  '''
  expresion : IDENTIFICADOR
  '''
  identificador = AST_identificador(p[1])
  p[0] = AST_expresion_identificador(identificador)

def p_modificador_expresion_invocacion(p): # AST_argumentos
  '''
  modificador_expresion : invocacion
  '''
  invocacion = p[1] # AST_argumentos
  p[0] = invocacion

def p_invocacion(p): # AST_argumentos
  '''
  invocacion : ABRE_PAREN s argumentos CIERRA_PAREN opt_cierre
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  argumentos = p[3]           # [AST_expresion]
  cierra = AST_sintaxis(p[4])
  opt_cierre = p[5]           # [AST_skippeable]
  p[0] = AST_argumentos(argumentos)
  p[0].apertura(s)
  p[0].clausura(concatenar(cierra, opt_cierre))

def p_argumentos_vacio(p): # [AST_expresion]
  '''
  argumentos : vacio
  '''
  p[0] = []

def p_argumentos_no_vacio(p): # [AST_expresion]
  '''
  argumentos : expresion s mas_argumentos
  '''
  expresion = p[1]          # AST_expresion
  s = p[2]                  # [AST_skippeable]
  rec = p[3]                # [AST_expresion]
  expresion.clausura(s)
  rec.insert(0, expresion)
  p[0] = rec

def p_mas_argumentos_fin(p): # [AST_expresion]
  '''
  mas_argumentos : vacio
  '''
  p[0] = []

def p_mas_argumentos(p): # [AST_expresion]
  '''
  mas_argumentos : COMA s expresion s mas_argumentos
  '''
  coma = AST_sintaxis(p[1])
  s1 = concatenar(coma, p[2]) # [AST_skippeable]
  expresion = p[3]            # AST_expresion
  s2 = p[4]                   # [AST_skippeable]
  rec = p[3]                  # [AST_expresion]
  expresion.apertura(s1)
  expresion.clausura(s2)
  rec.insert(0, expresion)
  p[0] = rec

def p_cierre(p): # [AST_skippeable]
  '''
  cierre : PUNTO_Y_COMA s
  '''
  punto_y_coma = AST_sintaxis(p[1])
  cierre = p[2]                       # [AST_skippeable]
  p[0] = concatenar(punto_y_coma, cierre)

def p_opt_cierre(p): # [AST_skippeable]
  '''
  opt_cierre : cierre
             | vacio
  '''
  p[0] = p[1]

def p_vacio(p): # [AST_skippeable]
  'vacio :'
  p[0] = []

class AST_nodo(object):
  def __init__(self):
    self.cierra = []
    self.abre = []
  def imitarEspacios(self, otro):
    self.abre = otro.abre + self.abre
    self.cierra = self.cierra + otro.cierra
  def apertura(self, c):
    if c is None:
      return
    if type(c) != type([]):
      c = [c]
    for x in reversed(c):
      self.abre.insert(0, x)
  def clausura(self, c):
    if c is None:
      return
    if type(c) != type([]):
      c = [c]
    for x in c:
      self.cierra.append(x)
  def restore(self,contenido=''):
    return f"{''.join(map(restore, self.abre))}{contenido}{''.join(map(restore, self.cierra))}"

class AST_skippeable(AST_nodo):
  def __init__(self):
    super().__init__()

class AST_espacios(AST_skippeable):
  def __init__(self, espacios):
    super().__init__()
    self.espacios = espacios
  def __str__(self):
    return show(self.espacios)
  def restore(self):
    return super().restore(f"{self.espacios}")

class AST_comentario(AST_skippeable):
  def __init__(self, contenido):
    super().__init__()
    self.contenido = contenido
  def __str__(self):
    return f"Comentario: {show(self.contenido)}"
  def restore(self):
    return super().restore(f"{self.contenido}")

class AST_sintaxis(AST_skippeable):
  def __init__(self, contenido):
    super().__init__()
    self.contenido = contenido
  def __str__(self):
    return f"Sintaxis: {show(self.contenido)}"
  def restore(self):
    return super().restore(f"{self.contenido}")

class AST_declaracion(AST_nodo):
  def __init__(self):
    super().__init__()

class AST_declaracion_funcion(AST_declaracion):
  def __init__(self, nombre, parametros, cuerpo):
    super().__init__()
    self.nombre = nombre          # AST_identificador
    self.parametros = parametros  # AST_parametros
    self.cuerpo = cuerpo          # AST_cuerpo
  def __str__(self):
    return f"DeclaraciónFunción : {show(self.nombre)}"
  def restore(self):
    return super().restore(f"{restore(self.nombre)}{restore(self.parametros)}{restore(self.cuerpo)}")

class AST_expresion(AST_declaracion):
  def __init__(self):
    super().__init__()

class AST_expresion_literal(AST_expresion):
  def __init__(self, literal):
    super().__init__()
    self.literal = literal        # String
  def __str__(self):
    return f"{show(self.literal)}"
  def restore(self):
    return super().restore(f"{restore(self.literal)}")

class AST_expresion_identificador(AST_expresion):
  def __init__(self, identificador):
    super().__init__()
    self.identificador = identificador    # AST_identificador
  def __str__(self):
    return f"{show(self.identificador)}"
  def restore(self):
    return super().restore(f"{restore(self.identificador)}")

class AST_expresion_funcion(AST_expresion):
  def __init__(self, parametros, cuerpo):
    super().__init__()
    self.parametros = parametros  # AST_parametros
    self.cuerpo = cuerpo          # AST_cuerpo
  def __str__(self):
    return f"FunciónAnónima"
  def restore(self):
    return super().restore(f"{restore(self.parametros)}{restore(self.cuerpo)}")

class AST_declaracion_variable(AST_declaracion):
  def __init__(self, nombre, asignacion=None):
    super().__init__()
    self.nombre = nombre          # AST_identificador
    self.asignacion = asignacion  # AST_expresion
  def __str__(self):
    return f"DeclaraciónVariable : {show(self.nombre)}"
  def restore(self):
    return super().restore(f"{restore(self.nombre)}{restore(self.asignacion)}")

class AST_invocacion(AST_declaracion):
  def __init__(self, funcion, argumentos):
    super().__init__()
    self.funcion = funcion        # AST_identificador | AST_expresion_funcion
    self.argumentos = argumentos  # AST_argumentos
  def __str__(self):
    return f"Invocacion : {show(self.funcion)}"
  def restore(self):
    return super().restore(f"{restore(self.funcion)}{restore(self.argumentos)}")

class AST_asignacion(AST_declaracion):
  def __init__(self, asignable, valor):
    super().__init__()
    self.asignable = asignable    # AST_asignable
    self.valor = valor            # AST_expresion
  def __str__(self):
    return f"Asignación : {show(self.asignable)} = {show(self.valor)}"
  def restore(self):
    return super().restore(f"{restore(self.asignable)}{restore(self.valor)}")

class AST_parametros(AST_declaracion):
  def __init__(self, parametros):
    super().__init__()
    self.parametros = parametros  # [AST_identificador]
  def __str__(self):
    return f"Parámetros : {show(self.parametros)}"
  def restore(self):
    return super().restore(f"{restore(self.parametros)}")

class AST_argumentos(AST_declaracion):
  def __init__(self, argumentos):
    super().__init__()
    self.argumentos = argumentos  # [AST_expresion]
  def __str__(self):
    return f"Argumentos : {show(self.argumentos)}"
  def restore(self):
    return super().restore(f"{restore(self.argumentos)}")

class AST_asignable(AST_declaracion):
  def __init__(self):
    super().__init__()

class AST_identificador(AST_asignable):
  def __init__(self, identificador):
    super().__init__()
    self.identificador = identificador    # String
  def __str__(self):
    return f"{self.identificador}"
  def restore(self):
    return super().restore(f"{self.identificador}")

def aplicarModificadorVariable(decl_var, mod):
  if type(mod) is AST_expresion:
    decl_var.asignacion = mod
  else: # [AST_skippeable]
    decl_var.clausura(mod)
  return decl_var

def aplicarModificadorFuncion(func, mod):
  if type(mod) is AST_argumentos:
    return AST_invocacion(func, mod)
  else: # [AST_skippeable]
    func.clausura(mod)
    return func

def aplicarModificadorIdentificador(id, mod):
  if type(mod) is AST_argumentos:
    return AST_invocacion(id, mod)
  elif isinstance(mod, AST_expresion):
    return AST_asignacion(id, mod)
  else: # [AST_skippeable]
    id.clausura(mod)
    return id

def aplicarModificadorAsignacion(asignacion, mod):
  if False:
    pass
  else: # [AST_skippeable]
    asignacion.clausura(mod)
    return asignacion

def show(x):
  if x is None:
    return ''
  if type(x) == type([]):
    return f"[{' '.join(list(map(show,x)))}]"
  return str(x).replace('\n','\\n').replace('\t','\\t').replace('\r','\\r')

def restore(x):
  if x is None:
    return ''
  if type(x) == type(''):
    return x
  if type(x) == type([]):
    return ','.join(list(map(restore,x)))
  return x.restore()

parser = yacc()

def parsear(contenido):
  return parser.parse(contenido)