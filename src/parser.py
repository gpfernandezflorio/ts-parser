from my_ply.lex import lex, LexToken
from my_ply.yacc import yacc

tokens = (
  'DECL_FUNC',
  'DECL_VAR',
  'DECL_CLASS',
  'IMPORT',
  'EXPORT',
  'FROM',
  'AS',
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
  'PREGUNTA',
  'ITERADOR',
  'MAS',
  'MENOS',
  'POR',
  'DIV',
  'PRE_MOD_UNARIO',
  'IMPLEMENTS',
  'EXTENDS',
  'NEW',
  'DOS_PUNTOS',
  'PUNTO_Y_COMA',
  'PUNTO',
  'COMA',
  'FORMAT_STRING_COMPLETE',
  'SKIP'
)

reserved_map = {
  'function':'DECL_FUNC',
  'class':'DECL_CLASS',
  'import':'IMPORT',
  'export':'EXPORT',
  'from':'FROM',
  'as':'AS',
  'else':'ELSE',
  'abstract':'ABSTRACT',
  'implements':'IMPLEMENTS',
  'extends':'EXTENDS',
  'new':'NEW'
}

for k in ['let','const','var']:
  reserved_map[k] = 'DECL_VAR'

for k in ['if','for','while']:
  reserved_map[k] = 'COMBINADOR'

for k in ['in','of']:
  reserved_map[k] = 'ITERADOR'

for k in ['abstract','static','private','protected','readonly','get','set']:
  reserved_map[k] = 'PRE_MOD_UNARIO'

def t_IDENTIFICADOR(t):
  r'[A-Za-z_][\w_]*'
  t.type = reserved_map.get(t.value, "IDENTIFICADOR")
  return t
t_NUMERO = r'(\d*\.\d+)|\d+'
t_STRING = r'("[^"]*")|(\'[^\']*\')|(`[^`$]*`)'
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
t_OPERADOR_BINARIO = r'===|!==|==|!=|>=|<=|>|<|&&|\|\|'
t_PREGUNTA = r'\?'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIV = r'/'
t_DOS_PUNTOS = r':'
t_PUNTO_Y_COMA = r';'
t_PUNTO = r'\.'
t_COMA = r','
def t_FORMAT_STRING_COMPLETE(t):
  r'(`[^`]*`)'
  t.type = "FORMAT_STRING_COMPLETE"
  t.lexer.lineno += t.value.count('\n')
  return t

def t_SKIP(t):
  r'(\ |\t|\n)+'
  t.type = "SKIP"
  t.lexer.lineno += t.value.count('\n')
  return t

def t_error(t):
  t.value = t.value[0]
  t.lexer.skip(1)
  return t

precedence = (
  ('left', 'VACIO'),
  ('left', 'PRE_MOD_UNARIO'),
  ('left', 'PUNTO_Y_COMA'),
  ('left', 'ABRE_PAREN'),
)

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

def p_error(p, parser=None):
  if p is None:
    print('EoF')
  else:
    print(f'Error en línea {p.lineno}, columna {p.colno} {p.value!r}')
  print(parser.statestack)
  print(parser.symstack)
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
    D -> `...`          D_STRING      AST_format_string
    D -> {...}          D_OBJETO      AST_expresion_objeto
    D -> (...)          D_PARENT      AST_expresion
    D -> if|for|while   D_COMMAND     AST_combinador
    D -> !|-|++|--      D_PREFIX      AST_operador
    D -> import         D_IMPORT      AST_import
    D -> export         D_EXPORT      AST_export
    D -> class          D_CLASS       AST_declaracion_clase
    D -> static | readonly | abstract | private | protected ...
                        es una declaración pero todavía no sé de qué
                                      AST_declaracion_funcion | AST_declaracion_variable | AST_declaracion_clase
''' #################################################################################################

# DECLARACIÓN : FUNCIÓN (declaración de función o función anónima)
 #################################################################################################
def p_declaracion_function(p): # AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion
  '''
  declaracion : declaracion_de_funcion
  '''
  p[0] = p[1]

def p_declaracion_funcion(p): # AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion
  '''
  declaracion_de_funcion : DECL_FUNC s funcion_declaracion_o_definicion
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])      # [AST_skippeable]
  rec = p[3]                            # AST_funcion_incompleta | AST_declaracion_funcion | AST_invocacion
  if type(rec) is AST_funcion_incompleta:
    rec = AST_expresion_funcion(rec)
  rec.apertura(s)
  p[0] = rec

def p_declaracion_function_decl(p): # AST_declaracion_funcion
  '''
  funcion_declaracion_o_definicion : IDENTIFICADOR s definicion_funcion opt_cierre
  '''
  nombre = AST_identificador(p[1])
  s = p[2]              # [AST_skippeable]
  rec = p[3]            # AST_funcion_incompleta | AST_invocacion
  cierre = p[4]
  # Si la estoy declarando, no debería haber una invocación
  if type(rec) is AST_invocacion:
    print("ERROR p_declaracion_function_decl")
    exit(0)
  nombre.clausura(s)
  p[0] = AST_declaracion_funcion(nombre, rec.parametros, rec.cuerpo, rec.decoradores)
  p[0].imitarEspacios(rec)
  p[0].clausura(cierre)

def p_declaracion_function_anon(p): # AST_funcion_incompleta | AST_invocacion
  '''
  funcion_declaracion_o_definicion : definicion_funcion
  '''
  rec = p[1]            # AST_funcion_incompleta | AST_invocacion
  p[0] = rec

