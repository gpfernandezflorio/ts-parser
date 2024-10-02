from my_ply.lex import lex, LexToken
from my_ply.yacc import yacc

tokens = (
  'DECL_FUNC',
  'DECL_VAR',
  'COMBINADOR',
  'ELSE',
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
  'ABRE_CORCHETE',
  'CIERRA_CORCHETE',
  'OPERADOR_PREFIJO',
  'OPERADOR_INFIJO',
  'OPERADOR_BINARIO',
  'MAS',
  'MENOS',
  'POR',
  'DIV',
  'DOS_PUNTOS',
  'PUNTO_Y_COMA',
  'PUNTO',
  'COMA',
  'SKIP'
)

reserved_map = {
  'function':'DECL_FUNC',
  'else':'ELSE'
}

for k in ['let','const','var']:
  reserved_map[k] = 'DECL_VAR'

for k in ['if','for','while']:
  reserved_map[k] = 'COMBINADOR'

for k in ['in','of']:
  reserved_map[k] = 'OPERADOR_BINARIO'

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
t_ASIGNACION = r'=|\+=|\*=|-=|/='
t_ABRE_PAREN = r'\('
t_CIERRA_PAREN = r'\)'
t_ABRE_LLAVE = r'{'
t_CIERRA_LLAVE = r'}'
t_ABRE_CORCHETE = r'\['
t_CIERRA_CORCHETE = r'\]'
t_OPERADOR_PREFIJO = r'!'
t_OPERADOR_INFIJO = r'\+\+|--'
t_OPERADOR_BINARIO = r'==|!=|===|!==|>=|<=|>|<|&&|\|\|'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIV = r'/'
t_DOS_PUNTOS = r':'
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

def token(tipo, valor, linea, col, pos):
  t = LexToken()
  t.type = tipo
  t.value = valor
  t.lineno = linea
  t.colno = col
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
  if p is None:
    print('EoF')
  else:
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
    D -> function       D_FUNCTION    AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion
    D -> let|var|const  D_VAR         AST_declaracion_variable
    D -> id             D_ID          AST_invocacion | AST_asignacion | AST_identificador | AST_expresion_acceso | AST_expresion_index
    D -> num            D_NUMERO      AST_expresion_literal
    D -> string         D_STRING      AST_expresion_literal
    D -> {...}          D_OBJETO      AST_expresion_objeto
    D -> if|for|while   D_COMMAND     AST_combinador
    D -> !|-|++|--      D_PREFIX      AST_operador
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
  declaracion_function : IDENTIFICADOR s definicion_funcion opt_cierre
  '''
  nombre = AST_identificador(p[1])
  s = p[2]              # [AST_skippeable]
  rec = p[3]            # AST_expresion_funcion | AST_invocacion
  cierre = p[4]
  # Si la estoy declarando, no debería haber una invocación
  if type(rec) is AST_invocacion:
    print("ERROR p_declaracion_function_decl")
    exit(0)
  nombre.clausura(s)
  p[0] = AST_declaracion_funcion(nombre, rec.parametros, rec.cuerpo)
  p[0].imitarEspacios(rec)
  p[0].clausura(cierre)

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
  parametros = p[1]       # AST_parametros
  s = p[2]                # [AST_skippeable]
  cuerpo = p[3]           # AST_cuerpo
  modificador = p[4]      # AST_argumentos | [AST_skippeable]
  parametros.clausura(s)
  expresion = AST_expresion_funcion(parametros, cuerpo)
  p[0] = aplicarModificador(expresion, modificador)

def p_opt_modificador_funcion_con_skip(p): # AST_argumentos | [AST_skippeable]  {skip, comentario}
  '''
  opt_modificador_funcion : sf modificador_funcion
  '''
  s = p[1]                  # [AST_skippeable]
  modificador = p[2]        # AST_argumentos | [AST_skippeable]
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_funcion_sin_skip(p): # AST_argumentos | [AST_skippeable]  {(, ;}
  '''
  opt_modificador_funcion : modificador_funcion
  '''
  modificador_funcion = p[1]    # AST_argumentos | [AST_skippeable]
  p[0] = modificador_funcion

def p_modificador_funcion_vacio(p): # [AST_skippeable]                      {lambda}
  '''
  modificador_funcion : vacio
  '''
  p[0] = []

def p_modificador_funcion_no_vacio(p): # [AST_skippeable]                      {lambda}
  '''
  modificador_funcion : modificador_funcion_no_vacio
  '''
  p[0] = p[1]

def p_modificador_funcion_modificador_expresion(p): # AST_argumentos
  '''
  modificador_funcion_no_vacio : modificador_expresion_no_vacio
  '''
  modificador_expresion = p[1]  # AST_argumentos
  p[0] = modificador_expresion

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
  contenido = p[2]               # [AST_nodo]
  cierra = AST_sintaxis(p[3])
  programa = AST_cuerpo(contenido)
  programa.apertura(abre)
  programa.clausura(cierra)
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
  rec = p[5]                  # [AST_identificador]
  identificador.apertura(s1)
  identificador.clausura(s2)
  rec.insert(0, identificador)
  p[0] = rec

# DECLARACIÓN : VARIABLE (declaración de variable)
 #################################################################################################
def p_declaracion_var(p): # AST_declaracion_variable
  '''
  declaracion : DECL_VAR sf identificador opt_modificador_variable
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])        # [AST_skippeable]
  identificador = p[3]                    # AST_identificador | AST_identificadores
  modificador_variable = p[4]             # AST_expresion | [AST_skippeable]
  decl_var = AST_declaracion_variable(identificador)
  decl_var.apertura(s)
  p[0] = aplicarModificador(decl_var, modificador_variable)