def p_definicion_funcion(p): # AST_funcion_incompleta | AST_invocacion
  '''
  definicion_funcion : parametros s opt_decorador_identificador_tipo cuerpo opt_modificador_funcion
  '''
  parametros = p[1]                             # AST_parametros
  s = p[2]                                      # [AST_skippeable]
  opt_tipo = p[3]                               # AST_identificador | [AST_skippeable]
  cuerpo = p[4]                                 # AST_cuerpo
  modificador = p[5]                            # AST_argumentos | [AST_skippeable]
  parametros.clausura(s)
  expresion = AST_funcion_incompleta(parametros, cuerpo)
  if type(opt_tipo) is AST_identificador:
    decorador = AST_decorador(opt_tipo, False)  # AST_decorador
    expresion.agregar_decorador(decorador)
  else:
    parametros.clausura(opt_tipo)
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
  s1 = concatenar(abre, p[2])     # [AST_skippeable]
  parametros = p[3]               # [AST_identificador]
  cierra = AST_sintaxis(p[4])     # AST_sintaxis
  p[0] = AST_parametros(parametros)
  p[0].apertura(s1)
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

def p_identificadores_con_mod_pre_decl(p): # [AST_identificador]
  '''
  identificadores : modificador_pre_decl_no_vacio primer_identificador
  '''
  modificadores = p[1]    # [AST_modificador_declaracion]
  identificadores = p[2]  # [AST_identificador]
  identificadores[0].modificadores_pre(modificadores)
  p[0] = identificadores

def p_identificadores_sin_mod_pre_decl(p): # [AST_identificador]
  '''
  identificadores : primer_identificador
  '''
  p[0] = p[1]

def p_identificadores_primer_identificador(p): # [AST_identificador]
  '''
  primer_identificador : IDENTIFICADOR opt_decorador_identificador mas_identificadores
  '''
  identificador = AST_identificador(p[1])
  opt_decorador = p[2]      # AST_decorador | [AST_skippeable]
  rec = p[3]                # [AST_identificador] | [AST_skippeable]
  if type(opt_decorador) is AST_decorador:
    identificador.agregar_decorador(opt_decorador)
  else:
    identificador.clausura(opt_decorador)
  if len(rec) > 0 and type(rec[0]) is AST_identificador:
    rec.insert(0, identificador)
  else:
    identificador.clausura(rec)
    rec = [identificador]
  p[0] = rec

def p_mas_identificadores_fin(p): # [AST_skippeable]
  '''
  mas_identificadores : vacio
  '''
  p[0] = []

def p_mas_identificadores(p): # [AST_identificador] | [AST_skippeable]
  '''
  mas_identificadores : COMA s identificadores
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  rec = p[3]                  # [AST_identificador] | [AST_skippeable]
  if len(rec) > 0 and type(rec[0]) is AST_identificador:
    rec[0].apertura(s)
  else:
    rec = concatenar(s, rec)
  p[0] = rec

def p_opt_decorador_identificador_con_skip(p): # AST_decorador | [AST_skippeable]
  '''
  opt_decorador_identificador : sf decorador_identificador
  '''
  s = p[1]                  # [AST_skippeable]
  decorador = p[2]          # AST_decorador | [AST_skippeable]
  p[0] = modificador_con_skip(decorador, s)

def p_opt_decorador_identificador_sin_skip(p): # AST_decorador | [AST_skippeable]
  '''
  opt_decorador_identificador : decorador_identificador
  '''
  p[0] = p[1]

def p_decorador_identificador_vacio(p): # [AST_skippeable]
  '''
  decorador_identificador : vacio
  '''
  p[0] = p[1]

def p_decorador_identificador_no_vacio(p): # AST_decorador
  '''
  decorador_identificador : decorador_identificador_no_vacio
  '''
  p[0] = p[1]

def p_opt_decorador_identificador_default(p): # AST_decorador
  '''
  decorador_identificador_no_vacio : ASIGNACION s expresion_asignada
  '''
  s = AST_sintaxis(p[1])                    # AST_sintaxis
  s = concatenar(s, p[2])                   # [AST_skippeable]
  expresion = p[3]                          # AST_expresion
  decorador = AST_decorador(expresion, False) # AST_decorador
  decorador.apertura(s)
  p[0] = decorador

def p_opt_decorador_identificador_opcional(p): # AST_decorador
  '''
  decorador_identificador_no_vacio : PREGUNTA s opt_decorador_identificador_tipo
  '''
  s = AST_sintaxis(p[1])                    # AST_sintaxis
  s = concatenar(s, p[2])                   # [AST_skippeable]
  opt_tipo = p[3]                           # AST_identificador | [AST_skippeable]
  tipo = None
  s = opt_tipo
  if type(opt_tipo) is AST_identificador:
    tipo = opt_tipo
    s = []
  decorador = AST_decorador(tipo, True)  # AST_decorador
  decorador.apertura(s)
  p[0] = decorador

def p_opt_decorador_identificador_tipo(p): # AST_decorador
  '''
  decorador_identificador_no_vacio : decorador_identificador_tipo_no_vacio
  '''
  tipo = p[1]                             # AST_identificador
  decorador = AST_decorador(tipo, False)  # AST_decorador
  p[0] = decorador

# Por alguna razón, esta rompe todo. Creo que tiene algo que ver con que empiece con skip así que en lugar
  # de usar esta, agrego espacios opcionales antes de cada uso
# def p_opt_decorador_identificador_tipo_con_skip(p): # AST_identificador | [AST_skippeable]
#   '''
#   opt_decorador_identificador_tipo : sf decorador_identificador_tipo
#   '''
#   s = p[1]                  # [AST_skippeable]
#   decorador = p[2]          # AST_identificador | [AST_skippeable]
#   p[0] = modificador_con_skip(decorador, s)