def p_identificador_uno(p): # AST_identificador
  '''
  identificador : IDENTIFICADOR
  '''
  p[0] = AST_identificador(p[1])

def p_identificador_varios(p): # AST_identificadores
  '''
  identificador : ABRE_LLAVE s identificadores CIERRA_LLAVE
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  identificadores = p[3]      # [AST_identificador]
  cierra = AST_sintaxis(p[4])
  p[0] = AST_identificadores(identificadores)
  p[0].apertura(s)
  p[0].clausura(cierra)

def p_opt_modificador_variable_con_skip(p): # AST_expresion         {skip, comentario}
  '''
  opt_modificador_variable : sf modificador_variable
  '''
  s = p[1]                  # [AST_skippeable]
  modificador = p[2]        # AST_expresion | [AST_skippeable]
  p[0] = p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_variable_sin_skip(p): # AST_expresion         {=, ;}
  '''
  opt_modificador_variable : modificador_variable
  '''
  modificador_variable = p[1]       # AST_expresion | [AST_skippeable]
  p[0] = modificador_variable

def p_modificador_variable_vacio(p): # [AST_skippeable]         {lambda}
  '''
  modificador_variable : vacio
  '''
  p[0] = []

def p_modificador_variable_no_vacio(p): # [AST_skippeable]         {lambda}
  '''
  modificador_variable : modificador_variable_no_vacio
  '''
  p[0] = p[1]

def p_modificador_variable_asignacion(p): # AST_expresion
  '''
  modificador_variable_no_vacio : asignacion
  '''
  asignacion = p[1]       # AST_expresion
  p[0] = asignacion

def p_modificador_variable_cierre(p): # [AST_skippeable]
  '''
  modificador_variable : cierre
  '''
  cierre = p[1]           # [AST_skippeable]
  p[0] = cierre

# DECLARACIÓN : IDENTIFICADOR (asignación, invocación, acceso o indexación)
 #################################################################################################
def p_declaracion_id(p): # AST_invocacion | AST_asignacion | AST_identificador | AST_expresion_acceso | AST_expresion_index
  '''
  declaracion : IDENTIFICADOR opt_modificador_asignable
  '''
  identificador = AST_identificador(p[1])
  modificador = p[2]                # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(identificador, modificador)

def p_opt_modificador_asignable_con_skip(p): # AST_argumentos | AST_expresion | AST_modificador_objeto {skip, comentario}
  '''
  opt_modificador_asignable : sf modificador_asignable
  '''
  s = p[1]                        # [AST_skippeable]
  modificador = p[2]              # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_asignable_sin_skip(p): # AST_argumentos | AST_expresion | AST_modificador_objeto {=, (, ., [}
  '''
  opt_modificador_asignable : modificador_asignable
  '''
  modificador_asignable = p[1]       # AST_argumentos | AST_expresion
  p[0] = modificador_asignable

def p_modificador_asignable_vacio(p): # [AST_skippeable]         {lambda}
  '''
  modificador_asignable : vacio
  '''
  p[0] = []

def p_modificador_asignable_no_vacio(p): # [AST_skippeable]         {lambda}
  '''
  modificador_asignable : modificador_asignable_no_vacio
  '''
  p[0] = p[1]

def p_modificador_asignable_asignacion(p): # AST_expresion
  '''
  modificador_asignable_no_vacio : asignacion
  '''
  asignacion = p[1]       # AST_expresion
  p[0] = asignacion

def p_modificador_asignable_modificador_objeto(p): # AST_modificador_objeto | AST_argumentos
  '''
  modificador_asignable_no_vacio : modificador_objeto_comando_no_vacio
  '''
  modificador_objeto = p[1]       # AST_modificador_objeto | AST_argumentos
  p[0] = modificador_objeto

def p_modificador_asignable_operador(p): # AST_modificador_operador
  '''
  modificador_asignable_no_vacio : operador opt_cierre
  '''
  modificador = p[1]               # [AST_skippeable]
  cierre = p[2]
  modificador.modificador_adicional(cierre)
  p[0] = modificador

def p_modificador_asignable_cierre(p): # [AST_skippeable]
  '''
  modificador_asignable : cierre
  '''
  cierre = p[1]                    # [AST_skippeable]
  p[0] = cierre

def p_modificador_objeto_acceso(p): # AST_modificador_objeto_acceso
  '''
  modificador_objeto_expresion_no_vacio : PUNTO s IDENTIFICADOR opt_modificador_expresion
  '''
  punto = AST_sintaxis(p[1])
  s = concatenar(punto, p[2])       # [AST_skippeable]
  campo = AST_identificador(p[3])   # AST_identificador
  opt_adicional = p[4]              # [AST_skippeable] | AST_modificador_objeto
  p[0] = AST_modificador_objeto_acceso(campo)
  p[0].apertura(s)
  if type(opt_adicional) == type([]):
    p[0].clausura(opt_adicional)
  else:
    p[0].modificador_adicional(opt_adicional)

def p_modificador_objeto_index(p): # AST_modificador_objeto_index
  '''
  modificador_objeto_expresion_no_vacio : ABRE_CORCHETE s expresion CIERRA_CORCHETE opt_modificador_expresion
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  indice = p[3]               # AST_expresion
  cierra = AST_sintaxis(p[4])
  opt_adicional = p[5]        # [AST_skippeable] | AST_modificador_objeto
  p[0] = AST_modificador_objeto_index(indice)
  p[0].apertura(s)
  p[0].clausura(cierra)
  if type(opt_adicional) == type([]):
    p[0].clausura(opt_adicional)
  else:
    p[0].modificador_adicional(opt_adicional)