def p_opt_decorador_identificador_tipo_sin_skip(p): # AST_identificador | [AST_skippeable]
  '''
  opt_decorador_identificador_tipo : decorador_identificador_tipo
  '''
  p[0] = p[1]

def p_decorador_identificador_tipo_vacio(p): # [AST_skippeable]
  '''
  decorador_identificador_tipo : vacio
  '''
  p[0] = p[1]

def p_decorador_identificador_tipo_no_vacio(p): # AST_identificador
  '''
  decorador_identificador_tipo : decorador_identificador_tipo_no_vacio
  '''
  p[0] = p[1]

def p_decorador_identificador_tipo(p): # AST_identificador
  '''
  decorador_identificador_tipo_no_vacio : DOS_PUNTOS s tipo
  '''
  r = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(r, p[2])   # [AST_skippeable]
  tipo = p[3]               # AST_identificador
  tipo.apertura(s)
  p[0] = tipo

def p_tipo(p): # AST_identificador
  '''
  tipo : IDENTIFICADOR
  '''
  tipo = AST_identificador(p[1])
  p[0] = tipo

# DECLARACIÓN : VARIABLE (declaración de variable)
 #################################################################################################
def p_declaracion_var(p): # AST_declaracion_variable
  '''
  declaracion : declaracion_variable
  '''
  p[0] = p[1]

def p_declaracion_variable(p): # AST_declaracion_variable
  '''
  declaracion_variable : DECL_VAR sf identificador opt_modificador_variable
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
  identificador : IDENTIFICADOR opt_decorador_identificador_tipo
  '''
  identificador = AST_identificador(p[1])       # AST_identificador
  opt_tipo = p[2]                               # AST_identificador | [AST_skippeable]
  if type(opt_tipo) is AST_identificador:
    decorador = AST_decorador(opt_tipo, False)  # AST_decorador
    identificador.agregar_decorador(decorador)
  else:
    identificador.clausura(opt_tipo)
  p[0] = identificador

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
  p[0] = modificador_con_skip(modificador, s)

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

def p_modificador_variable_iteracion(p): # AST_iterador
  '''
  modificador_variable_no_vacio : ITERADOR s expresion
  '''
  iterador = AST_sintaxis(p[1])     # AST_sintaxis
  s = concatenar(iterador, p[2])    # [AST_skippeable]
  expresion = p[3]                  # AST_expresion
  p[0] = AST_iterador(expresion)
  p[0].apertura(s)

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

def p_expresion_asignada_format_string(p): # AST_format_string | AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_asignada : format_string opt_modificador_expresion_asignada
  '''
  format_string = p[1]              # AST_format_string
  modificador_expresion = p[2]      # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(format_string, modificador_expresion)

def p_expresion_asignada_identificador(p): # AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_asignada : IDENTIFICADOR opt_modificador_expresion_asignada
  '''
  identificador = AST_identificador(p[1])
  modificador_expresion = p[2]      # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  expresion_base = AST_expresion_identificador(identificador)
  p[0] = aplicarModificador(expresion_base, modificador_expresion)

def p_expresion_asignada_funcion(p): # AST_expresion_funcion | AST_invocacion
  '''
  expresion_asignada : DECL_FUNC s definicion_funcion opt_cierre
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])      # [AST_skippeable]
  rec = p[3]                            # AST_funcion_incompleta | AST_invocacion
  cierre = p[4]
  rec.apertura(s)
  rec.clausura(cierre)
  if type(rec) is AST_funcion_incompleta:
    rec = AST_expresion_funcion(rec)
  p[0] = rec

def p_expresion_asignada_funcion_new(p): # AST_invocacion
  '''
  expresion_asignada : NEW s IDENTIFICADOR s invocacion
  '''
  new = AST_sintaxis(p[1])                  # AST_sintaxis
  s1 = concatenar(new, p[2])                # [AST_skippeable]
  identificador = AST_identificador(p[3])   # AST_identificador
  s2 = p[4]                                 # [AST_skippeable]
  argumentos = p[5]                         # AST_argumentos
  identificador.apertura(s1)
  identificador.clausura(s1)
  p[0] = aplicarModificador(identificador, argumentos)

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

def p_expresion_format_string(p): # AST_format_string | AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_sin_pre : format_string opt_modificador_expresion
  '''
  format_string = p[1]              # AST_format_string
  modificador_expresion = p[2]      # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(format_string, modificador_expresion)

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
  rec = p[3]                            # AST_funcion_incompleta | AST_invocacion
  rec.apertura(s)
  if type(rec) is AST_funcion_incompleta:
    rec = AST_expresion_funcion(rec)
  p[0] = rec

def p_expresion_objeto(p): # AST_expresion_objeto
  '''
  expresion_sin_pre : objeto
  '''
  objeto = p[1]
  p[0] = objeto

def p_expresion_parentesis(p): # AST_expresion
  '''
  expresion_sin_pre : expresion_entre_parentesis
  '''
  expresion = p[1] # AST_expresion
  p[0] = p[1]

def p_expresion_entre_parentesis(p): # AST_expresion
  '''
  expresion_entre_parentesis : ABRE_PAREN s expresion CIERRA_PAREN opt_modificador_expresion
  '''
  s = AST_sintaxis(p[1])
  s = concatenar(s, p[2])
  expresion = p[3]
  if isinstance(expresion, AST_operador):
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

def p_opt_modificador_expresion_sin_skip(p): # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable]  {(, =, ., as, [}
  '''
  opt_modificador_expresion : modificador_expresion
  '''
  modificador_expresion = p[1]    # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable]
  p[0] = modificador_expresion

def p_modificador_expresion_vacio(p): # [AST_skippeable]                      {lambda}
  '''
  modificador_expresion : vacio
  '''
  p[0] = []

def p_modificador_expresion_no_vacio(p): # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable]
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

def p_modificador_expresion_como_tipo(p): # AST_modificador_comotipo
  '''
  modificador_expresion_no_vacio : comotipo
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
                   | ITERADOR
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

def p_comotipo(p): # AST_modificador_comotipo
  '''
  comotipo : AS s expresion
  '''
  s = AST_sintaxis(p[1])
  s = concatenar(s, p[2])                             # [AST_skippeable]
  expresion = p[3]                                    # AST_expresion
  expresion.apertura(s)
  modificador = AST_modificador_comotipo(expresion)   # AST_modificador_comotipo
  p[0] = modificador

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
  mas_argumentos : COMA s argumentos
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  argumentos = p[3]           # AST_argumentos
  argumentos.apertura_temporal(s)
  p[0] = argumentos

def p_fin_argumentos(p): # AST_argumentos
  '''
  fin_argumentos : CIERRA_PAREN opt_modificador_invocacion
  '''
  opt_adicional = p[2]                      # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable]
  p[0] = AST_argumentos()
  p[0].modificador_adicional(opt_adicional)

def p_opt_modificador_invocacion_con_skip(p): # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable] | [AST_skippeable]
  '''
  opt_modificador_invocacion : sf modificador_invocacion
  '''
  s = p[1]                    # [AST_skippeable]
  modificador = p[2]          # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable] | [AST_skippeable]
  p[0] = modificador_con_skip(modificador, s)

def p_opt_modificador_invocacion_sin_skip(p): # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable]
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

def p_modificador_invocacion_no_vacio(p): # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable]
  '''
  modificador_invocacion : modificador_invocacion_no_vacio
  '''
  p[0] = p[1]

def p_modificador_invocacion_objeto(p): # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_modificador_comotipo | [AST_skippeable]
  '''
  modificador_invocacion_no_vacio : modificador_expresion_no_vacio
  '''
  modificador_objeto = p[1]
  p[0] = modificador_objeto

def p_modificador_invocacion_cierre(p): # [AST_skippeable]
  '''
  modificador_invocacion : cierre
  '''
  cierre = p[1]                    # [AST_skippeable]
  p[0] = cierre

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

# DECLARACIÓN : format_string
 #################################################################################################
def p_declaracion_format_string(p): # AST_format_string
  '''
  declaracion : format_string opt_modificador_objeto_comando
  '''
  format_string = p[1]            # AST_format_string
  modificador = p[2]              # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  p[0] = aplicarModificador(format_string, modificador)

def p_format_string_empty(p): # AST_format_string
  '''
  format_string : FORMAT_STRING_COMPLETE
  '''
  p[0] = AST_format_string(p[1])

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
  campo : clave_campo s DOS_PUNTOS s expresion
  '''
  clave = p[1] # AST_identificador | AST_expresion_literal (string)
  s = p[2]
  dp = AST_sintaxis(p[3])
  s = concatenar(s, dp)
  s = concatenar(s, p[4])
  valor = p[5]
  valor.apertura(s)
  p[0] = AST_campo(clave, valor)

def p_clave_campo_identificador(p): # AST_identificador
  '''
  clave_campo : IDENTIFICADOR
  '''
  clave = AST_identificador(p[1]) # AST_identificador
  p[0] = clave

def p_clave_campo_string(p): # AST_expresion_literal
  '''
  clave_campo : STRING
  '''
  clave = AST_expresion_literal(p[1])   # AST_expresion_literal
  p[0] = clave

def p_clave_campo_format_string(p): # AST_format_string
  '''
  clave_campo : format_string
  '''
  clave = p[1]      # AST_format_string
  p[0] = clave

# DECLARACIÓN : PARENTESIS
 #################################################################################################
def p_declaracion_parentesis(p): # AST_expresion
  '''
  declaracion : expresion_entre_parentesis
  '''
  expresion = p[1] # AST_expresion
  p[0] = p[1]

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

# DECLARACIÓN : IMPORT (import)
 #################################################################################################
def p_declaracion_import(p): # AST_import
  '''
  declaracion : IMPORT s elementos_a_importar s opt_cierre
  '''
  r = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(r, p[2])   # [AST_skippeable]
  importar = p[3]           # AST_import
  importar.apertura(s)
  s = concatenar(p[4], p[5])
  importar.clausura(s)
  p[0] = importar

def p_import_archivo(p): # AST_import
  '''
  elementos_a_importar : STRING
  '''
  archivo = AST_expresion_literal(p[1])   # AST_expresion_literal
  p[0] = AST_import(archivo)

def p_import_elementos(p): # AST_import
  '''
  elementos_a_importar : importables s opt_importar_como FROM s STRING
  '''
  importables = p[1]                      # AST_identificador | AST_identificadores | AST_sintaxis
  s1 = p[2]                               # [AST_skippeable]
  opt_alias = p[3]                        # AST_identificador | [AST_skippeable]
  r = AST_sintaxis(p[4])                  # AST_sintaxis
  s2 = concatenar(r,p[5])                 # [AST_skippeable]
  archivo = AST_expresion_literal(p[6])   # AST_expresion_literal
  importables.clausura(s1)
  archivo.apertura(s2)
  p[0] = AST_import(archivo, importables, opt_alias)