def p_asignacion(p): # AST_expresion
  '''
  asignacion : ASIGNACION s expresion_asignada
  '''
  asignacion = AST_sintaxis(p[1])
  s = concatenar(asignacion, p[2])    # [AST_skippeable]
  expresion = p[3]                    # AST_expresion
  expresion.apertura(s)
  p[0] = expresion

def p_expresion_asignada_literal(p): # AST_expresion_literal | # AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_asignada : NUMERO opt_modificador_expresion_asignada
                     | STRING opt_modificador_expresion_asignada
  '''
  literal = AST_expresion_literal(p[1]) # AST_expresion_literal
  modificador_expresion = p[2]          # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(literal, modificador_expresion)

def p_expresion_asignada_identificador(p): # AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_asignada : IDENTIFICADOR opt_modificador_expresion_asignada
  '''
  identificador = AST_identificador(p[1])
  modificador_expresion = p[2]      # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  expresion_base = AST_expresion_identificador(identificador)
  p[0] = aplicarModificador(expresion_base, modificador_expresion)

def p_expresion_asignada_funcion(p): # AST_expresion_funcion | AST_expresion_invocacion
  '''
  expresion_asignada : DECL_FUNC s definicion_funcion opt_cierre
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])      # [AST_skippeable]
  rec = p[3]                            # AST_expresion_funcion | AST_expresion_invocacion
  cierre = p[4]
  rec.apertura(s)
  rec.clausura(cierre)
  p[0] = rec

def p_expresion_asignada_objeto(p): # AST_expresion_objeto
  '''
  expresion_asignada : objeto opt_cierre
  '''
  objeto = p[1]
  cierre = p[2]
  objeto.clausura(cierre)
  p[0] = objeto

def p_opt_modificador_expresion_asignada_con_skip(p): # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]  {skip, comentario}
  '''
  opt_modificador_expresion_asignada : sf modificador_expresion_asignada
  '''
  s = p[1]                  # [AST_skippeable]
  modificador = p[2]        # AST_argumentos | AST_modificador_objeto | [AST_skippeable]
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_expresion_asignada_sin_skip(p): # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]  {(, =, ., [}
  '''
  opt_modificador_expresion_asignada : modificador_expresion_asignada
  '''
  modificador_expresion = p[1]    # AST_argumentos | AST_modificador_objeto | [AST_skippeable]
  p[0] = modificador_expresion

def p_modificador_expresion_asignada_vacio(p): # [AST_skippeable]                      {lambda}
  '''
  modificador_expresion_asignada : vacio
  '''
  p[0] = []

def p_modificador_expresion_asignada_no_vacio(p): # [AST_skippeable]                      {lambda}
  '''
  modificador_expresion_asignada : modificador_expresion_asignada_no_vacio
  '''
  p[0] = p[1]

def p_modificador_expresion_asignada_acceso(p): # AST_modificador_objeto | AST_argumentos
  '''
  modificador_expresion_asignada_no_vacio : modificador_objeto_comando_no_vacio
  '''
  modificador_objeto = p[1] # AST_modificador_objeto
  p[0] = modificador_objeto

def p_modificador_objeto_comando_acceso(p): # AST_modificador_objeto_acceso
  '''
  modificador_objeto_comando_no_vacio : PUNTO s IDENTIFICADOR opt_modificador_asignable
  '''
  punto = AST_sintaxis(p[1])
  s = concatenar(punto, p[2])       # [AST_skippeable]
  campo = AST_identificador(p[3])   # AST_identificador
  opt_adicional = p[4]              # [AST_skippeable] | AST_modificador_objeto
  p[0] = AST_modificador_objeto_acceso(campo)
  p[0].apertura(s)
  if type(opt_adicional) == type([]):
    p[0].clausura(opt_adicional)
  else:
    p[0].modificador_adicional(opt_adicional)

def p_modificador_objeto_comando_index(p): # AST_modificador_objeto_index
  '''
  modificador_objeto_comando_no_vacio : ABRE_CORCHETE s expresion CIERRA_CORCHETE opt_modificador_asignable
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  indice = p[3]               # AST_expresion
  cierra = AST_sintaxis(p[4])
  opt_adicional = p[5]        # [AST_skippeable] | AST_modificador_objeto
  p[0] = AST_modificador_objeto_index(indice)
  p[0].apertura(s)
  p[0].clausura(cierra)
  if type(opt_adicional) == type([]):
    p[0].clausura(opt_adicional)
  else:
    p[0].modificador_adicional(opt_adicional)

def p_modificador_objeto_comando_invocacion(p): # AST_argumentos
  '''
  modificador_objeto_comando_no_vacio : invocacion opt_cierre
  '''
  invocacion = p[1]     # AST_argumentos
  opt_cierre = p[2]     # [AST_skippeable]
  p[0] = invocacion
  p[0].modificador_adicional(opt_cierre)

def p_modificador_expresion_asignada_cierre(p): # [AST_skippeable]
  '''
  modificador_expresion_asignada : cierre
  '''
  cierre = p[1]                                 # [AST_skippeable]
  p[0] = cierre

## -- EXPRESIONES --

def p_expresion_sin_pre(p): # AST_expresion
  '''
  expresion : expresion_sin_pre
  '''
  expresion = p[1]
  p[0] = expresion

def p_expresion_con_pre(p): # AST_expresion
  '''
  expresion : operador_prefijo s expresion
  '''
  operador = p[1]                 # string
  s = concatenar(operador, p[2])  # [AST_skippeable]
  expresion = p[3]                # AST_expresion
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    expresion.izq = AST_operador(None, operador, expresion.izq)
  else:
    expresion = AST_operador(None, operador, expresion)
  expresion.apertura(s)
  p[0] = expresion

def p_expresion_literal(p): # AST_expresion_literal | AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_sin_pre : NUMERO opt_modificador_expresion
                    | STRING opt_modificador_expresion
  '''
  literal = AST_expresion_literal(p[1]) # AST_expresion_literal
  modificador_expresion = p[2]          # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(literal, modificador_expresion)

def p_expresion_identificador(p): # AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_sin_pre : IDENTIFICADOR opt_modificador_expresion
  '''
  identificador = AST_identificador(p[1])
  modificador_expresion = p[2]      # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  expresion_base = AST_expresion_identificador(identificador)
  p[0] = aplicarModificador(expresion_base, modificador_expresion)

def p_expresion_function(p): # AST_expresion_funcion | AST_invocacion
  '''
  expresion_sin_pre : DECL_FUNC s definicion_funcion
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])      # [AST_skippeable]
  rec = p[3]                            # AST_expresion_funcion | AST_invocacion
  rec.apertura(s)
  p[0] = rec

def p_expresion_objeto(p): # AST_expresion_objeto
  '''
  expresion_sin_pre : objeto
  '''
  objeto = p[1]
  p[0] = objeto

def p_expresion_parentesis(p): # AST_expresion
  '''
  expresion_sin_pre : ABRE_PAREN s expresion CIERRA_PAREN opt_modificador_expresion
  '''
  s = AST_sintaxis(p[1])
  s = concatenar(s, p[2])
  expresion = p[3]
  expresion.conParentesis()
  expresion.clausura(p[4])
  modificador_expresion = p[5]      # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  expresion.apertura(s)
  p[0] = aplicarModificador(expresion, modificador_expresion)

def p_opt_modificador_expresion_con_skip(p): # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]  {skip, comentario}
  '''
  opt_modificador_expresion : sf modificador_expresion
  '''
  s = p[1]                  # [AST_skippeable]
  modificador = p[2]        # AST_argumentos | AST_modificador_objeto | [AST_skippeable]
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_expresion_sin_skip(p): # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]  {(, =, ., [}
  '''
  opt_modificador_expresion : modificador_expresion
  '''
  modificador_expresion = p[1]    # AST_argumentos | AST_modificador_objeto | [AST_skippeable]
  p[0] = modificador_expresion

def p_modificador_expresion_vacio(p): # [AST_skippeable]                      {lambda}
  '''
  modificador_expresion : vacio
  '''
  p[0] = []

def p_modificador_expresion_no_vacio(p): # [AST_skippeable]                      {lambda}
  '''
  modificador_expresion : modificador_expresion_no_vacio
  '''
  p[0] = p[1]

def p_modificador_expresion_acceso(p): # AST_modificador_objeto
  '''
  modificador_expresion_no_vacio : modificador_objeto_expresion_no_vacio
  '''
  modificador_objeto = p[1] # AST_modificador_objeto
  p[0] = modificador_objeto

def p_modificador_expresion_invocacion(p): # AST_argumentos
  '''
  modificador_expresion_no_vacio : invocacion
  '''
  invocacion = p[1] # AST_argumentos
  p[0] = invocacion

def p_modificador_expresion_operador_binario(p): # AST_modificador_operador
  '''
  modificador_expresion_no_vacio : operador
  '''
  modificador = p[1]
  p[0] = modificador

def p_operador_operador_binario(p): # AST_modificador_operador_binario
  '''
  operador : operador_binario s expresion
  '''
  clase = p[1]
  s = concatenar(clase, p[2])
  expresion = p[3]
  expresion.apertura(s)
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    modificador = AST_modificador_operador_binario(clase, expresion.izq)
    modificador.modificador_adicional(AST_modificador_operador_binario(expresion.op, expresion.der))
  else:
    modificador = AST_modificador_operador_binario(clase, expresion)
  p[0] = modificador

# TODO: Agregar el MENOS además del OPERADOR_BINARIO, MAS, etc.
def p_operador_binario(p): # string
  '''
  operador_binario : OPERADOR_BINARIO
                   | MAS
                   | POR
                   | DIV
  '''
  operador = p[1]
  p[0] = operador

def p_operador_operador_posfijo(p): # AST_modificador_operador_posfijo
  '''
  operador : operador_posfijo opt_modificador_expresion
  '''
  operador = p[1]
  opt_adicional = p[2]
  modificador = AST_modificador_operador_posfijo(operador)
  modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_operador_posfijo(p): # string
  '''
  operador_posfijo : OPERADOR_INFIJO
  '''
  operador = p[1]
  p[0] = operador

def p_invocacion(p): # AST_argumentos
  '''
  invocacion : ABRE_PAREN s argumentos
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  argumentos = p[3]           # AST_argumentos
  argumentos.apertura(s)
  argumentos.clausura(')')
  p[0] = argumentos