def p_imporables_identificador(p): # AST_identificador | AST_identificadores
  '''
  importables : identificador
  '''
  identificador = p[1] # AST_identificador | AST_identificadores
  p[0] = identificador

def p_imporables_todo(p): # AST_sintaxis
  '''
  importables : POR
  '''
  todo = AST_sintaxis(p[1]) # AST_sintaxis
  p[0] = todo

def p_import_como_alias(p): # AST_identificador
  '''
  opt_importar_como : AS s IDENTIFICADOR s
  '''
  r = AST_sintaxis(p[1])            # AST_sintaxis
  s = concatenar(r,p[2])            # [AST_skippeable]
  alias = AST_identificador(p[3])   # AST_identificador
  alias.apertura(s)
  p[0] = alias

def p_import_como_vacio(p): # [AST_skippeable]
  '''
  opt_importar_como : vacio
  '''
  p[0] = []

# DECLARACIÓN : EXPORT (export)
 #################################################################################################
def p_declaracion_export(p): # AST_export
  '''
  declaracion : EXPORT s declaracion_o_identificador
  '''
  r = AST_sintaxis(p[1])            # AST_sintaxis
  s = concatenar(r,p[2])            # [AST_skippeable]
  exportado = p[3]                  # AST_declaracion_variable | AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion | AST_declaracion_clase | AST_identificador | AST_identificadores
  p[0] = AST_export(p[3])
  p[0].apertura(s)

def p_export_declaracion(p): # AST_declaracion_variable | AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion | AST_declaracion_clase
  '''
  declaracion_o_identificador : declaracion_variable
                              | declaracion_de_funcion
                              | declaracion_de_clase
                              | declaracion_otro
  '''
  p[0] = p[1]

def p_export_identificador(p): # AST_identificador | AST_identificadores | AST_asignacion
  '''
  declaracion_o_identificador : identificador opt_modificador_identificador
  '''
  identificador = p[1]
  modificador = p[2]
  p[0] = aplicarModificador(identificador, modificador)

def p_opt_modificador_identificador_con_skip(p):
  '''
  opt_modificador_identificador : sf modificador_identificador
  '''
  s = p[1]
  modificador = p[2]
  modificador.apertura(s)
  p[0] = modificador

def p_opt_modificador_identificador_sin_skip(p):
  '''
  opt_modificador_identificador : modificador_identificador
  '''
  p[0] = p[1]

def p_modificador_identificador_vacio(p):
  '''
  modificador_identificador : vacio
  '''
  p[0] = p[1]

def p_modificador_identificador_cierre(p):
  '''
  modificador_identificador : cierre
  '''
  p[0] = p[1]

def p_modificador_identificador_no_vacio(p):
  '''
  modificador_identificador : asignacion
  '''
  p[0] = p[1]

# DECLARACIÓN : CLASS (class)
 #################################################################################################
def p_declaracion_clase(p): # AST_declaracion_clase
  '''
  declaracion : declaracion_de_clase
  '''
  p[0] = p[1]

def p_declaracion_de_clase(p): # AST_declaracion_clase
  '''
  declaracion_de_clase : DECL_CLASS s IDENTIFICADOR opt_modificador_clase cuerpo_clase
  '''
  s = AST_sintaxis(p[1])            # AST_sintaxis
  s = concatenar(s, p[2])           # [AST_sintaxis]
  nombre = AST_identificador(p[3])  # AST_identificador
  post_mods = p[4]                  # [AST_modificador_declaracion]
  definicion = p[5]                 # AST_cuerpo
  nombre.apertura(s)
  p[0] = AST_declaracion_clase(nombre, definicion, post_mods)

def p_cuerpo_clase(p): # AST_cuerpo
  '''
  cuerpo_clase : ABRE_LLAVE programa_clase CIERRA_LLAVE
  '''
  abre = AST_sintaxis(p[1])
  contenido = p[2]               # [AST_nodo]
  cierra = AST_sintaxis(p[3])
  programa = AST_cuerpo(contenido)
  programa.apertura(abre)
  programa.clausura(cierra)
  p[0] = programa

def p_programa_clase_que_no_empieza_con_skip(p):
  '''
  programa_clase : programa_clase_util
  '''
  p[0] = p[1]

def p_programa_clase_que_empieza_con_skip(p):
  '''
  programa_clase : sf programa_clase_util
  '''
  p[0] = concatenar(p[1], p[2])

def p_programa_clase_util_vacio(p):
  '''
  programa_clase_util : vacio
  '''
  p[0] = []

def p_programa_clase_util_no_vacio(p):
  '''
  programa_clase_util : declaracion_dentro_de_clase programa_clase_util
  '''
  p[0] = concatenar(p[1], p[2])

def p_declaracion_dentro_de_clase_con_pre(p):
  '''
  declaracion_dentro_de_clase : modificador_pre_decl identificador opt_modificador_dentro_de_clase
  '''
  modificadores_pre = p[1]
  declaracion = p[2]
  opt_modificador_adicional = p[3]    # AST_expresion | AST_expresion_funcion | [AST_skippeable]
  declaracion = aplicarModificador(declaracion, opt_modificador_adicional)
  declaracion.modificadores_pre(modificadores_pre)
  p[0] = declaracion

def p_declaracion_dentro_de_clase_sin_pre(p):
  '''
  declaracion_dentro_de_clase : identificador opt_modificador_dentro_de_clase
  '''
  declaracion = p[1]
  opt_modificador_adicional = p[2]    # AST_expresion | AST_expresion_funcion | [AST_skippeable]
  declaracion = aplicarModificador(declaracion, opt_modificador_adicional)
  p[0] = declaracion

def p_opt_modificador_dentro_de_clase_con_skip(p): # AST_expresion | AST_expresion_funcion | [AST_skippeable]
  '''
  opt_modificador_dentro_de_clase : sf modificador_dentro_de_clase
  '''
  s = p[1]
  modificador = p[2] # AST_expresion | [AST_skippeable]
  if isinstance(modificador, AST_expresion):
    modificador.apertura(s)
  else:
    modificador = concatenar(modificador, s)
  p[0] = modificador

def p_opt_modificador_dentro_de_clase_sin_skip(p): # AST_expresion | AST_expresion_funcion | [AST_skippeable]
  '''
  opt_modificador_dentro_de_clase : modificador_dentro_de_clase
  '''
  p[0] = p[1]

def p_modificador_dentro_de_clase_vacio(p): # [AST_skippeable]
  '''
  modificador_dentro_de_clase : vacio
  '''
  p[0] = p[1]

def p_modificador_dentro_de_clase_cierre(p): # [AST_skippeable]
  '''
  modificador_dentro_de_clase : cierre
  '''
  p[0] = p[1]

def p_modificador_dentro_de_clase_no_vacio(p): # AST_expresion | AST_expresion_funcion
  '''
  modificador_dentro_de_clase : modificador_dentro_de_clase_no_vacio
  '''
  p[0] = p[1]

def p_modificador_dentro_de_clase_asignacion(p): # AST_expresion
  '''
  modificador_dentro_de_clase_no_vacio : asignacion
  '''
  asignacion = p[1]       # AST_expresion
  p[0] = asignacion

def p_modificador_dentro_de_clase_funcion(p): # AST_expresion_funcion
  '''
  modificador_dentro_de_clase_no_vacio : definicion_funcion
  '''
  definicion = p[1]                                           # AST_expresion_funcion | AST_invocacion
  # Si la estoy declarando, no debería haber una invocación
  if type(definicion) is AST_invocacion:
    print("ERROR p_modificador_dentro_de_clase_funcion")
    exit(0)
  p[0] = definicion

def p_opt_modificador_clase_con_skip(p): # [AST_modificador_declaracion] | [AST_skippeable]
  '''
  opt_modificador_clase : sf modificador_clase
  '''
  s = p[1]
  modificadores = p[2]
  if len(modificadores) > 0:
    modificadores[-1].apertura(s)
  else:
    modificadores = s
  p[0] = modificadores

def p_opt_modificador_clase_sin_skip(p): # [AST_modificador_declaracion]
  '''
  opt_modificador_clase : modificador_clase
  '''
  p[0] = p[1]

def p_modificador_clase_vacio(p):
  '''
  modificador_clase : vacio
  '''
  p[0] = p[1]

def p_modificador_clase_no_vacio(p): # [AST_modificador_declaracion]
  '''
  modificador_clase : modificador_clase_no_vacio
  '''
  p[0] = p[1]

def p_modificador_clase_implements(p): # [AST_modificador_declaracion]
  '''
  modificador_clase_no_vacio : IMPLEMENTS s IDENTIFICADOR opt_modificador_clase
  '''
  implements = AST_sintaxis(p[1])   # AST_sintaxis
  s = concatenar(implements, p[2])  # [AST_skippeable]
  nombre = AST_identificador(p[3])  # AST_identificador
  rec = p[4]                        # [AST_modificador_declaracion]
  nombre.apertura(s)
  implementacion = AST_modificador_declaracion_implementacion(nombre)
  p[0] = concatenar(implementacion, rec)

def p_modificador_clase_extends(p): # [AST_modificador_declaracion]
  '''
  modificador_clase_no_vacio : EXTENDS s IDENTIFICADOR opt_modificador_clase
  '''
  extends = AST_sintaxis(p[1])      # AST_sintaxis
  s = concatenar(extends, p[2])     # [AST_skippeable]
  nombre = AST_identificador(p[3])  # AST_identificador
  rec = p[5]                        # [AST_modificador_declaracion]
  nombre.apertura(s)
  extension = AST_modificador_declaracion_extension(nombre)
  p[0] = concatenar(extension, rec)


# DECLARACIÓN : ? (static | readonly | abstract | private | protected ...)
 #################################################################################################
def p_declaracion_otra_declaracion(p): # AST_declaracion_variable | AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion | AST_declaracion_clase
  '''
  declaracion : declaracion_otro
  '''
  p[0] = p[1]

def p_declaracion_otro(p): # AST_declaracion_variable | AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion | AST_declaracion_clase
  '''
  declaracion_otro : PRE_MOD_UNARIO opt_modificador_pre_decl declaracion_o_identificador
  '''
  unario = AST_identificador(p[1])  # AST_identificador
  modificadores = p[2]              # [AST_modificador_declaracion]
  declaracion = p[3]                # AST_declaracion_variable | AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion | AST_declaracion_clase
  unario = AST_modificador_declaracion_unario(unario)
  modificadores = concatenar(unario, modificadores)
  declaracion.modificadores_pre(modificadores)
  p[0] = declaracion