def p_argumentos_vacio(p): # AST_argumentos
  '''
  argumentos : fin_argumentos
  '''
  fin_argumentos = p[1]
  p[0] = fin_argumentos

def p_argumentos_no_vacio(p): # AST_argumentos
  '''
  argumentos : expresion mas_argumentos
  '''
  expresion = p[1]          # AST_expresion
  argumentos = p[2]         # AST_argumentos
  argumentos.agregar_argumento(expresion)
  p[0] = argumentos

def p_mas_argumentos_fin(p): # AST_argumentos
  '''
  mas_argumentos : fin_argumentos
  '''
  fin_argumentos = p[1]
  p[0] = fin_argumentos

def p_mas_argumentos(p): # AST_argumentos
  '''
  mas_argumentos : COMA s expresion mas_argumentos
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  expresion = p[3]            # AST_expresion
  argumentos = p[4]               # AST_argumentos
  expresion.apertura(s)
  argumentos.agregar_argumento(expresion)
  p[0] = argumentos

def p_fin_argumentos(p): # AST_argumentos
  '''
  fin_argumentos : CIERRA_PAREN opt_modificador_invocacion
  '''
  opt_adicional = p[2]
  p[0] = AST_argumentos()
  p[0].modificador_adicional(opt_adicional)

def p_opt_modificador_invocacion_con_skip(p): # [AST_skippeable] | AST_argumentos | AST_modificador_objeto
  '''
  opt_modificador_invocacion : sf modificador_invocacion
  '''
  s = p[1]                    # [AST_skippeable]
  modificador = p[2]          # AST_argumentos | AST_modificador_objeto | [AST_skippeable]
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_invocacion_sin_skip(p): # AST_argumentos | AST_modificador_objeto
  '''
  opt_modificador_invocacion : modificador_invocacion
  '''
  modificador = p[1]
  p[0] = modificador

def p_modificador_invocacion_vacio(p): # [AST_skippeable]
  '''
  modificador_invocacion : vacio
  '''
  p[0] = []

def p_modificador_invocacion_no_vacio(p): # [AST_skippeable]
  '''
  modificador_invocacion : modificador_invocacion_no_vacio
  '''
  p[0] = p[1]

def p_modificador_invocacion_invocacion(p): # AST_argumentos
  '''
  modificador_invocacion_no_vacio : invocacion
  '''
  invocacion = p[1]
  p[0] = invocacion

def p_modificador_invocacion_objeto(p): # AST_modificador_objeto
  '''
  modificador_invocacion_no_vacio : modificador_objeto_expresion_no_vacio
  '''
  modificador_objeto = p[1]
  p[0] = modificador_objeto

# DECLARACIÓN : NUMERO
 #################################################################################################
def p_declaracion_literal(p): # AST_expresion_literal
  '''
  declaracion : NUMERO opt_modificador_literal_suelto
  '''
  literal = AST_expresion_literal(p[1])   # AST_expresion_literal
  modificador = p[2]                      # [AST_skippeable]
  p[0] = aplicarModificador(literal, modificador)

def p_opt_modificador_literal_suelto_con_skip(p): # [AST_skippeable]
  '''
  opt_modificador_literal_suelto : sf modificador_literal_suelto
  '''
  s = p[1]                                # [AST_skippeable]
  modificador = p[2]                      # [AST_skippeable]
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_literal_suelto_sin_skip(p): # [AST_skippeable]
  '''
  opt_modificador_literal_suelto : modificador_literal_suelto
  '''
  modificador_literal_suelto = p[1]       # [AST_skippeable]
  p[0] = modificador_literal_suelto

def p_modificador_literal_suelto_vacio(p): # [AST_skippeable]
  '''
  modificador_literal_suelto : vacio
  '''
  p[0] = []

def p_modificador_literal_suelto_no_vacio(p): # [AST_skippeable]
  '''
  modificador_literal_suelto : modificador_literal_suelto_no_vacio
  '''
  modificador = p[1]
  p[0] = modificador

def p_modificador_literal_suelto_operador(p): # [AST_skippeable]
  '''
  modificador_literal_suelto_no_vacio : operador opt_cierre
  '''
  modificador = p[1]                                 # [AST_skippeable]
  cierre = p[2]
  modificador.modificador_adicional(cierre)
  p[0] = modificador

def p_modificador_literal_suelto_cierre(p): # [AST_skippeable]
  '''
  modificador_literal_suelto : cierre
  '''
  cierre = p[1]                                 # [AST_skippeable]
  p[0] = cierre

# DECLARACIÓN : STRING
 #################################################################################################
def p_declaracion_string(p): # AST_expresion_literal
  '''
  declaracion : STRING opt_modificador_objeto_comando
  '''
  literal = AST_expresion_literal(p[1])   # AST_expresion_literal
  modificador = p[2]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  p[0] = aplicarModificador(literal, modificador)

# DECLARACIÓN : OBJETO (no es asignable pero se vuelve asignable al accederlo o indexarlo)
 #################################################################################################
def p_declaracion_objeto(p): # AST_expresion_objeto
  '''
  declaracion : ABRE_LLAVE s campos opt_modificador_objeto_comando
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])              # [AST_skippeable]
  campos = p[3]                           # AST_campos
  modificador = p[4]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  objeto = AST_expresion_objeto(campos)
  objeto.apertura(s)
  objeto.clausura('}')
  p[0] = aplicarModificador(objeto, modificador)