def p_opt_modificador_pre_decl_con_skip(p): # [AST_modificador_declaracion] | [AST_skippeable]
  '''
  opt_modificador_pre_decl : sf modificador_pre_decl
  '''
  s = p[1]
  modificadores = p[2]
  if len(modificadores) > 0:
    modificadores[-1].apertura(s)
  else:
    modificadores = s
  p[0] = modificadores

def p_opt_modificador_pre_decl_sin_skip(p): # [AST_modificador_declaracion]
  '''
  opt_modificador_pre_decl : modificador_pre_decl
  '''
  p[0] = p[1]

def p_modificador_pre_decl_vacio(p): # [AST_modificador_declaracion]
  '''
  modificador_pre_decl : vacio
  '''
  p[0] = p[1]

def p_modificador_pre_decl_no_vacio(p): # [AST_modificador_declaracion]
  '''
  modificador_pre_decl : modificador_pre_decl_no_vacio
  '''
  p[0] = p[1]

def p_modificador_pre_decl_unario(p): # [AST_modificador_declaracion]
  '''
  modificador_pre_decl_no_vacio : PRE_MOD_UNARIO opt_modificador_pre_decl
  '''
  unario = AST_identificador(p[1])  # AST_identificador
  rec = p[2]                        # [AST_modificador_declaracion]
  unario = AST_modificador_declaracion_unario(unario)
  p[0] = concatenar(unario, rec)

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
  'vacio : %prec VACIO'
  p[0] = []

class AST_nodo(object):
  def __init__(self):
    self.cierra = []
    self.abre = []
    self.pre_mods = [] # TODO: Ver si esto (y la función modificadores_pre) tiene sentido que esté acá o dónde (debería aplicar únicamente a las declaraciones, creo)
  def imitarEspacios(self, otro):
    self.abre = otro.abre + self.abre
    self.cierra = self.cierra + otro.cierra
  def modificadores_pre(self, modificadores):
    self.pre_mods = modificadores
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
  def __init__(self, nombre, parametros, cuerpo, decoradores=[]):
    super().__init__()
    self.nombre = nombre            # AST_identificador
    self.parametros = parametros    # AST_parametros
    self.cuerpo = cuerpo            # AST_cuerpo
    self.decoradores = decoradores  # [AST_decorador]
  def __str__(self):
    return f"DeclaraciónFunción : {show(self.nombre)}"
  def restore(self):
    return super().restore(f"{restore(self.nombre)}{restore(self.parametros)}{restore(self.decoradores)}{restore(self.cuerpo)}")

class AST_declaracion_clase():
  def __init__(self, nombre, definicion, post_mods):
    super().__init__()
    self.nombre = nombre            # AST_identificador
    self.definicion = definicion    # AST_cuerpo
    self.post_mods = post_mods      # [AST_modificador_declaracion]
  def __str__(self):
    return f"Declaración clase : {show(self.nombre)}"
  def restore(self):
    return super().restore(f"{restore(self.pre_mods)}{restore(self.nombre)}{restore(self.post_mods)}{restore(self.definicion)}")

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
  def __init__(self, funcion_incompleta):
    super().__init__()
    self.parametros = funcion_incompleta.parametros   # AST_parametros
    self.cuerpo = funcion_incompleta.cuerpo           # AST_cuerpo
    self.imitarEspacios(funcion_incompleta)
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
    if type(funcion) is AST_funcion_incompleta:
      self.funcion = AST_expresion_funcion(funcion) # AST_identificador | AST_expresion_funcion
    else:
      self.funcion = funcion                        # AST_identificador | AST_expresion_funcion
    self.argumentos = argumentos                    # AST_argumentos
  def __str__(self):
    args = '' if cantidad(self.argumentos) == 0 else f" con {show(self.argumentos)}"
    return f"Invocacion : {show(self.funcion)}{args}"
  def restore(self):
    return super().restore(f"{restore(self.funcion)}{restore(self.argumentos)}")

class AST_iteracion(AST_declaracion):
  def __init__(self, variable, rango):
    super().__init__()
    self.variable = variable    # AST_identificador
    self.rango = rango          # AST_expresion
  def __str__(self):
    return f"Iteración : {show(self.variable)} {show(self.rango)}"
  def restore(self):
    return super().restore(f"{restore(self.variable)}{restore(self.rango)}")

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
    self.clave = clave  # AST_identificador | AST_expresion_literal (string)
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
    self.tmp = None
  def agregar_argumento(self, arg):
    if not (self.tmp is None):
      arg.apertura(self.tmp)
      self.tmp = None
    self.lista.insert(0, arg)
  def apertura_temporal(self, s):
    if len(self.lista) > 0:
      self.lista[0].apertura(s)
    elif self.tmp is None:
      self.tmp = s
    else:
      self.tmp = concatenar(s, self.tmp)
  def apertura(self, s):
    if not (self.tmp is None):
      s = concatenar(s, self.tmp)
    super().apertura(s)
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
    self.decoradores = []                 # [AST_decorador]
  def agregar_decorador(self, decorador):
    self.decoradores.append(decorador)
  def __str__(self):
    return f"{self.identificador}"
  def restore(self):
    return super().restore(f"{self.identificador}{restore(self.decoradores)}")

class AST_identificadores(AST_asignable):
  def __init__(self, identificadores):
    super().__init__()
    self.identificadores = identificadores # [AST_identificador]
  def __str__(self):
    return f"{show(self.identificadores)}"
  def restore(self):
    return super().restore(f"{''.join(map(restore, self.identificadores))}")

class AST_import(AST_declaracion):
  def __init__(self, archivo, importables=None, opt_alias=[]):
    super().__init__()
    self.archivo = archivo          # AST_expresion_literal
    self.importables = importables  # AST_identificador | AST_identificadores | AST_sintaxis | None
    self.opt_alias = opt_alias      # AST_identificador | [AST_skippeable]
  def __str__(self):
    return f"Import {show(self.archivo)}"
  def restore(self):
    return super().restore(f"{restore(self.importables)}{restore(self.opt_alias)}{restore(self.archivo)}")

class AST_export(AST_declaracion):
  def __init__(self, exportable):
    super().__init__()
    # Si lo estoy exportando, no debería ser una invocación ni una expresión suelta
    if type(exportable) is AST_invocacion or type(exportable) is AST_expresion_funcion:
      print("ERROR p_declaracion_function_decl")
      exit(0)
    self.exportable = exportable    # AST_declaracion_variable | AST_declaracion_funcion | AST_identificador | AST_identificadores
  def __str__(self):
    return f"Export {show(self.exportable)}"
  def restore(self):
    return super().restore(restore(self.exportable))

class AST_modificador_operador(AST_modificador):
  def __init__(self):
    super().__init__()

class AST_funcion_incompleta(AST_modificador):
  def __init__(self, parametros, cuerpo):
    super().__init__()
    self.parametros = parametros   # AST_parametros
    self.cuerpo = cuerpo           # AST_cuerpo
    self.decoradores = []          # [AST_decorador]
  def agregar_decorador(self, decorador):
    self.decoradores.append(decorador)

class AST_decorador(AST_modificador):
  def __init__(self, opt_tipo_o_default, opcional):
    super().__init__()
    self.opt_tipo_o_default = opt_tipo_o_default    # AST_identificador | AST_expresion | None
    self.opcional = opcional                        # bool
  def restore(self):
    return super().restore(f"{restore(self.opt_tipo_o_default)}")

class AST_modificador_operador_binario(AST_modificador_operador):
  def __init__(self, clase, expresion):
    super().__init__()
    self.clase = clase          # string
    self.expresion = expresion  # AST_expresion

class AST_modificador_comotipo(AST_modificador):
  def __init__(self, expresion):
    super().__init__()
    self.expresion = expresion  # AST_expresion

class AST_modificador_operador_posfijo(AST_modificador_operador):
  def __init__(self, clase):
    super().__init__()
    self.clase = clase          # string
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

class AST_iterador(AST_modificador):
  def __init__(self, expresion):
    super().__init__()
    self.expresion = expresion    # AST_expresion

class AST_modificador_declaracion(AST_modificador):
  def __init__(self):
    super().__init__()

class AST_modificador_declaracion_unario(AST_modificador_declaracion):
  def __init__(self, nombre):
    super().__init__()
    self.nombre = nombre
  def restore(self):
    return super().restore(f"{restore(self.nombre)}")

class AST_modificador_declaracion_implementacion(AST_modificador_declaracion):
  def __init__(self, nombre):
    super().__init__()
    self.nombre = nombre
  def restore(self):
    return super().restore(f"{restore(self.nombre)}")

class AST_modificador_declaracion_extension(AST_modificador_declaracion):
  def __init__(self, nombre):
    super().__init__()
    self.nombre = nombre
  def restore(self):
    return super().restore(f"{restore(self.nombre)}")

class AST_format_string(AST_expresion):
  def __init__(self, completo):
    super().__init__()
    # TODO: parsing auxiliar para identificar las expresiones dentro de "completo"
    self.elementos = []    # [AST_expresion]
  def restore(self):
    return super().restore(f"{''.join(map(restore, self.elementos))}")

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
    # OPERACIÓN: {nodo} + {mod}
    mod.expresion.imitarEspacios(mod)
    resultado = AST_operador(nodo, mod.clase, mod.expresion)
  elif isinstance(mod, AST_modificador_comotipo):
    # COMO TIPO: {nodo} as {mod}
    resultado.clausura(restore(mod))
  elif isinstance(mod, AST_modificador_operador_posfijo):
    # OPERACIÓN: {nodo} {mod}
    nodo.clausura(mod.restore())
    resultado = AST_operador(nodo, mod.clase, None)
  elif isinstance(mod, AST_argumentos):
    # INVOCACIÓN: {nodo} ( {mod} )
    resultado = AST_invocacion(nodo, mod)
  elif isinstance(mod, AST_iterador):
    # ITERACIÓN: {nodo} in {mod}
    mod.expresion.imitarEspacios(mod)
    resultado = AST_iteracion(nodo, mod.expresion)
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

def mostrarTokens(tokens):
  for t in tokens:
    print(fill(str(t.lineno),3) + ":" + fill(str(t.colno),6) + fill(t.type,15) + clean(t.value))

def mostrarAST(ast):
  for n in ast:
    print(n)

def mostrarDiff(a, b):
  lineas_a = a.split('\n')
  lineas_b = a.split('\n')
  i = 0
  m = min(len(lineas_a), len(lineas_b))
  while i < m and lineas_a[i] == lineas_b[i]:
    i += 1
  if i == m: # Uno es más largo
    if len(lineas_b) > len(lineas_a):
      print(f"Se generaron {len(lineas_b) - len(lineas_a)} líneas adicionales:")
      lineas = lineas_b[m:]
    else:
      print(f"Se perdieron {len(lineas_a) - len(lineas_b)} líneas:")
      lineas = lineas_a[m:]
    print(''.join(lineas))
  else:
    print(f"[{i+1}]")
    print(f"  {lineas_a[i]}")
    print(f"  {lineas_b[i]}")