def p_objeto_literal(p): # AST_expresion_objeto
  '''
  objeto : ABRE_LLAVE s campos opt_modificador_objeto_expresion
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])              # [AST_skippeable]
  campos = p[3]                           # AST_campos
  modificador = p[4]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  objeto = AST_expresion_objeto(campos)
  objeto.apertura(s)
  objeto.clausura('}')
  p[0] = aplicarModificador(objeto, modificador)

def p_opt_modificador_objeto_expresion_con_skip(p):
  '''
  opt_modificador_objeto_expresion : sf modificador_objeto_expresion
  '''
  s = p[1]                                # [AST_skippeable]
  modificador = p[2]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_objeto_expresion_sin_skip(p): # [AST_skippeable] | AST_argumentos | AST_modificador_objeto
  '''
  opt_modificador_objeto_expresion : modificador_objeto_expresion
  '''
  modificador = p[1]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  p[0] = modificador

def p_modificador_objeto_expresion_vacio(p): # [AST_skippeable]
  '''
  modificador_objeto_expresion : vacio
  '''
  p[0] = []

def p_modificador_objeto_expresion_no_vacio(p): # [AST_skippeable] | AST_argumentos | AST_modificador_objeto
  '''
  modificador_objeto_expresion : modificador_objeto_expresion_no_vacio
  '''
  modificador = p[1]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  p[0] = modificador

def p_opt_modificador_objeto_comando_con_skip(p): # [AST_skippeable] | AST_argumentos | AST_modificador_objeto
  '''
  opt_modificador_objeto_comando : sf modificador_objeto_comando
  '''
  s = p[1]                                # [AST_skippeable]
  modificador = p[2]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_objeto_comando_sin_skip(p): # [AST_skippeable] | AST_argumentos | AST_modificador_objeto
  '''
  opt_modificador_objeto_comando : modificador_objeto_comando
  '''
  modificador = p[1]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  p[0] = modificador

def p_modificador_objeto_comando_vacio(p): # [AST_skippeable]
  '''
  modificador_objeto_comando : vacio
  '''
  p[0] = []

def p_modificador_objeto_comando_no_vacio(p): # [AST_skippeable] | AST_argumentos | AST_modificador_objeto
  '''
  modificador_objeto_comando : modificador_objeto_comando_no_vacio
  '''
  modificador = p[1]                      # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  p[0] = modificador

def p_modificador_objeto_comando_cierre(p): # [AST_skippeable]
  '''
  modificador_objeto_comando : cierre
  '''
  cierre = p[1]                                 # [AST_skippeable]
  p[0] = cierre

def p_campos_vacio(p): # AST_campos
  '''
  campos : fin_campos
  '''
  fin_campos = p[1]
  p[0] = fin_campos

def p_campos_no_vacio(p): # AST_campos
  '''
  campos : campo mas_campos
  '''
  campo = p[1]          # AST_campo
  campos = p[2]         # AST_campos
  campos.agregar_campo(campo)
  p[0] = campos

def p_mas_campos_fin(p): # AST_campos
  '''
  mas_campos : fin_campos
  '''
  fin_campos = p[1]
  p[0] = fin_campos

def p_mas_campos(p): # AST_campos
  '''
  mas_campos : COMA s campos
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  campos = p[3]               # AST_campos
  campos.apertura(s)
  p[0] = campos

def p_fin_campos(p): # AST_campos
  '''
  fin_campos : CIERRA_LLAVE
  '''
  p[0] = AST_campos()

def p_campo(p): # AST_campo
  '''
  campo : IDENTIFICADOR s DOS_PUNTOS s expresion
  '''
  clave = p[1]
  s = p[2]
  dp = AST_sintaxis(p[3])
  s = concatenar(s, dp)
  s = concatenar(s, p[4])
  valor = p[5]
  valor.apertura(s)
  p[0] = AST_campo(clave, valor)

# DECLARACIÓN : COMBINADOR (if, for, while)
 #################################################################################################
def p_declaracion_combinador(p): # AST_combinador
  '''
  declaracion : combinador
  '''
  combinador = p[1] # AST_combinador
  p[0] = combinador

def p_combinador(p): # AST_combinador
  '''
  combinador : selector_combinador_no_vacio cuerpo s opt_cierre
  '''
  combinador = p[1] # AST_combinador
  cuerpo = p[2]     # AST_cuerpo
  cierre = concatenar(p[3], p[4])
  combinador.agregar_cuerpo(cuerpo)
  p[0] = combinador
  p[0].clausura(cierre)

def p_selector_combinador_simple(p): # AST_combinador
  '''
  selector_combinador_no_vacio : COMBINADOR s ABRE_PAREN programa CIERRA_PAREN s
  '''
  clase = p[1]                  # string
  s1 = concatenar(clase, p[2])
  s1 = concatenar(s1, p[3])
  expresion = p[4]              # [AST_nodo]
  s2 = AST_sintaxis(p[5])
  s2 = concatenar(s2, p[6])
  if len(expresion) > 0:
    expresion[0].apertura(s1)
    expresion[-1].clausura(s2)
  else:
    expresion = [concatenar(s1,s2)]
  p[0] = AST_combinador(clase, expresion)

def p_selector_combinador_else(p): # AST_combinador
  '''
  selector_combinador_no_vacio : ELSE opt_if
  '''
  clase = p[1]                  # string
  combinador = p[2]             # AST_combinador | [AST_skippeable]
  if (isinstance(combinador, AST_combinador)):
    combinador.apertura(clase)
  else:
    combinador = AST_combinador(clase)
    combinador.clausura(p[2])
  p[0] = combinador

def p_opt_if_con_skip(p): # AST_combinador | [AST_skippeable]
  '''
  opt_if : sf selector_combinador
  '''
  s = p[1]            # [AST_skippeable]
  selector = p[2]     # AST_combinador | [AST_skippeable]
  if (isinstance(selector, AST_combinador)):
    selector.apertura(s)
  else:
    selector = concatenar(s, selector)
  p[0] = selector

def p_opt_if_sin_skip(p): # AST_combinador | [AST_skippeable]
  '''
  opt_if : selector_combinador
  '''
  selector = p[1]     # AST_combinador | [AST_skippeable]
  p[0] = selector

def p_selector_combinador_vacio(p): # [AST_skippeable]
  '''
  selector_combinador : vacio
  '''
  p[0] = []

def p_selector_combinador_no_vacio(p): # AST_combinador
  '''
  selector_combinador : selector_combinador_no_vacio
  '''
  selector = p[1]
  p[0] = selector

# DECLARACIÓN : OPERADOR PREFIJO (!, -, ++, --)
 #################################################################################################
def p_declaracion_prefijo(p): # AST_operador
  '''
  declaracion : operador_prefijo s expresion_como_comando
  '''
  operador = p[1]                 # string
  s = concatenar(operador, p[2])  # [AST_skippeable]
  expresion = p[3]                # AST_expresion
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    expresion.izq = AST_operador(None, operador, expresion.izq)
  else:
    expresion = AST_operador(None, operador, expresion)
  expresion.apertura(s)
  p[0] = expresion

# TODO: Agregar el OPERADOR_INFIJO además del OPERADOR_PREFIJO y el MENOS
def p_operador_prefijo(p): # string
  '''
  operador_prefijo : OPERADOR_PREFIJO
                   | MENOS
  '''
  operador = p[1]
  p[0] = operador

def p_expresion_como_comando(p): # AST_expresion
  '''
  expresion_como_comando : expresion opt_cierre
  '''
  expresion = p[1]
  cierre = p[2]
  expresion.clausura(cierre)
  p[0] = expresion

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

class AST_modificador(AST_nodo):
  def __init__(self):
    super().__init__()
    self.adicional = []
  def modificador_adicional(self, otro):
    self.adicional.append(otro)

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

class AST_cuerpo(AST_declaracion):
  def __init__(self, contenido):
    super().__init__()
    self.contenido = contenido    # [AST_nodo]
  def __str__(self):
    return show(self.contenido)
  def restore(self):
    return super().restore(''.join(map(restore, self.contenido)))

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

class AST_expresion_objeto(AST_expresion):
  def __init__(self, campos):
    super().__init__()
    self.campos = campos        # AST_campos
  def __str__(self):
    return f"Objeto : {show(self.campos)}"
  def restore(self):
    return super().restore(f"{restore(self.campos)}")

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
    args = '' if cantidad(self.argumentos) == 0 else f" con {show(self.argumentos)}"
    return f"Invocacion : {show(self.funcion)}{args}"
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

class AST_expresion_acceso(AST_expresion):
  def __init__(self, objeto, modificador_campo):
    super().__init__()
    self.objeto = objeto                  # AST_expresion
    self.campo = modificador_campo.campo  # AST_identificador
    self.campo.imitarEspacios(modificador_campo)
  def __str__(self):
    return f"Acceso : {show(self.objeto)}.{show(self.campo)}"
  def restore(self):
    return super().restore(f"{restore(self.objeto)}{restore(self.campo)}")

class AST_expresion_index(AST_expresion):
  def __init__(self, objeto, modificador_indice):
    super().__init__()
    self.objeto = objeto                      # AST_expresion
    self.indice = modificador_indice.indice   # AST_expresion
    self.indice.imitarEspacios(modificador_indice)
  def __str__(self):
    return f"Acceso : {show(self.objeto)}[{show(self.indice)}]"
  def restore(self):
    return super().restore(f"{restore(self.objeto)}{restore(self.indice)}")

class AST_combinador(AST_declaracion):
  def __init__(self, clase, expresion=[]):
    super().__init__()
    self.clase = clase          # string
    self.expresion = expresion  # [AST_nodo] [[ OJO: no es una expresión porque podría ser algo como "let i=0; i++;" ]]
    self.cuerpo = []            # [AST_nodo]
  def agregar_cuerpo(self, cuerpo):
    self.cuerpo = cuerpo        # AST_cuerpo
  def __str__(self):
    return f"{self.clase} : {show(self.expresion)} {show(self.cuerpo)}"
  def restore(self):
    return super().restore(f"{restore(self.expresion)}{restore(self.cuerpo)}")

class AST_operador(AST_expresion):
  def __init__(self, izq, op, der):
    super().__init__()
    self.izq = izq    # AST_expresion | None
    self.op = op      # string
    self.der = der    # AST_expresion | None
    self.parentesis = False
  def esBinario(self):
    return not (self.izq is None) and not (self.der is None)
  def tieneParentesis(self):
    return self.parentesis
  def conParentesis(self):
    self.parentesis = True
  def apertura(self, c):
    if self.izq is None:
      self.der.apertura(c)
    else:
      self.izq.apertura(c)
  def clausura(self, c):
    if self.der is None:
      self.izq.clausura(c)
    else:
      self.der.clausura(c)
  def __str__(self):
    resultado = ""
    if not (self.izq is None):
      resultado += f" {show(self.izq)}"
    resultado += self.op;
    if not (self.der is None):
      resultado += f" {show(self.der)}"
    return f"{resultado}"
  def restore(self):
    return super().restore(f"{restore(self.izq)}{restore(self.der)}")

class AST_parametros(AST_declaracion):
  def __init__(self, parametros):
    super().__init__()
    self.parametros = parametros  # [AST_identificador]
  def __str__(self):
    return f"Parámetros : {show(self.parametros)}"
  def restore(self):
    return super().restore(f"{''.join(map(restore, self.parametros))}")

class AST_campo(AST_declaracion):
  def __init__(self, clave, valor):
    super().__init__()
    self.clave = clave  # AST_identificador
    self.valor = valor  # AST_expresion
  def __str__(self):
    return f"{show(self.clave)}:{show(self.valor)}"
  def restore(self):
    return super().restore(f"{restore(self.clave)}{restore(self.valor)}")

class AST_campos(AST_declaracion):
  def __init__(self):
    super().__init__()
    self.lista = []  # [AST_campo]
  def agregar_campo(self, campo):
    self.lista.insert(0, campo)
  def cantidad(self):
    return len(self.lista)
  def apertura(self, c):
    if self.cantidad() > 0:
      self.lista[0].apertura(c)
    else:
      super().apertura(c)
  def __str__(self):
    return f"{show(self.lista)}"
  def restore(self):
    return super().restore(f"{restore(self.lista)}")

class AST_argumentos(AST_modificador):
  def __init__(self):
    super().__init__()
    self.lista = []  # [AST_expresion]
  def agregar_argumento(self, arg):
    self.lista.insert(0, arg)
  def cantidad(self):
    return len(self.lista)
  def __str__(self):
    return f"{show(self.lista)}"
  def restore(self):
    return super().restore(f"{restore(self.lista)}")

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

class AST_identificadores(AST_asignable):
  def __init__(self, identificadores):
    super().__init__()
    self.identificadores = identificadores # [AST_identificador]
  def __str__(self):
    return f"{show(self.identificadores)}"
  def restore(self):
    return super().restore(f"{''.join(map(restore, self.identificadores))}")

class AST_modificador_operador(AST_modificador):
  def __init__(self):
    super().__init__()

class AST_modificador_operador_binario(AST_modificador_operador):
  def __init__(self, clase, expresion):
    self.clase = clase          # string
    self.expresion = expresion  # AST_expresion
    super().__init__()

class AST_modificador_operador_posfijo(AST_modificador_operador):
  def __init__(self, clase):
    self.clase = clase          # string
    super().__init__()
  def restore(self):
    return super().restore(f"{self.clase}")

class AST_modificador_objeto(AST_modificador):
  def __init__(self):
    super().__init__()

class AST_modificador_objeto_acceso(AST_modificador_objeto):
  def __init__(self, identificador):
    super().__init__()
    self.campo = identificador    # AST_identificador

class AST_modificador_objeto_index(AST_modificador_objeto):
  def __init__(self, expresion):
    super().__init__()
    self.indice = expresion       # AST_expresion

def modificador_con_skip(modificador, s):
  if type(modificador) == type([]):
    if len(modificador) > 0:
      modificador[0].apertura(s)
    else:
      modificador = s
  else:
    modificador.apertura(s)
  return modificador

def aplicarModificador(nodo, mod):
  resultado = nodo
  if type(mod) is AST_modificador_objeto_acceso:
    # ACCESO OBJETO: {nodo}.{mod}
    resultado = AST_expresion_acceso(nodo, mod)
  elif type(mod) is AST_modificador_objeto_index:
    # INDEX OBJETO: {nodo} [ {mod} ]
    resultado = AST_expresion_index(nodo, mod)
  elif isinstance(mod, AST_modificador_operador_binario):
    # OPERACIÓN {nodo} + {mod}
    mod.expresion.imitarEspacios(mod)
    resultado = AST_operador(nodo, mod.clase, mod.expresion)
  elif isinstance(mod, AST_modificador_operador_posfijo):
    # OPERACIÓN {nodo} {mod}
    nodo.clausura(mod.restore())
    resultado = AST_operador(nodo, mod.clase, None)
  elif isinstance(mod, AST_argumentos):
    # INVOCACIÓN: {nodo} ( {mod} )
    resultado = AST_invocacion(nodo, mod)
  elif isinstance(mod, AST_expresion):
    if isinstance(nodo, AST_declaracion_variable):
      # ASIGNACIÓN VARIABLE: Var {nodo} = {mod}
      resultado.asignacion = mod
    else:
      # ASIGNACIÓN GENÉRICA: {nodo} = {mod}
      resultado = AST_asignacion(nodo, mod)
  else: # [AST_skippeable]
    resultado.clausura(mod)
  if isinstance(mod, AST_modificador):
    for ad in mod.adicional:
      resultado = aplicarModificador(resultado, ad)
  return resultado

def cantidad(x):
  if type(x) == type([]):
    return len(x)
  return x.cantidad()

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
    return ''.join(list(map(restore,x)))
  return x.restore()

parser = yacc()

def parsear(contenido):
  return parser.parse(contenido, lex())