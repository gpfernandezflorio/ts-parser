from my_ply.lex import lex, LexToken
from my_ply.yacc import yacc
import functools

tokens = (
  'DECL_FUNC',
  'DECL_VAR',
  'DECL_CLASS',
  'RETURN',
  'IMPORT',
  'EXPORT',
  'FROM',
  'AS',
  'IS',
  'COMBINADOR1',
  'COMBINADOR2',
  'ELSE',
  'DEFAULT',
  'IDENTIFICADOR',
  'NUMERO',
  'STRING',
  'RE',
  'COMENTARIO_UL',
  'COMENTARIO_ML',
  'ASIGNACION1',
  'ASIGNACION2',
  'ABRE_PAREN',
  'CIERRA_PAREN',
  'ABRE_LLAVE',
  'CIERRA_LLAVE',
  'ABRE_CORCHETE',
  'CIERRA_CORCHETE',
  'OPERADOR_PREFIJO',
  'OPERADOR_INFIJO',
  'OPERADOR_BOOLEANO',
  'PREGUNTA',
  'EXCLAMACION',
  'IN',
  'OF',
  'MAS',
  'MENOS',
  'POR',
  'DIV',
  'MENOR',
  'MAYOR',
  'IMPLEMENTS',
  'EXTENDS',
  'NEW',
  'DOS_PUNTOS',
  'PUNTO_Y_COMA',
  'ACCESO1',
  'ACCESO2',
  'COMA',
  'FORMAT_STRING_COMPLETE',
  'FLECHA',
  'PIPE',
  'AND',
  'CASE',
  'TYPEOF',
  'VOID',
  'ESPACIO',
  'SALTO',
  'TYPE',
  'CATCH',
  'CORTE_CICLO'
)

reserved_map = {
  'function':'DECL_FUNC',
  'import':'IMPORT',
  'export':'EXPORT',
  'from':'FROM',
  'as':'AS',
  'is':'IS',
  'else':'ELSE',
  'default':'DEFAULT',
  'implements':'IMPLEMENTS',
  'extends':'EXTENDS',
  'new':'NEW',
  'case':'CASE',
  'typeof':'TYPEOF',
  'instanceof':'OPERADOR_BOOLEANO',
  'void':'VOID',
  'in':'IN',
  'of':'OF',
  'type':'TYPE',
  'catch':'CATCH'
}

for k in ['let','const','var']:
  reserved_map[k] = 'DECL_VAR'

for k in ['class','interface','namespace']:
  reserved_map[k] = 'DECL_CLASS'

for k in ['if','for','while','switch']:
  reserved_map[k] = 'COMBINADOR1'

for k in ['try','finally','do']:
  reserved_map[k] = 'COMBINADOR2'

for k in ['return','throw']:
  reserved_map[k] = 'RETURN'

for k in ['break','continue']:
  reserved_map[k] = 'CORTE_CICLO'

def t_IDENTIFICADOR(t):
  r'[A-Za-z_][\w_]*'
  t.type = reserved_map.get(t.value, "IDENTIFICADOR")
  return t
t_NUMERO = r'(\d*\.\d+)|(0x)?\d+'
#            [    comillas dobles   ] [     comillas simples      ] [backtick]
t_STRING = r'("([^\\"]|\\"|\\[^"])*")|(\'([^\\\']|\\\'|\\[^\'])*\')|(`[^`$]*`)'
t_RE = r'(/\ /|/[^/\*\ ]([^\\/\n\r]|\\/|\\\\/|\\(\(|\)|[a-z]|\.|\d))*/)g?(i|m)?'
t_COMENTARIO_UL = r'//[^\n\r]*'
def t_COMENTARIO_ML(t):
  r'/\*([^\*]|\*[^/])*\*/'
  t.type = "COMENTARIO_ML"
  t.lexer.lineno += t.value.count('\n')
  return t
t_ASIGNACION1 = r'='
t_ASIGNACION2 = r'\+=|\*=|-=|/=|\|=|<<=|>>=|%='
t_ABRE_PAREN = r'\('
t_CIERRA_PAREN = r'\)'
t_ABRE_LLAVE = r'{'
t_CIERRA_LLAVE = r'}'
t_ABRE_CORCHETE = r'\['
t_CIERRA_CORCHETE = r'\]'
t_OPERADOR_PREFIJO = r'\.\.\.'
t_OPERADOR_INFIJO = r'\+\+|--'
t_OPERADOR_BOOLEANO = r'===|!==|==|!=|>=|<=|&&|\|\||\?\?'
t_FLECHA = r'=>'
t_PIPE = r'\|'
t_AND = r'&'
t_PREGUNTA = r'\?'
t_EXCLAMACION = r'!'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIV = r'/|%'
t_MENOR = r'<'
t_MAYOR = r'>'
t_DOS_PUNTOS = r':'
t_PUNTO_Y_COMA = r';'
t_ACCESO1 = r'\.'
t_ACCESO2 = r'\?\.|\!\.'
t_COMA = r','
t_ESPACIO = r'(\ |\t)+'
def t_FORMAT_STRING_COMPLETE(t):
  r'(`[^`]*`)'
  t.type = "FORMAT_STRING_COMPLETE"
  t.lexer.lineno += t.value.count('\n')
  return t

def t_SALTO(t):
  r'\n'
  t.type = "SALTO"
  t.lexer.lineno += t.value.count('\n')
  return t

def t_error(t):
  t.value = t.value[0]
  t.lexer.skip(1)
  return t

precedence = (
  ('left', 'VACIO'),
  ('left', 'ESPACIOS'),
  ('left', 'COMENTARIO_ML', 'COMENTARIO_UL', 'ESPACIO', 'SALTO'),
  ('left', 'TYPE'),
  ('left', 'IDENTIFICADOR'),
  ('left', 'MENOR','MAYOR'),
  ('left', 'ABRE_PAREN'),
  ('left', 'ABRE_CORCHETE'),
  ('left', 'ABRE_LLAVE'),
  ('left', 'PUNTO_Y_COMA'),
  ('left', 'DOS_PUNTOS'),
  ('left', 'POR','DIV'),
  ('left', 'OPERADOR_PREFIJO','EXCLAMACION','OPERADOR_INFIJO','IN','OF'),
  ('left', 'MENOS','MAS'),
  ('left', 'ACCESO1', 'ACCESO2'),
  ('left', 'ASIGNACION1', 'ASIGNACION2'),
  ('left', 'FLECHA'),
  ('left', 'OPERADOR_BOOLEANO'),
  ('left', 'PREGUNTA'),
  ('left', 'PIPE','AND'),
  ('left', 'CIERRA_PAREN'),
  ('left', 'CIERRA_CORCHETE'),
  ('left', 'CIERRA_LLAVE'),
  ('left', 'DECL_FUNC'),
  ('left', 'COMA'),
  ('left', 'NEW'),
  ('left', 'AS'),
  ('left', 'IS'),
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

def p_error(t):
  if t is None:
    print('EoF')
  else:
    print(f'Error en línea {t.lineno}, columna {t.colno}: {t.type} ({t.value!r})')
  logParser()
  exit(1)

def es_identificador_sp(s):
  return s in ['abstract','static','private','protected','readonly','get','set','type']

def p_start(p): # AST_programa
  '''
  start : programa
  '''
  p[0] = AST_programa(p[1])

# PROGRAMA : [AST_nodo] #############################################################################
''' Un programa puede ser ...
    P -> PU     ... una lista de declaraciones      p(D) U {lambda}    : (AST_declaracion) : [ P ]
    P -> SF PU  ... o empezar con skippeables antes {skip, comentario} : (AST_skippeable) : [ P ]
''' #################################################################################################
def p_programa_que_no_empieza_con_skip(p): # [AST_nodo]
  '''
  programa : programa_util
  '''
  p[0] = p[1]

def p_programa_que_empieza_con_skip(p): # [AST_nodo]
  '''
  programa : sf programa_util
  '''
  p[0] = concatenar(p[1], p[2])

# PROGRAMA_ÚTIL : [AST_nodo] ########################################################################
''' Un programa útil es una lista de declaraciones (no puede empezar con skippeables)
    PU -> lambda                                    {lambda}
    PU -> D PU                                      p(D)
''' #################################################################################################
def p_programa_util_vacio(p): # [AST_nodo]
  '''
  programa_util : vacio
  '''
  p[0] = []

def p_programa_util_no_vacio(p): # [AST_declaracion]
  '''
  programa_util : declaracion opt_cierre programa_util
  '''
  declaracion = p[1]  # AST_declaracion
  s = p[2]            # [AST_skippeable]
  rec = p[3]          # [AST_declaracion]
  declaracion.clausura(s)
  p[0] = concatenar(declaracion, rec)

# SKIPPEABLE_FORZADO : [AST_skippeable] #############################################################
''' Un skippeable forzado debe tener al menos un skippeable y puede seguir con más skippeables
    SF -> skip S       {skip}         : AST_espacios
    SF -> comentario S {comentario}   : AST_comentario
''' #################################################################################################
def p_sf_espacios(p): # [AST_skippeable]
  '''
  sf : espacios
  '''
  p[0] = p[1]

def p_sf_salto(p): # [AST_skippeable]
  '''
  sf : salto
  '''
  p[0] = p[1]

def p_sf_comentario(p): # [AST_skippeable]
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
def p_skippeable_vacio(p): # [AST_nodo]
  '''
  s : vacio
  '''
  p[0] = []

def p_skippeable_no_vacio(p): # [AST_skippeable]
  '''
  s : sf %prec ESPACIOS
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
    D -> {...}          D_OBJETO      AST_tipo_objeto (ojo: no es un objeto literal, los campos se separan con ; en lugar de con ,)
    D -> (...)          D_PARENT      AST_expresion
    D -> if|for|while   D_COMMAND     AST_combinador
    D -> case           D_COMMAND     AST_combinador
    D -> !|-|++|--      D_PREFIX      AST_operador
    D -> return         D_RETURN      AST_return
    D -> break|continue D_CORTE_CICLO AST_return
    D -> import         D_IMPORT      AST_import
    D -> export         D_EXPORT      AST_export
    D -> class          D_CLASS       AST_declaracion_clase
    D -> type           D_TYPE        AST_declaracion_tipo
''' #################################################################################################

# Primero tengo que dividir entre objeto y no objeto porque si viene una llave después de la condición
  # de if no sé si es el cuerpo del if o un objeto.

def p_declaracion_no_objeto(p): # AST_declaracion
  '''
  declaracion : declaracion_no_objeto
  '''
  declaracion = p[1]
  p[0] = declaracion

# DECLARACIÓN : FUNCIÓN (declaración de función o función anónima)
 #################################################################################################
def p_declaracion_function(p): # AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion
  '''
  declaracion_no_objeto : declaracion_de_funcion
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
    rec = crearExpresionFuncion(rec)
  rec.apertura(s)
  p[0] = rec

def p_declaracion_function_decl(p): # AST_declaracion_funcion
  '''
  funcion_declaracion_o_definicion : IDENTIFICADOR opt_modificador_id_clase definicion_funcion
  '''
  nombre = AST_identificador(p[1])
  opt_decorador = p[2]  # AST_tipo_tupla | [AST_skippeable]
  rec = p[3]            # AST_funcion_incompleta | AST_invocacion
  # Si la estoy declarando, no debería haber una invocación
  if type(rec) is AST_invocacion:
    print("ERROR p_declaracion_function_decl")
    exit(0)
  nombre = aplicarModificador(nombre, opt_decorador)
  funcion = AST_declaracion_funcion(nombre, rec)
  p[0] = funcion

def p_declaracion_function_anon(p): # AST_funcion_incompleta | AST_invocacion
  '''
  funcion_declaracion_o_definicion : definicion_funcion
  '''
  rec = p[1]            # AST_funcion_incompleta | AST_invocacion
  p[0] = rec

def p_definicion_funcion(p): # AST_funcion_incompleta | AST_invocacion
  '''
  definicion_funcion : parametros opt_decorador_tipo opt_cuerpo opt_modificador_funcion
  '''
  parametros = p[1]                             # AST_parametros
  opt_tipo = p[2]                               # AST_decorador_tipo | [AST_skippeable]
  cuerpo = p[3]                                 # AST_cuerpo | [AST_skippeable]
  modificador = p[4]                            # AST_argumentos | [AST_skippeable]
  expresion = AST_funcion_incompleta(parametros, cuerpo)
  if isinstance(opt_tipo, AST_decorador_tipo):
    expresion = aplicarModificador(expresion, opt_tipo)
  else:
    parametros.clausura(opt_tipo)
  expresion.modificador_adicional(modificador)
  p[0] = expresion

def p_parametros(p): # AST_parametros
  '''
  parametros : ABRE_PAREN s identificadores_parametros CIERRA_PAREN s
  '''
  abre = AST_sintaxis(p[1])
  s1 = concatenar(abre, p[2])       # [AST_skippeable]
  lista = p[3]                      # [AST_identificador]
  cierra = AST_sintaxis(p[4])       # AST_sintaxis
  cierra = concatenar(cierra, p[5]) # [AST_skippeable]
  parametros = AST_parametros(lista)
  parametros.apertura(s1)
  parametros.clausura(cierra)
  p[0] = parametros

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

def p_identificadores_parametros_vacio(p): # [AST_identificador | AST_identificador_objeto]
  '''
  identificadores_parametros : vacio
  '''
  p[0] = []

def p_identificadores_parametros_no_vacio(p): # [AST_identificador | AST_identificador_objeto]
  '''
  identificadores_parametros : identificadores_parametros_no_vacio
  '''
  p[0] = p[1]

def p_identificadores_parametros_primer_identificador(p): # [AST_identificador | AST_identificador_objeto]
  '''
  identificadores_parametros_no_vacio : identificador_parametro opt_decorador_parametro mas_identificadores_parametros
  '''
  identificador = p[1]      # AST_identificador
  opt_mod = p[2]            # AST_decorador | [AST_skippeable]
  rec = p[3]                # [AST_identificador | AST_identificador_objeto] | [AST_skippeable]
  identificador = aplicarModificador(identificador, opt_mod)
  if len(rec) > 0 and isinstance(rec[0], AST_asignable):
    rec.insert(0, identificador)
  else:
    identificador.clausura(rec)
    rec = [identificador]
  p[0] = rec

def p_mas_identificadores_parametros_fin(p): # [AST_skippeable]
  '''
  mas_identificadores_parametros : vacio
  '''
  p[0] = []

def p_mas_identificadores_parametros(p): # [AST_identificador | AST_identificador_objeto] | [AST_skippeable]
  '''
  mas_identificadores_parametros : mas_identificadores_parametros_no_vacio
  '''
  p[0] = p[1]

def p_mas_identificadores_parametros_no_vacio(p): # [AST_identificador | AST_identificador_objeto] | [AST_skippeable]
  '''
  mas_identificadores_parametros_no_vacio : COMA s identificadores_parametros
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  rec = p[3]                  # [AST_identificador | AST_identificador_objeto] | [AST_skippeable]
  if len(rec) > 0 and isinstance(rec[0], AST_asignable):
    rec[0].apertura(s)
  else:
    rec = concatenar(s, rec)
  p[0] = rec

def p_identificador_parametro_objeto(p): # AST_identificador | AST_identificador_objeto
  '''
  identificador_parametro : ABRE_LLAVE s campos_parametro
  '''
  abre = AST_sintaxis(p[1])     # AST_sintaxis
  s = concatenar(abre, p[2])    # [AST_skippeable]
  campos = p[3]                 # AST_campos
  objeto = AST_identificador_objeto(campos)
  objeto.apertura(s)
  p[0] = objeto

def p_identificador_parametro_identificador(p): # AST_identificador | AST_identificador_objeto
  '''
  identificador_parametro : nombre_parametro s opt_mas_identificadores_o_modificadores_parametro
  '''  
  identificador = p[1]                      # AST_identificador
  s = p[2]                                  # [AST_skippeable]
  rec = p[3]                                # AST_identificador | AST_identificadores | AST_identificador_objeto | [AST_skippeable]
  identificador.clausura(s)
  if isinstance(rec, AST_asignable):
    decorador = AST_decorador_keyword(identificador)
    rec.agregar_decorador_pre(decorador)
    identificador = rec
  else:
    identificador.clausura(rec)
  p[0] = identificador

def p_nombre_parametro_con_prefijo(p): # AST_identificador
  '''
  nombre_parametro : operador_prefijo s nombre
  '''
  abre = AST_sintaxis(p[1])                 # AST_sintaxis
  s = concatenar(abre, p[2])                # [AST_skippeable]
  identificador = AST_identificador(p[3])   # AST_identificador
  identificador.apertura(s)
  p[0] = identificador

def p_nombre_parametro_sin_prefijo(p): # AST_identificador
  '''
  nombre_parametro : nombre
  '''
  p[0] = AST_identificador(p[1])

def p_mas_identificadores_o_modificadores_parametro_vacio(p): # [AST_skippeable]
  '''
  opt_mas_identificadores_o_modificadores_parametro : vacio
  '''
  p[0] = p[1]

def p_mas_identificadores_o_modificadores_parametro_no_vacio(p): # AST_identificador | AST_identificadores | AST_identificador_objeto
  '''
  opt_mas_identificadores_o_modificadores_parametro : identificador_parametro
  '''
  p[0] = p[1]

def p_campos_parametro_vacio(p): # AST_campos
  '''
  campos_parametro : fin_campos_parametro
  '''
  fin_campos = p[1]
  p[0] = fin_campos

def p_campos_parametro_no_vacio(p): # AST_campos
  '''
  campos_parametro : campo_parametro mas_campos_parametro
  '''
  campo = p[1]          # AST_campo
  campos = p[2]         # AST_campos
  campos.agregar_campo(campo)
  p[0] = campos

def p_mas_campos_parametro_fin(p): # AST_campos
  '''
  mas_campos_parametro : fin_campos_parametro
  '''
  fin_campos = p[1]
  p[0] = fin_campos

def p_mas_campos_parametro(p): # AST_campos
  '''
  mas_campos_parametro : COMA s campos_parametro
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  campos = p[3]               # AST_campos
  campos.apertura(s)
  p[0] = campos

def p_fin_campos_parametro(p): # AST_campos
  '''
  fin_campos_parametro : CIERRA_LLAVE
  '''
  s = AST_sintaxis(p[1])
  campos = AST_campos()
  campos.clausura(s)
  p[0] = campos

def p_campo_parametro(p): # AST_campo
  '''
  campo_parametro : clave_campo s opt_valor_campo_parametro
  '''
  clave = p[1]      # AST_identificador | AST_declaracion_funcion | ¿AST_invocacion? |AST_expresion_literal (string)
  s = p[2]          # [AST_skippeable]
  opt_valor = p[3]  # AST_expresion | [AST_skippeable]
  clave.clausura(s)
  if not isinstance(opt_valor, AST_expresion):
    clave.clausura(opt_valor)
    opt_valor = None
  campo = AST_campo(clave, opt_valor)
  p[0] = campo

def p_campo_parametro_con_valor(p): # AST_expresion
  '''
  opt_valor_campo_parametro : ASIGNACION1 s expresion
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # [AST_skippeable]
  valor = p[3]
  valor.apertura(s)
  p[0] = valor

def p_campo_parametro_sin_valor(p): # [AST_skippeable]
  '''
  opt_valor_campo_parametro : vacio
  '''
  p[0] = p[1]

def p_identificadores_vacio(p): # [AST_identificador]
  '''
  identificadores : vacio
  '''
  p[0] = []

def p_identificadores_no_vacio(p): # [AST_identificador]
  '''
  identificadores : identificadores_no_vacio
  '''
  p[0] = p[1]

def p_identificadores_con_prefijo(p): # [AST_identificador]
  '''
  identificadores_no_vacio : operador_prefijo s identificadores_no_vacio
                           | COMA s identificadores_no_vacio
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # [AST_skippeable]
  identificadores = p[3]    # [AST_identificador]
  identificadores[0].apertura(s)
  p[0] = identificadores

def p_identificadores_sin_prefijo(p): # [AST_identificador]
  '''
  identificadores_no_vacio : identificadores_sin_prefijo
  '''
  p[0] = p[1]

def p_identificadores_primer_identificador(p): # [AST_identificador]
  '''
  identificadores_sin_prefijo : identificador_con_modificadores_pre_sin_llaves opt_decorador_parametro mas_identificadores
  '''
  identificador = p[1]      # AST_identificador
  opt_mod = p[2]            # AST_decorador | [AST_skippeable]
  rec = p[3]                # [AST_identificador] | [AST_skippeable]
  identificador = aplicarModificador(identificador, opt_mod)
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
  mas_identificadores : mas_identificadores_no_vacio
  '''
  p[0] = p[1]

def p_mas_identificadores_no_vacio(p): # [AST_identificador] | [AST_skippeable]
  '''
  mas_identificadores_no_vacio : COMA s identificadores
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  rec = p[3]                  # [AST_identificador] | [AST_skippeable]
  if len(rec) > 0 and type(rec[0]) is AST_identificador:
    rec[0].apertura(s)
  else:
    rec = concatenar(s, rec)
  p[0] = rec

def p_decorador_opcional(p): # AST_decorador_opcional
  '''
  decorador_opcional : PREGUNTA s opt_decorador_tipo
                     | EXCLAMACION s opt_decorador_tipo
  '''
  s1 = AST_sintaxis(p[1])                   # AST_sintaxis
  s1 = concatenar(s1, p[2])                 # [AST_skippeable]
  opt_tipo = p[3]                           # AST_decorador_tipo | [AST_skippeable]
  decorador = AST_decorador_opcional()      # AST_decorador_opcional
  decorador.modificador_adicional(opt_tipo)
  decorador.apertura(s1)
  p[0] = decorador

def p_opt_is_si(p): # AST_decorador_tipo
  '''
  opt_is : IS s tipo
  '''
  s = AST_sintaxis(p[1])        # AST_sintaxis
  s = concatenar(s, p[2])       # [AST_skippeable]
  tipo = p[3]                   # AST_tipo
  tipo.apertura(s)
  p[0] = AST_decorador_tipo(tipo)

def p_opt_is_no(p): # AST_decorador_tipo
  '''
  opt_is : vacio
  '''
  p[0] = p[1]

def p_tipo_identificador(p): # AST_tipo
  '''
  tipo : IDENTIFICADOR opt_modificador_tipo
  '''
  identificador = AST_identificador(p[1]) # AST_identificador
  opt_modificador_tipo = p[2]             # AST_tipo_lista | AST_tipo_suma | AST_tipo_tupla | AST_modificador_objeto_acceso | [AST_skippeable]
  tipo = AST_tipo_base(identificador)     # AST_tipo_base
  tipo = aplicarModificador(tipo, opt_modificador_tipo)
  p[0] = tipo

def p_tipo_sin_identificador(p): # AST_tipo
  '''
  tipo : tipo_sin_id
  '''
  tipo = p[1]         # AST_identificador
  p[0] = tipo

def p_operador_acceso(p): # string
  '''
  operador_acceso : ACCESO1
                  | ACCESO2
  '''
  p[0] = p[1]

def p_nombre_no_type(p): # string
  '''
  nombre_no_type : IDENTIFICADOR
                 | FROM
                 | IN
  '''
  p[0] = p[1]

def p_nombre(p): # string
  '''
  nombre : TYPE
         | DECL_CLASS
         | CATCH
         | nombre_no_type
  '''
  p[0] = p[1]

def p_tipo_base(p): # AST_tipo_base
  '''
  tipo_sin_id : STRING opt_modificador_tipo
  '''
  tipo = AST_tipo_base(p[1])
  tipo = aplicarModificador(tipo, p[2])
  p[0] = tipo

def p_tipo_objeto(p): # AST_tipo_objeto
  '''
  tipo_sin_id : objeto_tipo
  '''
  p[0] = p[1]

def p_objeto_tipo(p): # AST_tipo_objeto
  '''
  objeto_tipo : ABRE_LLAVE s campos_tipo opt_modificador_tipo
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])              # [AST_skippeable]
  campos = p[3]                           # AST_campos_tipo
  opt_adicional = p[4]      # AST_tipo_lista | AST_tipo_suma | AST_tipo_tupla | AST_modificador_objeto_acceso | [AST_skippeable]
  tipo = AST_tipo_objeto(campos)
  tipo.apertura(s)
  tipo = aplicarModificador(tipo, opt_adicional)
  p[0] = tipo

def p_tipo_lista(p): # AST_tipo_varios
  '''
  tipo_sin_id : lista opt_modificador_tipo
  '''
  lista = p[1]              # AST_expresion_lista
  opt_adicional = p[2]      # AST_tipo_lista | AST_tipo_suma | AST_tipo_tupla | AST_modificador_objeto_acceso | [AST_skippeable]
  tipo = tipoDesdeNodo(lista)
  tipo = aplicarModificador(tipo, opt_adicional)
  p[0] = tipo

def p_tipo_parentesis(p): # AST_tipo (puede ser AST_tipo_flecha o un AST_tipo cualquiera entre paréntesis)
  '''
  tipo_sin_id : ABRE_PAREN s tipo_o_parametros opt_modificador_tipo
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # AST_skippeable
  rec = p[3]                # AST_tipo (puede ser AST_tipo_flecha o un AST_tipo cualquiera entre paréntesis)
  opt_adicional = p[4]      # AST_tipo_lista | AST_tipo_suma | AST_modificador_objeto_acceso | [AST_skippeable]
  rec.apertura(s)
  rec = aplicarModificador(rec, opt_adicional)
  p[0] = rec

def p_tipo_new(p): # AST_tipo
  '''
  tipo_sin_id : NEW s tipo
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # AST_skippeable
  rec = p[3]                # AST_tipo
  rec.apertura(s)
  p[0] = rec

def p_tipo_derivado(p): # AST_tipo_derivado
  '''
  tipo_sin_id : TYPEOF s IDENTIFICADOR opt_modificador_objeto_expresion
  '''
  s = AST_sintaxis(p[1])                                            # AST_sintaxis
  s = concatenar(s, p[2])                                           # AST_skippeable
  expresion = AST_expresion_identificador(AST_identificador(p[3]))  # AST_expresion
  modificador = p[4]
  expresion = aplicarModificador(expresion, modificador)
  tipo = AST_tipo_derivado(expresion)
  tipo.apertura(s)
  p[0] = tipo

def p_tipo_void(p): # AST_tipo_base
  '''
  tipo_sin_id : VOID
  '''
  s = AST_sintaxis(p[1])                                            # AST_sintaxis
  tipo = AST_tipo_void()
  tipo.apertura(s)
  p[0] = tipo

def p_tipo_suma(p): # AST_tipo_suma
  '''
  tipo_sin_id : tipo_con_pipe
  '''
  p[0] = p[1]

def p_tipo_producto(p): # AST_tipo_producto
  '''
  tipo_sin_id : tipo_con_and
  '''
  p[0] = p[1]

def p_tipo_o_parametros_tipo(p): # AST_tipo (entre paréntesis)
  '''
  tipo_o_parametros : tipo_sin_id opt_modificador_tipo CIERRA_PAREN
  '''
  tipo = p[1]               # AST_tipo
  opt_adicional = p[2]      # AST_tipo_lista | AST_tipo_suma | AST_tipo_tupla | AST_modificador_objeto_acceso | [AST_skippeable]
  s = AST_sintaxis(p[3])    # AST_sintaxis
  tipo.clausura(s)
  tipo = aplicarModificador(tipo, opt_adicional)
  p[0] = tipo

def p_tipo_o_parametros_flecha(p): # AST_tipo_flecha
  '''
  tipo_o_parametros : CIERRA_PAREN s FLECHA s tipo
  '''
  s = AST_sintaxis(p[1])            # AST_sintaxis
  s = concatenar(s, p[2])           # [AST_skippeable]
  s = concatenar(s, p[3])           # [AST_skippeable]
  s = concatenar(s, p[4])           # [AST_skippeable]
  tipo_salida = p[5]                # AST_identificador | AST_tipo_objeto | AST_tipo_flecha
  parametros = AST_parametros([])
  parametros.clausura(s)
  tipo_flecha = AST_tipo_flecha(parametros, tipo_salida)
  p[0] = tipo_flecha

def p_tipo_o_parametros_prefijo(p): # AST_tipo_flecha
  '''
  tipo_o_parametros : operador_prefijo s identificadores_no_vacio CIERRA_PAREN s FLECHA s tipo
  '''
  s1 = AST_sintaxis(p[1])     # AST_sintaxis
  s1 = concatenar(s1, p[2])   # [AST_skippeable]
  identificadores = p[3]      # [AST_identificador]
  identificadores[0].apertura(s1)
  s2 = AST_sintaxis(p[4])     # AST_sintaxis
  s2 = concatenar(s2, p[5])   # [AST_skippeable]
  parametros = AST_parametros(identificadores)
  parametros.clausura(s2)
  s3 = AST_sintaxis(p[6])     # AST_sintaxis
  s3 = concatenar(s3, p[7])   # [AST_skippeable]
  tipo_salida = p[8]          # AST_identificador | AST_tipo_objeto | AST_tipo_flecha
  parametros.clausura(s3)
  tipo_flecha = AST_tipo_flecha(parametros, tipo_salida)
  p[0] = tipo_flecha

def p_tipo_o_parametros_identificador(p): # AST_tipo (puede ser AST_tipo_flecha o un AST_tipo cualquiera entre paréntesis)
  '''
  tipo_o_parametros : IDENTIFICADOR s continuacion_identificador_para_tipo_o_parametros
  '''
  identificador = AST_identificador(p[1])   # AST_identificador
  s = p[2]                                  # [AST_skippeable]
  continuacion = p[3]                       # AST_tipo_flecha | AST_tipo_suma
  identificador.clausura(s)
  tipo = None
  if isinstance(continuacion, AST_tipo_flecha):
    tipo = continuacion
    tipo.primerParametro(identificador)
  elif isinstance(continuacion, AST_tipo_suma):
    tipo = aplicarModificador(AST_tipo_base(identificador), continuacion)
  else:
    # ERROR
    fallaDebug()
  p[0] = tipo

def p_continuacion_tipo_o_parametros_pipe(p): # AST_tipo_suma
  '''
  continuacion_identificador_para_tipo_o_parametros : tipo_con_pipe CIERRA_PAREN
  '''
  tipo = p[1]               # AST_tipo_suma
  s = AST_sintaxis(p[2])    # AST_sintaxis
  tipo.clausura(s)
  p[0] = tipo

def p_continuacion_tipo_o_parametros_coma(p): # AST_tipo_flecha
  '''
  continuacion_identificador_para_tipo_o_parametros : mas_identificadores_no_vacio CIERRA_PAREN s FLECHA s tipo
  '''
  lista = p[1]                      # [AST_identificador]
  cierra = AST_sintaxis(p[2])       # AST_sintaxis
  cierra = concatenar(cierra, p[3]) # [AST_skippeable]
  parametros = AST_parametros(lista)
  parametros.clausura(cierra)
  s = AST_sintaxis(p[4])            # AST_sintaxis
  s = concatenar(s, p[5])           # [AST_skippeable]
  tipo_salida = p[6]                # AST_identificador | AST_tipo_objeto | AST_tipo_flecha
  parametros.clausura(s)
  tipo_flecha = AST_tipo_flecha(parametros, tipo_salida)
  p[0] = tipo_flecha

def p_continuacion_tipo_o_parametros_dos_puntos(p): # AST_tipo_flecha
  '''
  continuacion_identificador_para_tipo_o_parametros : decorador_tipo s mas_identificadores CIERRA_PAREN s FLECHA s tipo
                                                    | decorador_opcional s mas_identificadores CIERRA_PAREN s FLECHA s tipo
  '''
  decorador = p[1]                  # AST_decorador_tipo
  s1 = p[2]                         # [AST_skippeable]
  decorador.clausura(s1)

  lista = p[3]                      # [AST_identificador] | [AST_skippeable]
  s2 = AST_sintaxis(p[4])           # AST_sintaxis
  s2 = concatenar(s2, p[5])         # [AST_skippeable]

  parametros = None
  if len(lista) > 0 and type(lista[0]) is AST_identificador:
    parametros = AST_parametros(lista)
    parametros.clausura(s2)
  else:
    parametros = AST_parametros([])
    decorador.clausura(lista)
    decorador.clausura(s2)

  s3 = AST_sintaxis(p[6])           # AST_sintaxis
  s3 = concatenar(s3, p[7])         # [AST_skippeable]
  tipo_salida = p[8]                # AST_identificador | AST_tipo_objeto | AST_tipo_flecha

  parametros.clausura(s3)
  parametros.agregar_decorador_parametro(decorador)
  tipo_flecha = AST_tipo_flecha(parametros, tipo_salida)
  p[0] = tipo_flecha

def p_campos_tipo_vacio(p): # AST_campos_tipo
  '''
  campos_tipo : fin_campos_tipo
  '''
  fin_campos = p[1]
  p[0] = fin_campos

def p_campos_tipo_no_vacio(p): # AST_campos_tipo
  '''
  campos_tipo : campo_tipo mas_campos_tipo
  '''
  campo = p[1]          # AST_campo_tipo
  campos = p[2]         # AST_campos_tipo
  campos.agregar_campo(campo)
  p[0] = campos

def p_mas_campos_tipo_fin(p): # AST_campos_tipo
  '''
  mas_campos_tipo : fin_campos_tipo
  '''
  fin_campos = p[1]
  p[0] = fin_campos

def p_mas_campos_tipo(p): # AST_campos_tipo
  '''
  mas_campos_tipo : separador campos_tipo
  '''
  separador = p[1]            # [AST_skippeable]
  campos = p[2]               # AST_campos_tipo
  campos.apertura(separador)
  p[0] = campos

def p_fin_campos_tipo(p): # AST_campos_tipo
  '''
  fin_campos_tipo : CIERRA_LLAVE
  '''
  s = AST_sintaxis(p[1])
  campos = AST_campos_tipo()
  campos.clausura(s)
  p[0] = campos

def p_campo_tipo(p): # AST_campo_tipo
  '''
  campo_tipo : clave_campo s opt_pregunta opt_decorador_tipo
  '''
  clave = p[1]              # AST_identificador | AST_expresion_literal (string)
  s = p[2]                  # [AST_skippeable]
  opt_pregunta = p[3]       # AST_decorador_opcional | [AST_skippeable]
  tipo = p[4]               # AST_decorador_tipo | [AST_skippeable]
  clave.clausura(s)
  if isinstance(opt_pregunta, AST_decorador_opcional):
    clave = aplicarModificador(clave, opt_pregunta)
  else:
    clave.clausura(opt_pregunta)
  if isinstance(tipo, AST_decorador_tipo):
    tipo_campo = tipo.tipo
    tipo_campo.imitarEspaciosYDecoradores(tipo)
    tipo = tipo_campo
  else:
    tipo_campo = clave
    clave = None
    tipo_campo.clausura(tipo)
    tipo = tipo_campo
  p[0] = AST_campo_tipo(clave, tipo)

def p_opt_pregunta_vacio(p):
  '''
  opt_pregunta : vacio
  '''
  p[0] = p[1]

def p_opt_pregunta_no_vacio(p):
  '''
  opt_pregunta : PREGUNTA s
  '''
  s = AST_sintaxis(p[1])
  s = concatenar(s, p[2])
  decorador = AST_decorador_opcional()
  decorador.apertura(s)
  p[0] = decorador

# DECLARACIÓN : VARIABLE (declaración de variable)
 #################################################################################################
def p_declaracion_var(p): # AST_declaracion_variable
  '''
  declaracion_no_objeto : declaracion_variable
  '''
  p[0] = p[1]

def p_declaracion_variable(p): # AST_declaracion_variable
  '''
  declaracion_variable : DECL_VAR sf identificador opt_modificador_variable
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])        # [AST_skippeable]
  identificador = p[3]                    # AST_identificador | AST_identificadores
  modificador_variable = p[4]             # AST_modificador_asignacion | AST_iterador | AST_modificador_variable_adicional | [AST_skippeable]
  decl_var = AST_declaracion_variable(identificador)
  decl_var.apertura(s)
  decl_var = aplicarModificador(decl_var, modificador_variable)
  p[0] = decl_var

def p_identificador_simple(p): # AST_identificador
  '''
  identificador : identificador_uno_con_type
  '''
  p[0] = p[1]

def p_identificador_no_type(p): # AST_identificador
  '''
  identificador : identificador_no_type
  '''
  p[0] = p[1]

def p_identificador_no_type_simple(p): # AST_identificador
  '''
  identificador_no_type : identificador_uno_no_type
  '''
  p[0] = p[1]

def p_identificador_uno(p): # AST_identificador
  '''
  identificador_uno_con_type : TYPE opt_decorador_tipo
  '''
  identificador = AST_identificador(p[1])       # AST_identificador
  opt_tipo = p[2]                               # AST_decorador_tipo | AST_decorador_subtipo | [AST_skippeable]
  identificador = aplicarModificador(identificador, opt_tipo)
  p[0] = identificador

def p_identificador_uno_no_type(p): # AST_identificador
  '''
  identificador_uno_no_type : nombre_no_type opt_decorador_tipo
  '''
  identificador = AST_identificador(p[1])       # AST_identificador
  opt_tipo = p[2]                               # AST_decorador_tipo | AST_decorador_subtipo | [AST_skippeable]
  identificador = aplicarModificador(identificador, opt_tipo)
  p[0] = identificador

def p_identificador_con_llaves(p): # AST_identificadores
  '''
  identificador_no_type : ABRE_LLAVE s identificadores_no_vacio CIERRA_LLAVE
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  lista = p[3]      # [AST_identificador]
  cierra = AST_sintaxis(p[4])
  identificadores = AST_identificadores(lista)
  identificadores.apertura(s)
  identificadores.clausura(cierra)
  p[0] = identificadores

def p_identificador_con_corchetes(p): # AST_identificadores
  '''
  identificador_no_type : ABRE_CORCHETE s identificadores_no_vacio CIERRA_CORCHETE
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  lista = p[3]      # [AST_identificador]
  cierra = AST_sintaxis(p[4])
  identificadores = AST_identificadores(lista)
  identificadores.apertura(s)
  identificadores.clausura(cierra)
  p[0] = identificadores

def p_mas_variables_vacio(p): # [AST_skippeable]
  '''
  opt_mas_variables : vacio
  '''
  p[0] = p[1]

def p_mas_variables_no_vacio(p): # AST_modificador_variable_adicional
  '''
  opt_mas_variables : mas_variables
  '''
  p[0] = p[1]

def p_mas_variables(p): # AST_modificador_variable_adicional
  '''
  mas_variables : COMA s identificador opt_modificador_variable
  '''
  s = AST_sintaxis(p[1])
  s = concatenar(s, p[2])
  identificador = p[3]                    # AST_identificador
  modificador_variable = p[4]             # AST_modificador_asignacion | AST_modificador_variable_adicional | [AST_skippeable]
  identificador.apertura(s)
  modificador = AST_modificador_variable_adicional(identificador)
  modificador.modificador_adicional(modificador_variable)
  p[0] = modificador

# DECLARACIÓN : IDENTIFICADOR (asignación, invocación, acceso o indexación)
 #################################################################################################
def p_declaracion_id(p): # AST_invocacion | AST_asignacion | AST_identificador | AST_expresion_acceso | AST_expresion_index
  '''
  declaracion_no_objeto : identificador_con_modificadores_pre_sin_llaves opt_modificador_asignable
  '''
  identificador = p[1]      # AST_identificador | AST_identificadores
  modificador = p[2]        # AST_argumentos | AST_modificador_asignacion | AST_modificador_objeto | AST_modificador_operador | [AST_skippeable]
  identificador = aplicarModificador(identificador, modificador)
  p[0] = identificador

def p_continuacion_abre_corchete_expresion(p): # AST_modificador_objeto_index
  '''
  continuacion_abre_corchete : expresion CIERRA_CORCHETE opt_modificador_asignable
  '''
  indice = p[1]               # AST_expresion
  cierra = AST_sintaxis(p[2]) # AST_sintaxis
  opt_adicional = p[3]        # [AST_skippeable] | AST_modificador_objeto
  modificador = AST_modificador_objeto_index(indice)
  modificador.clausura(cierra)
  modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_continuacion_abre_corchete_tipo(p): # AST_tipo_lista
  '''
  continuacion_abre_corchete : CIERRA_CORCHETE opt_modificador_asignable
  '''
  cierra = AST_sintaxis(p[1]) # AST_sintaxis
  opt_adicional = p[2]        # AST_tipo_lista | AST_tipo_suma | AST_modificador_objeto_acceso | [AST_skippeable]
  lista = AST_tipo_lista()
  lista.clausura(cierra)
  lista.modificador_adicional(opt_adicional)
  p[0] = lista

def p_simbolo_asignacion(p): # string
  '''
  simbolo_asignacion : ASIGNACION1
                     | ASIGNACION2
  '''
  p[0] = p[1]

def p_expresion_asignada_sin_pre(p): # AST_expresion
  '''
  expresion_asignada : expresion_asignada_sin_pre
  '''
  expresion = p[1]
  p[0] = expresion

def p_expresion_asignada_con_pre(p): # AST_expresion
  '''
  expresion_asignada : operador_prefijo s expresion_asignada
  '''
  operador = p[1]                 # string
  s = AST_sintaxis(operador)      # AST_sintaxis
  s = concatenar(s, p[2])         # [AST_skippeable]
  expresion = p[3]                # AST_expresion
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    expresion.izq = AST_operador(None, operador, expresion.izq)
  else:
    expresion = AST_operador(None, operador, expresion)
  expresion.apertura(s)
  p[0] = expresion

def p_expresion_asignada_literal(p): # AST_expresion_literal | # AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_asignada_sin_pre : literal opt_modificador_expresion_asignada
  '''
  literal = p[1]                        # AST_expresion_literal
  modificador_expresion = p[2]          # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(literal, modificador_expresion)

def p_expresion_asignada_format_string(p): # AST_format_string | AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_asignada_sin_pre : format_string opt_modificador_expresion_asignada
  '''
  format_string = p[1]              # AST_format_string
  modificador_expresion = p[2]      # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(format_string, modificador_expresion)

def p_expresion_asignada_identificador(p): # AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_asignada_sin_pre : nombre opt_modificador_expresion_asignada
  '''
  identificador = AST_identificador(p[1])
  modificador_expresion = p[2]      # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  expresion_base = AST_expresion_identificador(identificador)
  p[0] = aplicarModificador(expresion_base, modificador_expresion)

def p_expresion_asignada_funcion(p): # AST_expresion_funcion | AST_invocacion
  '''
  expresion_asignada_sin_pre : DECL_FUNC s definicion_funcion
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])      # [AST_skippeable]
  rec = p[3]                            # AST_funcion_incompleta | AST_invocacion
  rec.apertura(s)
  if type(rec) is AST_funcion_incompleta:
    rec = crearExpresionFuncion(rec)
  p[0] = rec

def p_expresion_asignada_new(p): # AST_expresion
  '''
  expresion_asignada_sin_pre : NEW s expresion_o_acceso_para_clase opt_modificador_expresion_asignada
  '''
  new = p[1]                                # string
  s = p[2]                                  # [AST_skippeable]
  tipo = p[3]                               # AST_tipo | AST_modificador_objeto_acceso
  opt_adicional = p[4]                      # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  expresion = tipo
  if isinstance(tipo, AST_modificador_objeto_acceso):
    new = AST_identificador(new)
    new.clausura(s)
    expresion = aplicarModificador(new, tipo)
  else:
    s = concatenar(AST_sintaxis(new), s)
    expresion = AST_expresion_new(tipo)
    expresion.apertura(s)
  p[0] = aplicarModificador(expresion, opt_adicional)

def p_expresion_o_acceso_expresion(p): # AST_tipo
  '''
  expresion_o_acceso_para_clase : nombre_clase
  '''
  p[0] = p[1]

def p_expresion_o_acceso_acceso(p): # AST_modificador_objeto_acceso
  '''
  expresion_o_acceso_para_clase : operador_acceso s nombre
  '''
  punto = AST_sintaxis(p[1])
  s = concatenar(punto, p[2])       # [AST_skippeable]
  campo = AST_identificador(p[3])   # AST_identificador
  modificador = AST_modificador_objeto_acceso(campo)
  modificador.apertura(s)
  p[0] = modificador

def p_id_clase(p): # AST_tipo_base | AST_tipo_compuesto
  '''
  id_clase : IDENTIFICADOR opt_modificador_id_clase
  '''
  identificador = AST_identificador(p[1])
  modificador = p[2]
  clase = AST_tipo_base(identificador)
  p[0] = aplicarModificador(clase, modificador)

def p_nombre_clase_id(p): # AST_tipo_base | AST_tipo_compuesto
  '''
  nombre_clase : IDENTIFICADOR opt_modificador_id_clase
  '''
  identificador = AST_identificador(p[1])   # AST_identificador
  modificador = p[2]                        # AST_tipo_tupla | [AST_skippeable]
  clase = AST_tipo_base(identificador)
  p[0] = aplicarModificador(clase, modificador)

def p_nombre_clase_parentesis(p): # AST_tipo
  '''
  nombre_clase : ABRE_PAREN s expresion CIERRA_PAREN
  '''
  abre = AST_sintaxis(p[1])     # AST_sintaxis
  abre = concatenar(abre, p[2]) # [AST_skippeable]
  expresion = p[3]              # AST_expresion
  cierra = AST_sintaxis(p[4])   # AST_sintaxis
  expresion.apertura(abre)
  expresion.clausura(cierra)
  tipo = AST_tipo_base(expresion)
  p[0] = tipo

def p_expresion_asignada_typeof(p): # AST_expresion
  '''
  expresion_asignada_sin_pre : TYPEOF s expresion opt_modificador_expresion_asignada
  '''
  s = AST_sintaxis(p[1])                    # AST_sintaxis
  s = concatenar(s, p[2])                   # [AST_skippeable]
  clase = p[3]                              # AST_expresion
  opt_adicional = p[4]                      # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  clase.apertura(s)
  p[0] = aplicarModificador(clase, opt_adicional)

def p_expresion_asignada_objeto(p): # AST_expresion_objeto
  '''
  expresion_asignada_sin_pre : objeto
  '''
  objeto = p[1]
  p[0] = objeto

def p_expresion_asignada_lista(p): # AST_expresion_lista
  '''
  expresion_asignada_sin_pre : lista opt_modificador_objeto_expresion
  '''
  lista = p[1]            # AST_expresion_lista
  modificador = p[2]      # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_decorador_comotipo | [AST_skippeable]
  lista = aplicarModificador(lista, modificador)
  p[0] = lista

def p_expresion_asignada_parentesis(p): # AST_expresion
  '''
  expresion_asignada_sin_pre : expresion_asignada_entre_parentesis
  '''
  expresion = p[1] # AST_expresion
  p[0] = p[1]

def p_expresion_asignada_entre_parentesis(p): # AST_expresion
  '''
  expresion_asignada_entre_parentesis : ABRE_PAREN s expresion_o_parametros CIERRA_PAREN opt_modificador_expresion_asignada
  '''
  abre = AST_sintaxis(p[1])         # AST_sintaxis
  abre = concatenar(abre, p[2])     # [AST_skippeable]
  expresion = p[3]                  # AST_identificador | AST_parametros | AST_expresion
  cierra = AST_sintaxis(p[4])       # AST_sintaxis
  modificador_expresion = p[5]      # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  if isinstance(expresion, AST_operador):
    expresion.conParentesis()
  expresion.apertura(abre)
  expresion.clausura(cierra)
  p[0] = aplicarModificador(expresion, modificador_expresion)

def p_expresion_o_parametros_objeto(p): # AST_expresion_objeto
  '''
  expresion_o_parametros : objeto
  '''
  expresion = p[1]          # AST_expresion_objeto
  p[0] = expresion

def p_expresion_o_parametros_con_prefijo(p): # AST_expresion
  '''
  expresion_o_parametros : operador_prefijo s expresion_no_obj
  '''
  operador = p[1]                 # string
  s = AST_sintaxis(operador)      # AST_sintaxis
  s = concatenar(s, p[2])         # [AST_skippeable]
  expresion = p[3]                # AST_expresion
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    expresion.izq = AST_operador(None, operador, expresion.izq)
  else:
    expresion = AST_operador(None, operador, expresion)
  expresion.apertura(s)
  p[0] = expresion

def p_expresion_o_parametros_identificador(p): # AST_identificador | AST_parametros
  '''
  expresion_o_parametros : nombre s opt_continuacion_expresion_o_parametros
  '''
  identificador = AST_identificador(p[1])   # AST_identificador
  s = p[2]
  continuacion = p[3]                       # AST_parametros | [AST_skippeable] | AST_decorador (con [AST_identificador] en adicional) | AST_modificador
  identificador.clausura(s)
  resultado = identificador
  if isinstance(continuacion, AST_parametros):
    resultado = continuacion
    resultado.primerParametro(identificador)
  elif isinstance(continuacion, AST_decorador):
    opt_adicional = continuacion.adicional
    continuacion.adicional = []
    resultado = aplicarModificador(resultado, continuacion)
    if len(opt_adicional) == 1: # tiene que ser [AST_identificador]
      lista = opt_adicional[0]
      lista.insert(0, resultado)
      resultado = AST_parametros(lista)
  elif isinstance(continuacion, AST_modificador):
    resultado = aplicarModificador(resultado, continuacion)
  else:
    resultado.clausura(continuacion)
  p[0] = resultado

def p_expresion_o_parametros_expresion_suelta(p): # AST_expresion
  '''
  expresion_o_parametros : expresion_suelta
                         | declaracion_de_funcion
  '''
  p[0] = p[1]

def p_expresion_o_parametros_vacio(p): # AST_parametros
  '''
  expresion_o_parametros : vacio
  '''
  p[0] = AST_parametros([])

def p_opt_continuacion_expresion_o_parametros_vacio(p): # [AST_skippeable]
  '''
  opt_continuacion_expresion_o_parametros : vacio
  '''
  p[0] = p[1]

def p_opt_continuacion_expresion_o_parametros_parametros(p): # AST_parametros
  '''
  opt_continuacion_expresion_o_parametros : COMA s identificadores
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  lista = p[3]                # [AST_identificador] | [AST_skippeable]
  abre = []
  parametros = None
  if len(lista) > 0 and type(lista[0]) is AST_identificador:
    lista[0].apertura(s)
  else:
    abre = concatenar(s, lista)
    lista = []
  parametros = AST_parametros(lista)
  parametros.apertura(abre)
  p[0] = parametros

def p_opt_continuacion_expresion_o_parametros_decorador(p): # AST_decorador (que puede venir con una lista de AST_identificador como adicional)
  '''
  opt_continuacion_expresion_o_parametros : decorador_tipo mas_identificadores
  '''
  decorador = p[1]                        # AST_decorador_tipo
  rec = p[2]                              # [AST_identificador] | [AST_skippeable]
  if len(rec) > 0 and type(rec[0]) is AST_identificador:
    decorador.modificador_adicional(rec)
  else:
    decorador.clausura(rec)
  p[0] = decorador

def p_opt_continuacion_expresion_o_parametros_otros(p): # AST_modificador
  '''
  opt_continuacion_expresion_o_parametros : modificador_asignable
  '''
  p[0] = p[1]

def p_cuerpo_abstraccion_expresion(p): # AST_cuerpo
  '''
  cuerpo_abstraccion : expresion_no_obj
  '''
  p[0] = AST_cuerpo([p[1]])

def p_cuerpo_abstraccion_expresion_con_void(p): # AST_cuerpo | AST_tipo_void
  '''
  cuerpo_abstraccion : VOID s opt_expresion
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # [AST_skippeable]
  expresion = p[3]          # AST_expresion | [AST_skippeable]
  resultado = expresion
  if isinstance(expresion, AST_expresion):
    expresion.apertura(s)
    resultado = AST_cuerpo([expresion])
  else:
    resultado = AST_tipo_void()
    resultado.apertura(s)
    resultado.clausura(expresion)
  p[0] = resultado

def p_cuerpo_abstraccion_cuerpo(p): # AST_cuerpo
  '''
  cuerpo_abstraccion : cuerpo
  '''
  p[0] = p[1]

def p_modificador_objeto_expresion_no_tipada_acceso(p): # AST_modificador_objeto_acceso
  '''
  modificador_objeto_expresion_no_tipada : operador_acceso s nombre opt_modificador_asignable_no_tipado
  '''
  punto = AST_sintaxis(p[1])
  s = concatenar(punto, p[2])       # [AST_skippeable]
  campo = AST_identificador(p[3])   # AST_identificador
  opt_adicional = p[4]              # [AST_skippeable] | AST_modificador_objeto
  modificador = AST_modificador_objeto_acceso(campo)
  modificador.apertura(s)
  modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_modificador_objeto_expresion_no_tipada_index(p): # AST_modificador_objeto_index | AST_tipo_lista
  '''
  modificador_objeto_expresion_no_tipada : ABRE_CORCHETE s continuacion_abre_corchete_no_tipada
  '''
  abre = AST_sintaxis(p[1])   # AST_sintaxis
  s = concatenar(abre, p[2])  # [AST_skippeable]
  rec = p[3]                  # AST_modificador_objeto_index | AST_tipo_lista
  rec.apertura(s)
  p[0] = rec

def p_continuacion_abre_corchete_expresion_no_tipada(p): # AST_modificador_objeto_index
  '''
  continuacion_abre_corchete_no_tipada : expresion CIERRA_CORCHETE opt_modificador_asignable_no_tipado
  '''
  indice = p[1]               # AST_expresion
  cierra = AST_sintaxis(p[2]) # AST_sintaxis
  opt_adicional = p[3]        # [AST_skippeable] | AST_modificador_objeto
  modificador = AST_modificador_objeto_index(indice)
  modificador.clausura(cierra)
  modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_continuacion_abre_corchete_no_tipada_tipo(p): # AST_tipo_lista
  '''
  continuacion_abre_corchete_no_tipada : CIERRA_CORCHETE opt_modificador_asignable_no_tipado
  '''
  cierra = AST_sintaxis(p[1]) # AST_sintaxis
  opt_adicional = p[2]        # AST_tipo_lista | AST_tipo_suma | AST_modificador_objeto_acceso | [AST_skippeable]
  lista = AST_tipo_lista()
  lista.clausura(cierra)
  lista.modificador_adicional(opt_adicional)
  p[0] = lista

def p_modificador_objeto_no_tipada_comotipo(p): # AST_decorador_comotipo
  '''
  modificador_objeto_expresion_no_tipada : comotipo
  '''
  modificador = p[1]        # AST_decorador_comotipo
  p[0] = modificador

## -- EXPRESIONES --

def p_expresion_invocacion(p): # AST_expresion
  '''
  expresion : expresion_sin_invocacion s opt_invocacion
  '''
  expresion = p[1]          # AST_expresion
  s = p[2]                  # [AST_skippeable]
  opt_invocacion = p[3]     # AST_argumentos | [AST_skippeable]
  expresion.clausura(s)
  p[0] = aplicarModificador(expresion, opt_invocacion)

def p_opt_invocacion_si(p): # AST_argumentos
  '''
  opt_invocacion : invocacion
  '''
  p[0] = p[1]

def p_opt_invocacion_no(p): # [AST_skippeable]
  '''
  opt_invocacion : vacio
  '''
  p[0] = p[1]

def p_expresion_objeto(p): # AST_expresion_objeto
  '''
  expresion_sin_invocacion : objeto
  '''
  objeto = p[1]
  p[0] = objeto

def p_expresion_no_objeto(p): # AST_expresion
  '''
  expresion_sin_invocacion : expresion_no_obj
  '''
  expresion = p[1]
  p[0] = expresion

def p_expresion_sin_pre(p): # AST_expresion
  '''
  expresion_no_obj : expresion_sin_pre
  '''
  expresion = p[1]
  p[0] = expresion

def p_expresion_con_pre(p): # AST_expresion
  '''
  expresion_no_obj : operador_prefijo s expresion_no_obj
  '''
  operador = p[1]                 # string
  s = AST_sintaxis(operador)      # AST_sintaxis
  s = concatenar(s, p[2])         # [AST_skippeable]
  expresion = p[3]                # AST_expresion
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    expresion.izq = AST_operador(None, operador, expresion.izq)
  else:
    expresion = AST_operador(None, operador, expresion)
  expresion.apertura(s)
  p[0] = expresion

def p_expresion_identificador(p): # AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_sin_pre : nombre opt_decorador_tipo opt_modificador_asignable
  '''
  identificador = AST_identificador(p[1])   # AST_identificador
  opt_tipo = p[2]                           # AST_decorador_tipo | AST_decorador_subtipo | [AST_skippeable]
  modificador_expresion = p[3]              # AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  identificador = aplicarModificador(identificador, opt_tipo)
  expresion_base = AST_expresion_identificador(identificador)
  expresion = aplicarModificador(expresion_base, modificador_expresion)
  p[0] = expresion

def p_expresion_sin_identificador(p): # AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_sin_pre : expresion_sin_pre_ni_id
  '''
  expresion = p[1]
  p[0] = expresion

def p_expresion_function(p): # AST_expresion_funcion | AST_invocacion
  '''
  expresion_sin_pre_ni_id : DECL_FUNC s definicion_funcion
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])      # [AST_skippeable]
  rec = p[3]                            # AST_funcion_incompleta | AST_invocacion
  rec.apertura(s)
  if type(rec) is AST_funcion_incompleta:
    rec = crearExpresionFuncion(rec)
  p[0] = rec

def p_expresion_suelta(p): # ...
  '''
  expresion_sin_pre_ni_id : expresion_suelta
  '''
  p[0] = p[1]

def p_expresion_no_tipada_function(p): # AST_expresion_funcion | AST_invocacion
  '''
  expresion_sin_pre_ni_id_no_tipada : DECL_FUNC s definicion_funcion
  '''
  declarador = AST_sintaxis(p[1])
  s = concatenar(declarador, p[2])      # [AST_skippeable]
  rec = p[3]                            # AST_funcion_incompleta | AST_invocacion
  rec.apertura(s)
  if type(rec) is AST_funcion_incompleta:
    rec = crearExpresionFuncion(rec)
  p[0] = rec

def p_expresion_no_tipada_suelta(p): # ...
  '''
  expresion_sin_pre_ni_id_no_tipada : expresion_suelta_no_tipada
  '''
  p[0] = p[1]

def p_expresion_suelta_con_modificador(p): # AST_expresion
  '''
  expresion_suelta : expresion_atomo opt_modificador_expresion
  '''
  expresion = p[1]          # AST_expresion
  modificador = p[2]        # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(expresion, modificador)

def p_expresion_suelta_no_tipada_con_modificador(p): # AST_expresion
  '''
  expresion_suelta_no_tipada : expresion_atomo opt_modificador_expresion_no_tipada
  '''
  expresion = p[1]          # AST_expresion
  modificador = p[2]        # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  p[0] = aplicarModificador(expresion, modificador)

def p_expresion_literal(p): # AST_expresion_literal
  '''
  expresion_atomo : literal
  '''
  literal =p[1]
  p[0] = literal

def p_literal(p): # AST_expresion_literal
  '''
  literal : NUMERO
          | STRING
          | RE
  '''
  literal = AST_expresion_literal(p[1]) # AST_expresion_literal
  p[0] = literal

def p_expresion_format_string(p): # AST_format_string | AST_expresion (_invocacion, _acceso, _index, ...)
  '''
  expresion_atomo : format_string
  '''
  format_string = p[1]              # AST_format_string
  p[0] = format_string

def p_format_string_empty(p): # AST_format_string
  '''
  format_string : FORMAT_STRING_COMPLETE
  '''
  p[0] = AST_format_string(p[1])

def p_expresion_new(p): # AST_expresion
  '''
  expresion_atomo : NEW s expresion_o_acceso_para_clase
  '''
  new = p[1]                                # string
  s = p[2]                                  # [AST_skippeable]
  tipo = p[3]                               # AST_tipo | AST_modificador_objeto_acceso
  expresion = tipo
  if isinstance(tipo, AST_modificador_objeto_acceso):
    new = AST_identificador(new)
    new.clausura(s)
    expresion = aplicarModificador(new, tipo)
  else:
    s = concatenar(AST_sintaxis(new), s)
    expresion = AST_expresion_new(tipo)
    expresion.apertura(s)
  p[0] = expresion

def p_expresion_typeof(p): # AST_expresion
  '''
  expresion_suelta : TYPEOF s expresion opt_modificador_expresion
  '''
  s = AST_sintaxis(p[1])                    # AST_sintaxis
  s = concatenar(s, p[2])                   # [AST_skippeable]
  clase = p[3]                              # AST_expresion
  opt_adicional = p[4]                      # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  clase.apertura(s)
  p[0] = aplicarModificador(clase, opt_adicional)

def p_expresion_no_tipada_typeof(p): # AST_expresion
  '''
  expresion_suelta_no_tipada : TYPEOF s expresion_no_tipada opt_modificador_expresion_no_tipada
  '''
  s = AST_sintaxis(p[1])                    # AST_sintaxis
  s = concatenar(s, p[2])                   # [AST_skippeable]
  clase = p[3]                              # AST_expresion
  opt_adicional = p[4]                      # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  clase.apertura(s)
  p[0] = aplicarModificador(clase, opt_adicional)

def p_expresion_lista(p): # AST_expresion_lista
  '''
  expresion_atomo : lista
  '''
  lista = p[1]            # AST_expresion_lista
  p[0] = lista

def p_expresion_parentesis(p): # AST_expresion
  '''
  expresion_atomo : expresion_entre_parentesis
  '''
  expresion = p[1] # AST_expresion
  p[0] = p[1]

def p_expresion_entre_parentesis(p): # AST_expresion
  '''
  expresion_entre_parentesis : ABRE_PAREN s expresion_o_parametros CIERRA_PAREN
  '''
  abre = AST_sintaxis(p[1])         # AST_sintaxis
  abre = concatenar(abre, p[2])     # [AST_skippeable]
  expresion = p[3]                  # AST_identificador | AST_parametros | AST_expresion
  cierra = AST_sintaxis(p[4])       # AST_sintaxis
  if isinstance(expresion, AST_operador):
    expresion.conParentesis()
  expresion.apertura(abre)
  expresion.clausura(cierra)
  p[0] = expresion

def p_expresion_no_tipada_objeto(p):
  '''
  expresion_no_tipada : objeto
  '''
  p[0] = p[1]

def p_expresion_no_tipada_con_pre(p):
  '''
  expresion_no_tipada : operador_prefijo s expresion_no_tipada
  '''
  operador = p[1]                 # string
  s = AST_sintaxis(operador)      # AST_sintaxis
  s = concatenar(s, p[2])         # [AST_skippeable]
  expresion = p[3]                # AST_expresion
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    expresion.izq = AST_operador(None, operador, expresion.izq)
  else:
    expresion = AST_operador(None, operador, expresion)
  expresion.apertura(s)
  p[0] = expresion

def p_expresion_no_tipada_id(p):
  '''
  expresion_no_tipada : IDENTIFICADOR opt_modificador_expresion_no_tipada
  '''
  identificador = AST_identificador(p[1])   # AST_identificador
  modificador_expresion = p[2]              # AST_cuerpo | AST_tipo_void | AST_argumentos | AST_expresion | AST_modificador_objeto | [AST_skippeable]
  expresion_base = AST_expresion_identificador(identificador)
  expresion = aplicarModificador(expresion_base, modificador_expresion)
  p[0] = expresion

def p_expresion_no_tipada_otros(p):
  '''
  expresion_no_tipada : expresion_sin_pre_ni_id_no_tipada
  '''
  p[0] = p[1]

def p_operador_no_tipado_operador_binario(p): # AST_modificador_operador_binario
  '''
  operador_no_tipado : operador_binario s expresion_no_tipada
  '''
  clase = p[1]                # string
  s = AST_sintaxis(clase)     # AST_sintaxis
  s = concatenar(s, p[2])     # AST_skippeable
  expresion = p[3]            # AST_expresion
  expresion.apertura(s)
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    modificador = AST_modificador_operador_binario(clase, expresion.izq)
    modificador.modificador_adicional(AST_modificador_operador_binario(expresion.op, expresion.der))
  else:
    modificador = AST_modificador_operador_binario(clase, expresion)
  p[0] = modificador

def p_operador_no_tipado_operador_ternario(p): # AST_modificador_operador_ternario
  '''
  operador_no_tipado : PREGUNTA s expresion_no_tipada DOS_PUNTOS s expresion_no_tipada
  '''
  s1 = AST_sintaxis(p[1])     # AST_sintaxis
  s1 = concatenar(s1, p[2])   # [AST_skippeable]
  e1 = p[3]                   # AST_expresion
  s2 = AST_sintaxis(p[4])     # AST_sintaxis
  s2 = concatenar(s2, p[5])   # [AST_skippeable]
  e2 = p[6]                   # AST_expresion
  e1.apertura(s1)
  e2.apertura(s2)
  p[0] = AST_modificador_operador_ternario(e1,e2)

def p_operador_no_tipado_operador_posfijo(p): # AST_modificador_operador_posfijo
  '''
  operador_no_tipado : operador_posfijo opt_modificador_expresion_no_tipada
  '''
  operador = p[1]
  opt_adicional = p[2]
  modificador = AST_modificador_operador_posfijo(operador)
  modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_operador_operador_binario(p): # AST_modificador_operador_binario
  '''
  operador : operador_binario s expresion
  '''
  clase = p[1]                # string
  s = AST_sintaxis(clase)     # AST_sintaxis
  s = concatenar(s, p[2])     # AST_skippeable
  expresion = p[3]            # AST_expresion
  expresion.apertura(s)
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    modificador = AST_modificador_operador_binario(clase, expresion.izq)
    modificador.modificador_adicional(AST_modificador_operador_binario(expresion.op, expresion.der))
  else:
    modificador = AST_modificador_operador_binario(clase, expresion)
  p[0] = modificador

def p_operador_operador_ternario(p): # AST_modificador_operador_ternario
  '''
  operador : PREGUNTA s expresion_no_tipada DOS_PUNTOS s expresion
  '''
  s1 = AST_sintaxis(p[1])     # AST_sintaxis
  s1 = concatenar(s1, p[2])   # [AST_skippeable]
  e1 = p[3]                   # AST_expresion
  s2 = AST_sintaxis(p[4])     # AST_sintaxis
  s2 = concatenar(s2, p[5])   # [AST_skippeable]
  e2 = p[6]                   # AST_expresion
  e1.apertura(s1)
  e2.apertura(s2)
  p[0] = AST_modificador_operador_ternario(e1,e2)

def p_operador_binario(p): # string
  '''
  operador_binario : OPERADOR_BOOLEANO
                   | MAS
                   | POR
                   | DIV
                   | MENOS
                   | MENOR
                   | MAYOR
                   | shift
                   | AND
                   | PIPE
                   | IN
  '''
  operador = p[1]
  p[0] = operador

def p_shift(p): # string
  '''
  shift : MENOR MENOR
        | MAYOR MAYOR
  '''
  p[0] = p[1] + p[2]

def p_iterador(p): # string
  '''
  iterador : IN
           | OF
  '''
  p[0] = p[1]

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
                   | OPERADOR_PREFIJO
                   | EXCLAMACION
  '''
  operador = p[1]
  p[0] = operador

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
  argumentos.apertura(s)
  p[0] = argumentos

def p_fin_argumentos(p): # AST_argumentos
  '''
  fin_argumentos : CIERRA_PAREN opt_modificador_expresion
  '''
  s = AST_sintaxis(p[1])
  opt_adicional = p[2]        # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_decorador_comotipo | [AST_skippeable]
  argumentos = AST_argumentos()
  argumentos.clausura(s)
  argumentos.modificador_adicional(opt_adicional)
  p[0] = argumentos

def p_argumentos_no_tipados_vacio(p): # AST_argumentos
  '''
  argumentos_no_tipados : fin_argumentos_no_tipados
  '''
  fin_argumentos = p[1]
  p[0] = fin_argumentos

def p_argumentos_no_tipados_no_vacio(p): # AST_argumentos
  '''
  argumentos_no_tipados : expresion mas_argumentos_no_tipados
  '''
  expresion = p[1]          # AST_expresion
  argumentos = p[2]         # AST_argumentos
  argumentos.agregar_argumento(expresion)
  p[0] = argumentos

def p_mas_argumentos_no_tipados_fin(p): # AST_argumentos
  '''
  mas_argumentos_no_tipados : fin_argumentos_no_tipados
  '''
  fin_argumentos = p[1]
  p[0] = fin_argumentos

def p_mas_argumentos_no_tipados(p): # AST_argumentos
  '''
  mas_argumentos_no_tipados : COMA s argumentos_no_tipados
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  argumentos = p[3]           # AST_argumentos
  argumentos.apertura(s)
  p[0] = argumentos

def p_fin_argumentos_no_tipados(p): # AST_argumentos
  '''
  fin_argumentos_no_tipados : CIERRA_PAREN opt_modificador_expresion_no_tipada
  '''
  s = AST_sintaxis(p[1])
  opt_adicional = p[2]        # AST_argumentos | AST_modificador_operador | AST_modificador_objeto | AST_decorador_comotipo | [AST_skippeable]
  argumentos = AST_argumentos()
  argumentos.clausura(s)
  argumentos.modificador_adicional(opt_adicional)
  p[0] = argumentos

# DECLARACIÓN : OBJETO (no es asignable pero se vuelve asignable al accederlo o indexarlo)
 #################################################################################################
def p_declaracion_objeto(p): # AST_tipo_objeto
  '''
  declaracion : ABRE_LLAVE s campos_tipo
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])              # [AST_skippeable]
  campos = p[3]                           # AST_campos_tipo
  objeto = AST_tipo_objeto(campos)
  objeto.apertura(s)
  p[0] = objeto

def p_objeto_literal(p): # AST_expresion_objeto
  '''
  objeto : ABRE_LLAVE s campos opt_modificador_objeto_expresion
  '''
  abre = AST_sintaxis(p[1])     # AST_sintaxis
  s = concatenar(abre, p[2])    # [AST_skippeable]
  campos = p[3]                 # AST_campos
  modificador = p[4]            # [AST_skippeable] | AST_modificador_objeto | AST_argumentos
  objeto = AST_expresion_objeto(campos)
  objeto.apertura(s)
  p[0] = aplicarModificador(objeto, modificador)

def p_lista_literal(p): # AST_expresion_lista
  '''
  lista : ABRE_CORCHETE s elementos
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])              # [AST_skippeable]
  elementos = p[3]                        # AST_elementos
  modificadores = elementos.adicional     # [AST_modificador]
  elementos.adicional = []
  lista = AST_expresion_lista(elementos)
  lista.apertura(s)
  for m in modificadores:
    lista = aplicarModificador(lista, m)
  p[0] = lista

def p_elementos_vacio(p): # AST_elementos
  '''
  elementos : fin_elementos
  '''
  fin_elementos = p[1]
  p[0] = fin_elementos

def p_elementos_no_vacio(p): # AST_elementos
  '''
  elementos : expresion mas_elementos
  '''
  expresion = p[1]          # AST_expresion
  elementos = p[2]          # AST_elementos
  elementos.agregar_elemento(expresion)
  p[0] = elementos

def p_mas_elementos_fin(p): # AST_elementos
  '''
  mas_elementos : fin_elementos
  '''
  fin_elementos = p[1]
  p[0] = fin_elementos

def p_mas_elementos(p): # AST_elementos
  '''
  mas_elementos : COMA s elementos
  '''
  coma = AST_sintaxis(p[1])
  s = concatenar(coma, p[2])  # [AST_skippeable]
  elementos = p[3]           # AST_elementos
  elementos.apertura(s)
  p[0] = elementos

def p_fin_elementos(p): # AST_elementos
  '''
  fin_elementos : CIERRA_CORCHETE
  '''
  s = AST_sintaxis(p[1])  # AST_sintaxis
  elementos = AST_elementos()
  elementos.clausura(s)
  p[0] = elementos

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
  s = AST_sintaxis(p[1])
  campos = AST_campos()
  campos.clausura(s)
  p[0] = campos

def p_campo(p): # AST_campo
  '''
  campo : clave_campo s opt_valor_campo
  '''
  clave = p[1]      # AST_identificador | AST_declaracion_funcion | ¿AST_invocacion? | AST_expresion_literal | AST_format_string | AST_expresion
  s = p[2]          # [AST_skippeable]
  opt_valor = p[3]  # AST_expresion | [AST_skippeable]
  clave.clausura(s)
  if not isinstance(opt_valor, AST_expresion):
    clave.clausura(opt_valor)
    opt_valor = None
  campo = AST_campo(clave, opt_valor)
  p[0] = campo

def p_campo_con_valor(p): # AST_expresion
  '''
  opt_valor_campo : DOS_PUNTOS s expresion
                  | ASIGNACION1 s expresion
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # [AST_skippeable]
  valor = p[3]
  valor.apertura(s)
  p[0] = valor

def p_campo_sin_valor(p): # [AST_skippeable]
  '''
  opt_valor_campo : vacio
  '''
  p[0] = p[1]

def p_clave_campo_identificador_con_prefijo(p): # AST_expresion | AST_identificador | AST_declaracion_funcion | ¿AST_invocacion?
  '''
  clave_campo : operador_prefijo nombre opt_modificador_clave_campo
  '''
  pre = AST_sintaxis(p[1])        # AST_sintaxis
  clave = AST_identificador(p[2]) # AST_identificador
  modificador = p[3]              # AST_funcion_incompleta | AST_invocacion | AST_modificador_objeto_acceso | [AST_skippeable]
  clave.apertura(pre)
  if isinstance(modificador, AST_invocacion):
    pass # ¿Esto sería un error?
  elif isinstance(modificador, AST_funcion_incompleta):
    clave = crearDeclaracionFuncion(clave, modificador)
  elif isinstance(modificador, AST_modificador_objeto_acceso):
    clave = aplicarModificador(clave, modificador)
  else:
    clave.clausura(modificador)
  p[0] = clave

def p_clave_campo_identificador(p): # AST_identificador | AST_declaracion_funcion | ¿AST_invocacion?
  '''
  clave_campo : nombre opt_definicion_funcion
  '''
  clave = AST_identificador(p[1]) # AST_identificador
  opt_definicion = p[2]           # AST_funcion_incompleta | AST_invocacion | [AST_skippeable]
  if isinstance(opt_definicion, AST_invocacion):
    pass # ¿Esto sería un error?
  elif isinstance(opt_definicion, AST_funcion_incompleta):
    clave = crearDeclaracionFuncion(clave, opt_definicion)
  else:
    clave.clausura(opt_definicion)
  p[0] = clave

def p_opt_definicion_funcion_si(p): # AST_funcion_incompleta | AST_invocacion
  '''
  opt_definicion_funcion : definicion_funcion
  '''
  p[0] = p[1]

def p_opt_definicion_funcion_no(p): # [AST_skippeable]
  '''
  opt_definicion_funcion : vacio
  '''
  p[0] = p[1]

def p_clave_campo_literal(p): # AST_expresion_literal
  '''
  clave_campo : NUMERO
              | STRING
  '''
  clave = AST_expresion_literal(p[1])   # AST_expresion_literal
  p[0] = clave

def p_clave_campo_format_string(p): # AST_format_string
  '''
  clave_campo : format_string
  '''
  clave = p[1]      # AST_format_string
  p[0] = clave

def p_clave_campo_variable(p): # AST_identificador
  '''
  clave_campo : ABRE_CORCHETE s IDENTIFICADOR opt_decorador_tipo CIERRA_CORCHETE
  '''
  abre = AST_sintaxis(p[1])                 # AST_sintaxis
  abre = concatenar(abre, p[2])             # [AST_skippeable]
  identificador = AST_identificador(p[3])   # AST_identificador
  opt_decorador = p[4]                      # AST_decorador_tipo | AST_decorador_subtipo | [AST_skippeable]
  cierra = AST_sintaxis(p[5])               # AST_sintaxis
  identificador = aplicarModificador(identificador, opt_decorador)
  identificador.apertura(abre)
  identificador.clausura(cierra)
  p[0] = identificador

# DECLARACIÓN : OTRAS EXPRESIONES SUELTAS
 #################################################################################################
def p_declaracion_expresion_suelta(p): # AST_expresion
  '''
  declaracion_no_objeto : expresion_suelta
  '''
  expresion = p[1] # AST_expresion
  p[0] = p[1]

# DECLARACIÓN : COMBINADOR (if, for, while, else, switch, try, finally)
 #################################################################################################
def p_declaracion_combinador(p): # AST_combinador
  '''
  declaracion_no_objeto : combinador
  '''
  combinador = p[1] # AST_combinador
  p[0] = combinador

def p_combinador(p): # AST_combinador
  '''
  combinador : selector_combinador cuerpo_combinador
  '''
  combinador = p[1] # AST_combinador
  cuerpo = p[2]     # AST_cuerpo | [AST_skippeable]
  combinador.agregar_cuerpo(cuerpo)
  p[0] = combinador

def p_cuerpo_combinador_con_llaves(p): # AST_cuerpo | [AST_skippeable]
  '''
  cuerpo_combinador : opt_cuerpo
  '''
  cuerpo = p[1]                   # AST_cuerpo | [AST_skippeable]
  p[0] = cuerpo

def p_cuerpo_combinador_sin_llaves(p): # AST_cuerpo
  '''
  cuerpo_combinador : declaracion_no_objeto
  '''
  contenido = p[1]               # AST_declaracion
  programa = AST_cuerpo([contenido])
  p[0] = programa

def p_opt_cuerpo_vacio(p): # [AST_skippeable]
  '''
  opt_cuerpo : vacio
  '''
  p[0] = p[1]

def p_opt_cuerpo_cuerpo(p): # AST_cuerpo
  '''
  opt_cuerpo : cuerpo
  '''
  p[0] = p[1]

def p_selector_combinador_simple_1(p): # AST_combinador
  '''
  selector_combinador : COMBINADOR1 s ABRE_PAREN programa CIERRA_PAREN s
  '''
  clase = p[1]                                # string
  s1 = AST_sintaxis(clase)                    # AST_sintaxis
  s1 = concatenar(s1, p[2])                   # AST_skippeable
  s1 = concatenar(s1, AST_sintaxis(p[3]))     # AST_skippeable
  expresion = p[4]                            # [AST_nodo]
  s2 = AST_sintaxis(p[5])
  s2 = concatenar(s2, p[6])
  if len(expresion) > 0:
    expresion[0].apertura(s1)
    expresion[-1].clausura(s2)
  else:
    expresion = concatenar(s1,s2)
  p[0] = AST_combinador(clase, expresion)

def p_selector_combinador_simple_2(p): # AST_combinador
  '''
  selector_combinador : COMBINADOR2 s
  '''
  clase = p[1]                  # string
  s = AST_sintaxis(clase)       # AST_sintaxis
  s = concatenar(s, p[2])       # [AST_skippeable]
  combinador = AST_combinador(clase)
  combinador.apertura(s)
  p[0] = combinador

def p_selector_combinador_simple_3(p): # AST_combinador
  '''
  selector_combinador : CATCH s opt_guarda
  '''
  clase = p[1]                  # string
  s = AST_sintaxis(clase)       # AST_sintaxis
  s = concatenar(s, p[2])       # [AST_skippeable]
  expresion = p[3]              # [AST_nodo]
  combinador = AST_combinador(clase, expresion)
  combinador.apertura(s)
  p[0] = combinador

def p_opt_guarda_si(p):
  '''
  opt_guarda : ABRE_PAREN programa CIERRA_PAREN s
  '''
  s1 = AST_sintaxis(p[1])       # AST_sintaxis
  expresion = p[2]              # [AST_nodo]
  s2 = AST_sintaxis(p[3])       # AST_sintaxis
  s2 = concatenar(s2, p[4])     # [AST_skippeable]
  if len(expresion) > 0:
    expresion[0].apertura(s1)
    expresion[-1].clausura(s2)
  else:
    expresion = concatenar(s1,s2)
  p[0] = expresion

def p_opt_guarda_no(p):
  '''
  opt_guarda : vacio
  '''
  p[0] = p[1]

def p_selector_combinador_else(p): # AST_combinador
  '''
  selector_combinador : ELSE opt_if
  '''
  clase = p[1]                  # string
  s = AST_sintaxis(clase)       # AST_sintaxis
  combinador = p[2]             # AST_combinador | [AST_skippeable]
  if not (isinstance(combinador, AST_combinador)):
    combinador = AST_combinador(clase)
    combinador.clausura(p[2])
  combinador.apertura(s)
  p[0] = combinador

def p_opt_if(p): # AST_combinador | [AST_skippeable]
  '''
  opt_if : selector_combinador
         | sf opt_if
         | vacio
  '''
  p[0] = modificador_opcional(p)

# DECLARACIÓN : COMBINADOR (case)
 #################################################################################################
def p_declaracion_case(p): # AST_combinador
  '''
  declaracion_no_objeto : CASE s expresion_no_tipada DOS_PUNTOS s cuerpo_combinador
  '''
  clase = p[1]                        # string
  abre = AST_sintaxis(clase)          # AST_sintaxis
  abre = concatenar(abre, p[2])       # [AST_skippeable]
  expresion = p[3]                    # AST_expresion
  cierra = AST_sintaxis(p[4])         # AST_sintaxis
  cierra = concatenar(cierra, p[5])   # [AST_skippeable]
  cuerpo = p[6]                       # AST_cuerpo
  expresion.clausura(cierra)
  combinador = AST_combinador(clase, expresion)
  combinador.apertura(abre)
  combinador.agregar_cuerpo(cuerpo)
  p[0] = combinador

def p_declaracion_default(p): # AST_combinador
  '''
  declaracion_no_objeto : DEFAULT s DOS_PUNTOS s cuerpo_combinador
  '''
  clase = p[1]                        # string
  abre = AST_sintaxis(clase)          # AST_sintaxis
  abre = concatenar(abre, p[2])       # [AST_skippeable]
  cierra = AST_sintaxis(p[3])         # AST_sintaxis
  cierra = concatenar(cierra, p[4])   # [AST_skippeable]
  cuerpo = p[5]                       # AST_cuerpo
  combinador = AST_combinador(clase)
  combinador.apertura(concatenar(abre, cierra))
  combinador.agregar_cuerpo(cuerpo)
  p[0] = combinador

# DECLARACIÓN : OPERADOR PREFIJO (!, -, ++, --)
 #################################################################################################
def p_declaracion_prefijo(p): # AST_operador
  '''
  declaracion_no_objeto : operador_prefijo s expresion_como_comando
  '''
  operador = p[1]                 # string
  s = AST_sintaxis(operador)      # AST_sintaxis
  s = concatenar(s, p[2])         # [AST_skippeable]
  expresion = p[3]                # AST_expresion
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    expresion.izq = AST_operador(None, operador, expresion.izq)
  else:
    expresion = AST_operador(None, operador, expresion)
  expresion.apertura(s)
  p[0] = expresion

def p_operador_prefijo(p): # string
  '''
  operador_prefijo : OPERADOR_PREFIJO
                   | OPERADOR_INFIJO
                   | EXCLAMACION
                   | MENOS
  '''
  operador = p[1]
  p[0] = operador

def p_expresion_como_comando(p): # AST_expresion
  '''
  expresion_como_comando : expresion
  '''
  expresion = p[1]
  p[0] = expresion

# DECLARACIÓN : RETURN (return | throw)
 #################################################################################################
def p_declaracion_return(p): # AST_return
  '''
  declaracion_no_objeto : RETURN s opt_expresion
  '''
  s1 = AST_sintaxis(p[1])     # AST_sintaxis
  s1 = concatenar(s1, p[2])   # [AST_skippeable]
  expresion = p[3]            # AST_expresion | [AST_skippeable]
  if isinstance(expresion, AST_expresion):
    expresion.apertura(s1)
  else:
    expresion = concatenar(s1, expresion)
  p[0] = AST_return(expresion)

def p_opt_expresion_expresion(p):
  '''
  opt_expresion : expresion
  '''
  p[0] = p[1]

def p_opt_expresion_nada(p):
  '''
  opt_expresion : vacio
  '''
  p[0] = p[1]

# DECLARACIÓN : CORTE_CICLO (break | continue)
 #################################################################################################
def p_declaracion_corte(p): # AST_return
  '''
  declaracion_no_objeto : CORTE_CICLO
  '''
  s = AST_sintaxis(p[1])      # AST_sintaxis
  p[0] = AST_return(s)

# DECLARACIÓN : IMPORT (import)
 #################################################################################################
def p_declaracion_import(p): # AST_import
  '''
  declaracion_no_objeto : IMPORT s elementos_a_importar
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # [AST_skippeable]
  importar = p[3]           # AST_import
  importar.apertura(s)
  p[0] = importar

def p_import_archivo(p): # AST_import
  '''
  elementos_a_importar : STRING
  '''
  archivo = AST_expresion_literal(p[1])   # AST_expresion_literal
  p[0] = AST_import(archivo)

def p_import_elementos(p): # AST_import
  '''
  elementos_a_importar : opt_type s importables s opt_importar_como FROM s STRING
  '''
  t = p[1]                                # AST_sintaxis | [AST_skippeable]
  s1 = concatenar(t, p[2])                # [AST_skippeable]
  importables = p[3]                      # AST_identificador | AST_identificadores | AST_sintaxis
  s2 = p[4]                               # [AST_skippeable]
  opt_alias = p[5]                        # AST_identificador | [AST_skippeable]
  r = AST_sintaxis(p[6])                  # AST_sintaxis
  s3 = concatenar(r,p[7])                 # [AST_skippeable]
  archivo = AST_expresion_literal(p[8])   # AST_expresion_literal
  es_tipo = isinstance(t, AST_sintaxis) and t.contenido == 'type'
  importables.apertura(s1)
  importables.clausura(s2)
  archivo.apertura(s3)
  p[0] = AST_import(archivo, importables, opt_alias, es_tipo)

def p_opt_type_vacio(p): # [AST_skippeable]
  '''
  opt_type : vacio
  '''
  p[0] = p[1]

def p_opt_type_tipo(p): # AST_sintaxis
  '''
  opt_type : TYPE
  '''
  p[0] = AST_sintaxis(p[1])

def p_imporables_identificador(p): # AST_identificador | AST_identificadores
  '''
  importables : mas_identificadores_o_modificadores_no_vacio
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
  s1 = AST_sintaxis(p[1])           # AST_sintaxis
  s1 = concatenar(s1,p[2])          # [AST_skippeable]
  alias = AST_identificador(p[3])   # AST_identificador
  s2 = p[4]                         # [AST_skippeable]
  alias.apertura(s1)
  alias.clausura(s2)
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
  declaracion_no_objeto : EXPORT s declaracion_o_identificador
  '''
  s = AST_sintaxis(p[1])            # AST_sintaxis
  s = concatenar(s,p[2])            # [AST_skippeable]
  exportado = p[3]                  # AST_declaracion_variable | AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion | AST_declaracion_clase | AST_declaracion_tipo | AST_identificador | AST_identificadores
  export = AST_export(exportado)
  export.apertura(s)
  p[0] = export

def p_export_declaracion(p): # AST_declaracion_variable | AST_expresion_funcion | AST_declaracion_funcion | AST_invocacion | AST_declaracion_clase | AST_declaracion_tipo
  '''
  declaracion_o_identificador : declaracion_variable
                              | declaracion_de_funcion
                              | declaracion_de_clase
                              | declaracion_de_tipo
  '''
  p[0] = p[1]

def p_export_identificador(p): # AST_identificador | AST_identificadores | AST_asignacion
  '''
  declaracion_o_identificador : identificador_no_type opt_modificador_identificador
  '''
  identificador = p[1]
  modificador = p[2]
  p[0] = aplicarModificador(identificador, modificador)

# DECLARACIÓN : TYPE (type)
 #################################################################################################
def p_declaracion_tipo(p): # AST_declaracion_tipo
  '''
  declaracion_no_objeto : declaracion_de_tipo
  '''
  p[0] = p[1]

def p_declaracion_de_tipo(p): # AST_declaracion_tipo | AST_identificador | AST_identificadores
  '''
  declaracion_de_tipo : TYPE s continuacion_type_en_declaracion
  '''
  resultado = None
  c = p[3]                                                    # AST_TMP ( vacio | nombre | decorador | modificador | operador )
  if c.identificador == "vacio": # Es una variable llamada 'type'
    identificador = AST_identificador(p[1])
    identificador.clausura(p[2])
    identificador.clausura(c.contenido)
    resultado = identificador
  elif c.identificador == "nombre": # Sigue otro nombre así que estoy declarando un tipo (type IDENTIFICADOR = ...)
    nombre = c.contenido
    rec = c.rec
    if rec.identificador == "tipo": # El nombre del tipo es 'nombre'
      tipo = rec.contenido
      s = AST_sintaxis(p[1])      # AST_sintaxis
      s = concatenar(s, p[2])     # [AST_skippeable]
      tipo = AST_declaracion_tipo(nombre, tipo)
      tipo.apertura(s)
      resultado = tipo
    elif rec.identificador == "modificador": # El nombre del tipo es 'nombre' modificado (e.g. IDENTIFICADOR<...>)
      modificador = rec.contenido
      tipo = rec.rec
      s = AST_sintaxis(p[1])      # AST_sintaxis
      s = concatenar(s, p[2])     # [AST_skippeable]
      nombre = AST_tipo_base(nombre)
      nombre = aplicarModificador(nombre, modificador)
      tipo = AST_declaracion_tipo(nombre, tipo)
      tipo.apertura(s)
      resultado = tipo
    elif rec.identificador == "mas_ids": # El nombre del tipo viene después y 'nombre' es otro modificador (e.g. public, static, etc.)
      mas_ids = rec.contenido     # AST_identificador | AST_identificadores
      identificador = AST_identificador(p[1])
      identificador.clausura(p[2])
      decorador = AST_decorador_keyword(identificador)
      mas_ids.agregar_decorador_pre(decorador)
      for m in rec.rec:
        mas_ids = aplicarModificador(mas_ids, m)
      resultado = mas_ids
  elif c.identificador == "decorador":
    decorador = c.contenido
    identificador = AST_identificador(p[1])
    identificador.clausura(p[2])
    resultado = aplicarModificador(identificador, decorador)
  elif c.identificador == "modificador":
    modificador = c.contenido
    identificador = AST_identificador(p[1])
    identificador.clausura(p[2])
    resultado = aplicarModificador(identificador, modificador)
  elif c.identificador == "operador":
    operador = c.contenido
    identificador = AST_identificador(p[1])
    identificador.clausura(p[2])
    resultado = aplicarModificador(identificador, operador)
  else:
    fallaDebug()
  p[0] = resultado

def p_continuacion_type_en_declaracion_vacio(p): # AST_TMP ( vacio )
  '''
  continuacion_type_en_declaracion : vacio
  '''
  p[0] = AST_TMP("vacio", p[1])

def p_continuacion_type_en_declaracion_sigue_id(p): # AST_TMP ( nombre ) ; ( tipo | modificador | mas_ids )
  '''
  continuacion_type_en_declaracion : IDENTIFICADOR s continuacion_nombre_en_declaracion
  '''
  nombre = AST_identificador(p[1])
  s = p[2]
  rec = p[3]
  nombre.clausura(s)
  p[0] = AST_TMP("nombre", nombre, rec)

def p_continuacion_type_en_declaracion_sigue_decorador(p): # AST_TMP ( decorador )
  '''
  continuacion_type_en_declaracion : decorador_declaracion_clase opt_modificador_dentro_de_clase
  '''
  decorador = p[1]
  opt_modificador_adicional = p[2]
  decorador.modificador_adicional(opt_modificador_adicional)
  p[0] = AST_TMP("decorador", decorador)

def p_continuacion_type_en_declaracion_sigue_modificador(p): # AST_TMP ( modificador )
  '''
  continuacion_type_en_declaracion : modificador_dentro_de_clase
  '''
  modificador = p[1]
  p[0] = AST_TMP("modificador", modificador)

def p_continuacion_type_en_declaracion_sigue_operador_binario(p): # AST_TMP ( operador )
  '''
  continuacion_type_en_declaracion : operador_binario_no_menor s expresion
  '''
  clase = p[1]                # string
  s = AST_sintaxis(clase)     # AST_sintaxis
  s = concatenar(s, p[2])     # [AST_skippeable]
  expresion = p[3]
  expresion.apertura(s)
  if isinstance(expresion, AST_operador) and expresion.esBinario() and not expresion.tieneParentesis():
    modificador = AST_modificador_operador_binario(clase, expresion.izq)
    modificador.modificador_adicional(AST_modificador_operador_binario(expresion.op, expresion.der))
  else:
    modificador = AST_modificador_operador_binario(clase, expresion)
  p[0] = AST_TMP("operador", modificador)

def p_continuacion_type_en_declaracion_sigue_operador_ternario(p): # AST_TMP ( operador )
  '''
  continuacion_type_en_declaracion : PREGUNTA s expresion_no_tipada DOS_PUNTOS s expresion
  '''
  s1 = AST_sintaxis(p[1])     # AST_sintaxis
  s1 = concatenar(s1, p[2])   # [AST_skippeable]
  e1 = p[3]                   # AST_expresion
  s2 = AST_sintaxis(p[4])     # AST_sintaxis
  s2 = concatenar(s2, p[5])   # [AST_skippeable]
  e2 = p[6]                   # AST_expresion
  e1.apertura(s1)
  e2.apertura(s2)
  modificador = AST_modificador_operador_ternario(e1,e2)
  p[0] = AST_TMP("operador", modificador)

def p_operador_binario_no_menor(p): # string
  '''
  operador_binario_no_menor : OPERADOR_BOOLEANO
                            | MAS
                            | POR
                            | DIV
                            | MENOS
                            | MAYOR
                            | PIPE
                            | IN
  '''
  operador = p[1]
  p[0] = operador

def p_continuacion_type_en_declaracion_sigue_operador_posfijo(p): # AST_TMP ( operador )
  '''
  continuacion_type_en_declaracion : operador_posfijo_no_exclamacion opt_modificador_expresion
  '''
  operador = p[1]
  opt_adicional = p[2]
  modificador = AST_modificador_operador_posfijo(operador)
  modificador.modificador_adicional(opt_adicional)
  p[0] = AST_TMP("operador", modificador)

def p_operador_posfijo_no_exclamacion(p): # string
  '''
  operador_posfijo_no_exclamacion : OPERADOR_INFIJO
                                  | OPERADOR_PREFIJO
  '''
  operador = p[1]
  p[0] = operador

def p_continuacion_nombre_en_declaracion_sigue_asignacion(p): # AST_TMP ( tipo )
  '''
  continuacion_nombre_en_declaracion : ASIGNACION1 s tipo
  '''
  s = AST_sintaxis(p[1])
  s = concatenar(s, p[2])
  tipo = p[3]
  tipo.apertura(s)
  p[0] = AST_TMP("tipo", tipo)

def p_continuacion_nombre_en_declaracion_sigue_id_clase(p): # AST_TMP ( modificador )
  '''
  continuacion_nombre_en_declaracion : modificador_id_clase s ASIGNACION1 s tipo
  '''
  modificador = p[1]
  s = AST_sintaxis(p[3])
  s = concatenar(p[2], s)
  s = concatenar(s, p[4])
  tipo = p[5]
  tipo.apertura(s)
  p[0] = AST_TMP("modificador", modificador, tipo)

def p_continuacion_nombre_en_declaracion_sigue_mas_ids(p): # AST_TMP ( mas_ids )
  '''
  continuacion_nombre_en_declaracion : mas_identificadores_o_modificadores_no_vacio opt_decorador_declaracion_clase opt_modificador_dentro_de_clase 
  '''
  declaracion = p[1]          # AST_identificador | AST_identificadores
  opt_decorador = p[2]                # AST_decorador | [AST_skippeable]
  opt_modificador_adicional = p[3]    # AST_modificador_asignacion | AST_expresion_funcion | [AST_skippeable]
  p[0] = AST_TMP("mas_ids", declaracion, [opt_decorador, opt_modificador_adicional])

# DECLARACIÓN : CLASS (class)
 #################################################################################################
def p_declaracion_clase(p): # AST_declaracion_clase
  '''
  declaracion_no_objeto : declaracion_de_clase
  '''
  p[0] = p[1]

def p_declaracion_con_class(p): # AST_declaracion_clase | AST_identificador
  '''
  declaracion_de_clase : DECL_CLASS s continuacion_class
  '''
  resultado = None
  c = p[3]                            # AST_TMP ( clase | decorador )
  if c.identificador == 'clase':
    s = AST_sintaxis(p[1])            # AST_sintaxis
    s = concatenar(s, p[2])           # [AST_skippeable]
    clase = c.contenido
    clase.apertura(s)
    resultado = clase
  elif c.identificador == 'decorador':
    identificador = AST_identificador(p[1]) # AST_identificador
    s = p[2]                                # [AST_skippeable]
    decorador = c.contenido
    identificador.apertura(s)
    identificador = aplicarModificador(identificador, decorador)
    resultado = identificador
  else:
    fallaDebug()
  p[0] = resultado

def p_continuacion_class_definicion_clase(p): # AST_TMP ( clase )
  '''
  continuacion_class : id_clase opt_modificador_clase cuerpo_clase
  '''
  nombre = p[1]                     # AST_tipo
  modificador = p[2]                # AST_decorador | [AST_skippeable]
  definicion = p[3]                 # AST_cuerpo
  nombre = aplicarModificador(nombre, modificador)
  clase = AST_declaracion_clase(nombre, definicion)
  p[0] = AST_TMP('clase', clase)

def p_continuacion_class_definicion_campo(p): # AST_TMP ( decorador )
  '''
  continuacion_class : decorador_tipo
                     | decorador_opcional
  '''
  decorador = p[1]
  p[0] = AST_TMP('decorador', decorador)

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
  programa_clase_util : declaracion_dentro_de_clase opt_cierre programa_clase_util
  '''
  declaracion = p[1]
  cierre = p[2]
  rec = p[3]
  declaracion.clausura(cierre)
  p[0] = concatenar(declaracion, rec)

def p_declaracion_dentro_de_clase_con_pre(p): # AST_declaracion
  '''
  declaracion_dentro_de_clase : declarador_o_identificador_con_modificadores_pre opt_decorador_declaracion_clase opt_modificador_dentro_de_clase
  '''
  declaracion = p[1]                  # AST_declaracion
  opt_decorador = p[2]                # AST_decorador | [AST_skippeable]
  opt_modificador_adicional = p[3]    # AST_modificador_asignacion | AST_expresion_funcion | [AST_skippeable]
  declaracion = aplicarModificador(declaracion, opt_decorador)
  declaracion = aplicarModificador(declaracion, opt_modificador_adicional)
  p[0] = declaracion

def p_declaracion_dentro_de_clase_tipo(p): # AST_declaracion_tipo | AST_identificador | AST_identificadores
  '''
  declaracion_dentro_de_clase : declaracion_de_tipo
  '''
  p[0] = p[1]

def p_declaracion_dentro_de_clase_indexacion(p): # AST_indexacion_clase
  '''
  declaracion_dentro_de_clase : ABRE_CORCHETE s identificador CIERRA_CORCHETE opt_decorador_tipo
  '''
  abre = AST_sintaxis(p[1])       # AST_sintaxis
  abre = concatenar(abre, p[2])   # [AST_skippeable]
  identificador = p[3]            # AST_identificador
  cierra = AST_sintaxis(p[4])     # AST_sintaxis
  decorador = p[5]                # AST_decorador_tipo | [AST_skippeable]
  identificador.apertura(abre)
  identificador.clausura(cierra)
  indexado = AST_indexacion_clase(identificador)
  indexado = aplicarModificador(indexado, decorador)
  p[0] = indexado


def p_declarador_o_identificador_con_modificadores_pre_decl(p): # AST_declaracion_clase
  '''
  declarador_o_identificador_con_modificadores_pre : declaracion_de_clase
  '''
  p[0] = p[1]

def p_declarador_o_identificador_con_modificadores_pre_ids(p): # AST_identificador | AST_identificadores
  '''
  declarador_o_identificador_con_modificadores_pre : identificador_con_modificadores_pre
  '''
  p[0] = p[1]

def p_declaracion_dentro_de_clase_export(p): # AST_export
  '''
  declaracion_dentro_de_clase : EXPORT s declaracion_dentro_de_clase
  '''
  s = AST_sintaxis(p[1])              # AST_sintaxis
  s = concatenar(s, p[2])             # [AST_skippeable]
  declaracion = p[3]                  # AST_declaracion
  declaracion = AST_export(declaracion)
  declaracion.apertura(s)
  p[0] = declaracion

def p_declaracion_dentro_de_clase_new(p): # AST_export
  '''
  declaracion_dentro_de_clase : NEW s opt_mas_identificadores_o_modificadores opt_decorador_declaracion_clase opt_modificador_dentro_de_clase
  '''
  identificador = AST_identificador(p[1])   # AST_identificador
  s = p[2]                                  # [AST_skippeable]
  rec = p[3]                                # AST_identificador | AST_identificadores | [AST_skippeable]
  identificador.clausura(s)
  if isinstance(rec, AST_asignable):
    decorador = AST_decorador_keyword(identificador)
    rec.agregar_decorador_pre(decorador)
    identificador = rec
  else:
    identificador.clausura(rec)
  opt_decorador = p[4]                # AST_decorador | [AST_skippeable]
  opt_modificador_adicional = p[5]    # AST_modificador_asignacion | AST_expresion_funcion | [AST_skippeable]
  identificador = aplicarModificador(identificador, opt_decorador)
  identificador = aplicarModificador(identificador, opt_modificador_adicional)
  p[0] = identificador

def p_identificadores_con_modificadores_pre(p): # AST_identificadores
  '''
  identificador_con_modificadores_pre : ABRE_LLAVE s identificadores_o_type CIERRA_LLAVE
  '''
  abre = AST_sintaxis(p[1])   # AST_sintaxis
  s = concatenar(abre, p[2])  # [AST_skippeable]
  lista = p[3]                # [AST_identificador]
  cierra = AST_sintaxis(p[4]) # AST_sintaxis
  identificadores = AST_identificadores(lista)
  identificadores.apertura(s)
  identificadores.clausura(cierra)
  p[0] = identificadores

def p_identificadores_con_modificadores_sin_llaves(p): # AST_identificador | AST_identificadores
  '''
  identificador_con_modificadores_pre : identificador_con_modificadores_pre_sin_llaves
  '''
  p[0] = p[1]

def p_identificador_o_type_type(p): # [AST_identificador]
  '''
  identificadores_o_type : TYPE s identificadores
  '''
  rec = p[3]                  # [AST_identificador]
  if len(rec) == 0:
    identificador = AST_identificador(p[1])
    identificador.clausura(p[2])
    p[0] = [identificador]
  else:
    s = AST_sintaxis(p[1])      # AST_sintaxis
    s = concatenar(s, p[2])     # [AST_skippeable]
    rec[0].apertura(s)
    p[0] = rec

def p_identificador_o_type_no_type(p): # [AST_identificador]
  '''
  identificadores_o_type : identificadores_no_vacio
  '''
  p[0] = p[1]

def p_identificador_con_modificadores_pre(p): # AST_identificador | AST_identificadores
  '''
  identificador_con_modificadores_pre_sin_llaves : nombre_no_type s opt_mas_identificadores_o_modificadores
  '''
  identificador = AST_identificador(p[1])   # AST_identificador
  s = p[2]                                  # [AST_skippeable]
  rec = p[3]                                # AST_identificador | AST_identificadores | [AST_skippeable]
  identificador.clausura(s)
  if isinstance(rec, AST_asignable):
    decorador = AST_decorador_keyword(identificador)
    rec.agregar_decorador_pre(decorador)
    identificador = rec
  else:
    identificador.clausura(rec)
  p[0] = identificador

def p_mas_identificadores_o_modificadores_vacio(p): # [AST_skippeable]
  '''
  opt_mas_identificadores_o_modificadores : vacio
  '''
  p[0] = p[1]

def p_mas_identificadores_o_modificadores_no_vacio(p): # AST_identificador | AST_identificadores
  '''
  opt_mas_identificadores_o_modificadores : mas_identificadores_o_modificadores_no_vacio
  '''
  p[0] = p[1]

def p_mas_identificadores_o_modificadores_proximo(p): # AST_identificador | AST_identificadores
  '''
  mas_identificadores_o_modificadores_no_vacio : identificador_con_modificadores_pre
  '''
  p[0] = p[1]

def p_id_clases_coma(p): # AST_tipo_varios
  '''
  id_clases_coma : id_clase s opt_mas_ids_clase_coma
  '''
  clase = p[1]    # AST_tipo
  s = p[2]        # [AST_skippeable]
  rec = p[3]      # AST_tipo_varios | [AST_skippeable]
  clase.clausura(s)
  if isinstance(rec, AST_tipo_varios):
    rec.agregar_tipo(clase)
  else:
    clase.clausura(rec)
    rec = AST_tipo_varios(clase)
  p[0] = clase

def p_opt_mas_ids_clase_coma_ninguna(p): # [AST_skippeable]
  '''
  opt_mas_ids_clase_coma : vacio
  '''
  p[0] = p[1]

def p_opt_mas_ids_clase_coma_otra(p): # AST_tipo_varios
  '''
  opt_mas_ids_clase_coma : COMA s id_clases_coma
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # [AST_skippeable]
  clase = p[3]              # AST_tipo_varios
  clase.apertura(s)
  p[0] = clase

def p_id_clases_and(p): # AST_tipo_varios
  '''
  id_clases_and : id_clase s opt_mas_ids_clase_and
  '''
  clase = p[1]    # AST_tipo
  s = p[2]        # [AST_skippeable]
  rec = p[3]      # AST_tipo_varios | [AST_skippeable]
  clase.clausura(s)
  if isinstance(rec, AST_tipo_varios):
    rec.agregar_tipo(clase)
  else:
    clase.clausura(rec)
    rec = AST_tipo_varios(clase)
  p[0] = clase

def p_opt_mas_ids_clase_and_ninguna(p): # [AST_skippeable]
  '''
  opt_mas_ids_clase_and : vacio
  '''
  p[0] = p[1]

def p_opt_mas_ids_clase_and_otra(p): # AST_tipo_varios
  '''
  opt_mas_ids_clase_and : AND s id_clases_and
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # [AST_skippeable]
  clase = p[3]              # AST_tipo_varios
  clase.apertura(s)
  p[0] = clase

def p_tipos_fin(p): # AST_tipo_tupla
  '''
  tipos : vacio
  '''
  p[0] = AST_tipo_tupla([])

def p_tipos_tipo(p): # AST_tipo_tupla
  '''
  tipos : tipo opt_modificador_extend_and mas_tipos
  '''
  tipo = p[1]             # AST_tipo
  modificador = p[2]      # AST_decorador | [AST_skippeable]
  rec = p[3]              # AST_tipo_tupla
  tipo = aplicarModificador(tipo, modificador)
  rec.fst(tipo)
  p[0] = rec

def p_mas_tipos_fin(p): # AST_tipo_tupla
  '''
  mas_tipos : vacio
  '''
  p[0] = AST_tipo_tupla([])

def p_mas_tipos_tipo(p): # AST_tipo_tupla
  '''
  mas_tipos : COMA s tipos
  '''
  s = AST_sintaxis(p[1])    # AST_sintaxis
  s = concatenar(s, p[2])   # [AST_skippeable]
  rec = p[3]                # AST_tipo_tupla
  rec.apertura(s)
  p[0] = rec

def p_cierre(p): # [AST_skippeable]
  '''
  cierre : PUNTO_Y_COMA s
  '''
  punto_y_coma = AST_sintaxis(p[1])
  cierre = p[2]                       # [AST_skippeable]
  p[0] = concatenar(punto_y_coma, cierre)

def p_salto(p): # [AST_skippeable]
  '''
  salto : SALTO s
  '''
  salto = AST_salto(p[1])
  cierre = p[2]                       # [AST_skippeable]
  p[0] = concatenar(salto, cierre)

def p_separador(p): # [AST_skippeable]
  '''
  separador : cierre
            | salto
  '''
  p[0] = p[1]

def p_espacios(p): # [AST_skippeable]
  '''
  espacios : ESPACIO s
  '''
  espacios = AST_espacios(p[1])
  cierre = p[2]                       # [AST_skippeable]
  p[0] = concatenar(espacios, cierre)

def p_opt_cierre_con_skip(p): # [AST_skippeable]
  '''
  opt_cierre :  espacios opt_cierre
  '''
  p[0] = concatenar(p[1], p[2])

def p_opt_cierre_sin_skip(p): # [AST_skippeable]
  '''
  opt_cierre : separador
  '''
  p[0] = p[1]

def p_opt_cierre_nada(p): # [AST_skippeable]
  '''
  opt_cierre : vacio
  '''
  p[0] = p[1]

def p_vacio(p): # [AST_skippeable]
  'vacio : %prec VACIO'
  p[0] = []

## == MODIFICADORES == ##

def p_opt_modificador_clave_campo(p): # ... | [AST_skippeable]
  '''
  opt_modificador_clave_campo : modificador_clave_campo
                              | sf opt_modificador_clave_campo
                              | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_clave_campo(p): # AST_funcion_incompleta | AST_invocacion | AST_modificador_objeto_acceso
  '''
  modificador_clave_campo : definicion_funcion
                          | acceso opt_modificador_expresion
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_id_clase(p): # ... | [AST_skippeable]
  '''
  opt_modificador_id_clase : modificador_id_clase
                           | sf opt_modificador_id_clase
                           | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_id_clase(p): # AST_tipo_tupla
  '''
  modificador_id_clase : tipo_tupla
  '''
  modificador = p[1]
  p[0] = modificador

def p_opt_modificador_dentro_de_clase(p): # ... | [AST_skippeable]
  '''
  opt_modificador_dentro_de_clase : modificador_dentro_de_clase
                                  | sf opt_modificador_dentro_de_clase
                                  | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_dentro_de_clase(p): # AST_modificador_objeto | AST_expresion_funcion
  '''
  modificador_dentro_de_clase : modificador_objeto_expresion
                              | definicion_funcion
  '''
  modificador = p[1]                  # AST_modificador_objeto | AST_expresion_funcion | AST_invocacion
  # Si la estoy declarando, no debería haber una invocación
  if type(modificador) is AST_invocacion:
    fallaDebug()
  p[0] = modificador

def p_opt_modificador_clase(p): # ... | [AST_skippeable]
  '''
  opt_modificador_clase : modificador_clase
                        | sf opt_modificador_clase
                        | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_clase(p): # AST_decorador_implementacion | AST_decorador_extension
  '''
  modificador_clase : implementa opt_modificador_clase
                    | extiende opt_modificador_clase
  '''
  modificador = p[1]    # AST_decorador
  opt_adicional = p[2]  # AST_decorador | [AST_skippeable]
  modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_identificador(p): # ... | [AST_skippeable]
  '''
  opt_modificador_identificador : modificador_identificador
                                | sf opt_modificador_identificador
                                | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_identificador(p): # AST_modificador_asignacion
  '''
  modificador_identificador : asignacion
  '''
  modificador = p[1]
  p[0] = modificador

def p_opt_modificador_expresion(p): # ... | [AST_skippeable]
  '''
  opt_modificador_expresion : modificador_expresion
                            | sf opt_modificador_expresion
                            | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_expresion(p): # AST_modificador_objeto | AST_argumentos | AST_modificador_operador | AST_cuerpo | AST_tipo_void | AST_decorador_tipo
  '''
  modificador_expresion : modificador_objeto_expresion
                        | invocacion opt_modificador_expresion
                        | operador
                        | flecha
                        | decorador_y_flecha
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_expresion_no_tipada(p): # ... | [AST_skippeable]
  '''
  opt_modificador_expresion_no_tipada : modificador_expresion_no_tipada
                                      | sf opt_modificador_expresion_no_tipada
                                      | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_expresion_no_tipada(p): # AST_modificador_objeto | AST_argumentos | AST_modificador_operador | AST_cuerpo | AST_tipo_void
  '''
  modificador_expresion_no_tipada : modificador_objeto_expresion_no_tipada
                                  | invocacion_no_tipada
                                  | operador_no_tipado
                                  | flecha
  '''
  modificador = p[1]
  p[0] = modificador

def p_opt_modificador_expresion_asignada(p): # ... | [AST_skippeable]
  '''
  opt_modificador_expresion_asignada : modificador_expresion_asignada
                                     | sf opt_modificador_expresion_asignada
                                     | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_expresion_asignada_acceso(p): # AST_modificador_objeto | AST_tipo_lista | AST_argumentos | AST_modificador_operador | AST_decorador_comotipo | AST_cuerpo | AST_tipo_void
  '''
  modificador_expresion_asignada : acceso opt_modificador_asignable
                                 | indexacion
                                 | invocacion opt_modificador_expresion
                                 | operador
                                 | comotipo opt_modificador_expresion_asignada
                                 | flecha
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_asignable(p): # ... | [AST_skippeable]
  '''
  opt_modificador_asignable : modificador_asignable
                            | sf opt_modificador_asignable
                            | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_asignable(p): # AST_modificador_asignacion | AST_modificador_objeto | AST_tipo_lista | AST_argumentos | AST_decorador_comotipo | AST_modificador_operador
  '''
  modificador_asignable : asignacion
                        | acceso opt_modificador_asignable
                        | indexacion
                        | invocacion opt_modificador_expresion
                        | comotipo opt_modificador_asignable
                        | operador
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_asignable_no_tipado(p): # ... | [AST_skippeable]
  '''
  opt_modificador_asignable_no_tipado : modificador_asignable_no_tipado
                                      | sf opt_modificador_asignable_no_tipado
                                      | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_asignable_no_tipado(p): # AST_modificador_asignacion | AST_modificador_objeto | AST_tipo_lista | AST_argumentos | AST_decorador_comotipo | AST_modificador_operador
  '''
  modificador_asignable_no_tipado : asignacion
                                  | acceso_no_tipado
                                  | indexacion_no_tipada
                                  | invocacion_no_tipada
                                  | comotipo opt_modificador_asignable_no_tipado
                                  | operador_no_tipado
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_objeto_expresion(p): # ... | [AST_skippeable]
  '''
  opt_modificador_objeto_expresion : modificador_objeto_expresion
                                   | sf opt_modificador_objeto_expresion
                                   | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_objeto_expresion(p): # AST_modificador_asignacion | AST_modificador_objeto | AST_tipo_lista | AST_decorador_comotipo
  '''
  modificador_objeto_expresion : asignacion
                               | acceso opt_modificador_asignable
                               | indexacion
                               | comotipo
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_variable(p): # ... | [AST_skippeable]
  '''
  opt_modificador_variable : modificador_variable
                           | sf opt_modificador_variable
                           | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_variable(p): # AST_modificador_asignacion | AST_iterador | AST_modificador_variable_adicional
  '''
  modificador_variable : asignacion opt_mas_variables
                       | iteracion
                       | mas_variables
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_tipo(p): # ... | [AST_skippeable]
  '''
  opt_modificador_tipo : modificador_tipo
                       | sf opt_modificador_tipo
                       | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_tipo(p): # AST_tipo_tupla | AST_tipo_lista | AST_tipo_suma | AST_modificador_objeto_acceso
  '''
  modificador_tipo : tipo_tupla
                   | tipo_con_lista opt_modificador_tipo
                   | tipo_con_pipe
                   | tipo_con_and
                   | acceso opt_modificador_tipo
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_decorador_declaracion_clase(p): # ... | [AST_skippeable]
  '''
  opt_decorador_declaracion_clase : decorador_declaracion_clase
                                  | sf opt_decorador_declaracion_clase
                                  | vacio
  '''
  p[0] = modificador_opcional(p)
def p_decorador_declaracion_clase(p): # AST_decorador_opcional | AST_decorador_tipo
  '''
  decorador_declaracion_clase : decorador_opcional
                              | decorador_tipo
                              | decorador_tipo_tupla
  '''
  modificador = p[1]
  p[0] = modificador

def p_opt_decorador_parametro(p): # ... | [AST_skippeable]
  '''
  opt_decorador_parametro : decorador_parametro
                          | sf opt_decorador_parametro
                          | vacio
  '''
  p[0] = modificador_opcional(p)
def p_decorador_parametro(p): # AST_decorador_comotipo | AST_decorador_default | AST_decorador_opcional | AST_decorador_tipo
  '''
  decorador_parametro : comotipo
                      | decorador_default
                      | decorador_opcional opt_decorador_parametro
                      | decorador_tipo opt_decorador_parametro
                      | decorador_tipo_tupla opt_decorador_parametro
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_decorador_tipo(p): # AST_decorador_tipo | [AST_skippeable]
  '''
  opt_decorador_tipo : decorador_tipo
                     | sf opt_decorador_tipo
                     | vacio
  '''
  p[0] = modificador_opcional(p)

def p_opt_modificador_funcion(p): # ... | [AST_skippeable]
  '''
  opt_modificador_funcion : modificador_funcion
                          | sf opt_modificador_funcion
                          | vacio
  '''
  p[0] = modificador_opcional(p)
def p_modificador_funcion(p): # AST_argumentos | AST_modificador_asignacion | AST_modificador_objeto | AST_tipo_lista | AST_decorador_comotipo
  '''
  modificador_funcion : invocacion
                      | asignacion
                      | acceso opt_modificador_asignable
                      | indexacion
                      | comotipo
  '''
  modificador = p[1]
  if len(p) > 2:
    opt_adicional = p[2]      # AST_modificador | [AST_skippeable]
    modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_opt_modificador_extend_and(p): # AST_decorador_extension
  '''
  opt_modificador_extend_and : EXTENDS s id_clases_and opt_modificador_extend_and
  '''
  s = AST_sintaxis(p[1])            # AST_sintaxis
  s = concatenar(s, p[2])           # [AST_skippeable]
  nombre = p[3]                     # AST_tipo_varios
  rec = p[4]                        # AST_decorador_extension | AST_decorador_default | [AST_skippeable]
  extension = AST_decorador_extension(nombre)
  extension.apertura(s)
  extension.modificador_adicional(rec)
  p[0] = extension

def p_opt_modificador_extend_and_default(p): # AST_decorador_default
  '''
  opt_modificador_extend_and : simbolo_asignacion s identificador opt_modificador_extend_and
  '''
  s = AST_sintaxis(p[1])                        # AST_sintaxis
  s = concatenar(s, p[2])                       # [AST_skippeable]
  expresion = p[3]                              # AST_expresion
  opt_adicional = p[4]                          # AST_decorador_extension | AST_decorador_default | [AST_skippeable]
  decorador = AST_decorador_default(expresion)  # AST_decorador_default
  decorador.apertura(s)
  decorador.modificador_adicional(opt_adicional)
  p[0] = decorador

def p_opt_modificador_extend_and_vacio(p): # [AST_skippeable]
  '''
  opt_modificador_extend_and : vacio
  '''
  p[0] = p[1]

## == Q == ##

def p_extiende(p): # AST_decorador_extension
  '''
  extiende : EXTENDS s id_clases_coma
  '''
  s = AST_sintaxis(p[1])            # AST_sintaxis
  s = concatenar(s, p[2])           # [AST_skippeable]
  nombre = p[3]                     # AST_tipo_varios
  extension = AST_decorador_extension(nombre)
  extension.apertura(s)
  p[0] = extension

def p_implementa(p): # AST_decorador_implementacion
  '''
  implementa : IMPLEMENTS s id_clases_coma
  '''
  implements = AST_sintaxis(p[1])   # AST_sintaxis
  s = concatenar(implements, p[2])  # [AST_skippeable]
  nombre = p[3]                     # AST_tipo_varios
  implementacion = AST_decorador_implementacion(nombre)
  implementacion.apertura(s)
  p[0] = implementacion

def p_tipo_tupla(p): # AST_tipo_tupla
  '''
  tipo_tupla : MENOR s tipos MAYOR opt_modificador_tipo
  '''
  abre = AST_sintaxis(p[1])       # AST_sintaxis
  abre = concatenar(abre, p[2])   # [AST_skippeable]
  tipo = p[3]                     # AST_tipo_tupla
  cierra = AST_sintaxis(p[4])     # AST_sintaxis
  opt_adicional = p[5]            # AST_tipo_lista | AST_tipo_suma | AST_tipo_tupla | AST_modificador_objeto_acceso | [AST_skippeable]
  tipo.apertura(abre)
  tipo.clausura(cierra)
  tipo = aplicarModificador(tipo, opt_adicional)
  p[0] = tipo

def p_asignacion(p): # AST_modificador_asignacion
  '''
  asignacion : simbolo_asignacion s expresion_asignada
  '''
  asignacion = AST_sintaxis(p[1])
  s = concatenar(asignacion, p[2])    # [AST_skippeable]
  expresion = p[3]                    # AST_expresion
  expresion.apertura(s)
  p[0] = AST_modificador_asignacion(expresion)

def p_acceso_objeto(p): # AST_modificador_objeto_acceso
  '''
  acceso : operador_acceso s campo_acceso
  '''
  punto = AST_sintaxis(p[1])
  s = concatenar(punto, p[2])       # [AST_skippeable]
  campo = p[3]                      # AST_identificador | AST_argumentos
  modificador = AST_modificador_objeto_acceso(campo)
  modificador.apertura(s)
  p[0] = modificador

def p_campo_acceso_id(p): # AST_identificador
  '''
  campo_acceso : nombre
  '''
  p[0] = AST_identificador(p[1])

def p_campo_acceso_argumentos(p): # AST_argumentos
  '''
  campo_acceso : invocacion
  '''
  p[0] = p[1]

def p_acceso_objeto_no_tipado(p): # AST_modificador_objeto_acceso
  '''
  acceso_no_tipado : operador_acceso s nombre opt_modificador_asignable_no_tipado
  '''
  punto = AST_sintaxis(p[1])
  s = concatenar(punto, p[2])       # [AST_skippeable]
  campo = AST_identificador(p[3])   # AST_identificador
  opt_adicional = p[4]              # [AST_skippeable] | AST_modificador_objeto
  modificador = AST_modificador_objeto_acceso(campo)
  modificador.apertura(s)
  modificador.modificador_adicional(opt_adicional)
  p[0] = modificador

def p_indexacion_objeto(p): # AST_modificador_objeto_index | AST_tipo_lista
  '''
  indexacion : ABRE_CORCHETE s continuacion_abre_corchete
  '''
  abre = AST_sintaxis(p[1])   # AST_sintaxis
  s = concatenar(abre, p[2])  # [AST_skippeable]
  rec = p[3]                  # AST_modificador_objeto_index | AST_tipo_lista
  rec.apertura(s)
  p[0] = rec

def p_indexacion_objeto_no_tipada(p): # AST_modificador_objeto_index | AST_tipo_lista
  '''
  indexacion_no_tipada : ABRE_CORCHETE s continuacion_abre_corchete_no_tipada
  '''
  abre = AST_sintaxis(p[1])   # AST_sintaxis
  s = concatenar(abre, p[2])  # [AST_skippeable]
  rec = p[3]                  # AST_modificador_objeto_index | AST_tipo_lista
  rec.apertura(s)
  p[0] = rec

def p_invocacion(p): # AST_argumentos
  '''
  invocacion : ABRE_PAREN s argumentos
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  argumentos = p[3]           # AST_argumentos
  argumentos.apertura(s)
  p[0] = argumentos

def p_invocacion_no_tipada(p): # AST_argumentos
  '''
  invocacion_no_tipada : ABRE_PAREN s argumentos_no_tipados
  '''
  abre = AST_sintaxis(p[1])
  s = concatenar(abre, p[2])  # [AST_skippeable]
  argumentos = p[3]           # AST_argumentos
  argumentos.apertura(s)
  p[0] = argumentos

def p_iteracion(p): # AST_iterador
  '''
  iteracion : iterador s expresion
  '''
  iterador = AST_sintaxis(p[1])     # AST_sintaxis
  s = concatenar(iterador, p[2])    # [AST_skippeable]
  expresion = p[3]                  # AST_expresion
  iterador = AST_iterador(expresion)
  iterador.apertura(s)
  p[0] = iterador

def p_comotipo(p): # AST_decorador_comotipo
  '''
  comotipo : AS s tipo
  '''
  s = AST_sintaxis(p[1])
  s = concatenar(s, p[2])                        # [AST_skippeable]
  tipo = p[3]                                    # AST_tipo
  tipo.apertura(s)
  modificador = AST_decorador_comotipo(tipo)   # AST_decorador_comotipo
  p[0] = modificador

def p_flecha(p): # AST_cuerpo | AST_tipo_void
  '''
  flecha : FLECHA s cuerpo_abstraccion
  '''
  s = AST_sintaxis(p[1])  # AST_sintaxis
  s = concatenar(s, p[2]) # [AST_skippeable]
  cuerpo = p[3]           # AST_cuerpo | AST_tipo_void
  cuerpo.apertura(s)
  p[0] = cuerpo

def p_decorador_y_flecha(p): # AST_decorador_tipo
  '''
  decorador_y_flecha : decorador_tipo flecha
  '''
  decorador = p[1]        # AST_decorador_tipo
  flecha = p[2]           # AST_cuerpo | AST_tipo_void
  decorador.modificador_adicional(flecha)
  p[0] = decorador

def p_decorador_tipo(p): # AST_decorador_tipo
  '''
  decorador_tipo : DOS_PUNTOS s tipo s opt_is
  '''
  abre = AST_sintaxis(p[1])       # AST_sintaxis
  abre = concatenar(abre, p[2])   # [AST_skippeable]
  tipo = p[3]                     # AST_tipo
  cierra = p[4]                   # [AST_skippeable]
  opt_adicional = p[5]            # AST_decorador_tipo | [AST_skippeable]
  if isinstance(opt_adicional, AST_decorador_tipo):
    opt_adicional.apertura(cierra)
    tipo.nuevo_alias(opt_adicional)
  else:
    cierra = concatenar(cierra, opt_adicional)
    tipo.clausura(cierra)
  tipo = AST_decorador_tipo(tipo)
  tipo.apertura(abre)
  p[0] = tipo

def p_decorador_tipo_tupla(p): # AST_decorador_tipo
  '''
  decorador_tipo_tupla : tipo_tupla
  '''
  tipo_tupla = p[1]                 # AST_tipo_tupla
  p[0] = AST_decorador_tipo(tipo_tupla)

def p_tipo_con_pipe(p): # AST_tipo_suma
  '''
  tipo_con_pipe : PIPE s tipo
  '''
  s = AST_sintaxis(p[1])                  # AST_sintaxis
  s = concatenar(s, p[2])                 # [AST_skippeable]
  tipo_rec = p[3]                         # AST_tipo
  if not (type(tipo_rec) is AST_tipo_suma):
    tipo_rec = AST_tipo_suma([tipo_rec])
  tipo_rec.apertura(s)
  p[0] = tipo_rec

def p_tipo_con_and(p): # AST_tipo_producto
  '''
  tipo_con_and : AND s tipo
  '''
  s = AST_sintaxis(p[1])                  # AST_sintaxis
  s = concatenar(s, p[2])                 # [AST_skippeable]
  tipo_rec = p[3]                         # AST_tipo
  if not (type(tipo_rec) is AST_tipo_producto):
    tipo_rec = AST_tipo_producto([tipo_rec])
  tipo_rec.apertura(s)
  p[0] = tipo_rec

def p_tipo_con_lista(p): # AST_tipo_lista
  '''
  tipo_con_lista : ABRE_CORCHETE CIERRA_CORCHETE
  '''
  s = AST_sintaxis(p[1])                  # AST_sintaxis
  s = concatenar(s, AST_sintaxis(p[2]))   # [AST_skippeable]
  lista = AST_tipo_lista()
  lista.clausura(s)
  p[0] = lista

def p_decorador_default(p): # AST_decorador_default
  '''
  decorador_default : asignacion
  '''
  asignacion = p[1]                 # AST_modificador_asignacion
  expresion = asignacion.expresion
  expresion.imitarEspaciosYDecoradores(asignacion)
  p[0] = AST_decorador_default(expresion)

def modificador_opcional(p):
  resultado = p[1]
  if len(p) == 3:
    if isinstance(p[2], AST_nodo):
      resultado = p[2]
      resultado.apertura(p[1])
    else:
      resultado = concatenar(p[1], p[2])
  return resultado

class AST_nodo(object):
  def __init__(self):
    self.cierra = []
    self.abre = []
    self.decoradores_pre = []
    self.decoradores = []
  def imitarEspaciosYDecoradores(self, otro):
    self.imitarDecoradores(otro)
    self.imitarEspacios(otro)
  def imitarDecoradores(self, otro):
    self.imitarDecoradoresPre(otro)
    self.imitarDecoradoresPost(otro)
  def imitarDecoradoresPre(self, otro):
    for decorador in reversed(otro.decoradores_pre):
      self.agregar_decorador_pre(decorador)
  def imitarDecoradoresPost(self, otro):
    for decorador in otro.decoradores:
      self.agregar_decorador(decorador)
  def anularEspacios(self):
    self.abre = []
    self.cierra = []
  def imitarEspacios(self, otro):
    self.imitarEspaciosA(otro)
    self.imitarEspaciosC(otro)
  def imitarEspaciosA(self, otro):
    self.abre = otro.abre + self.abre
  def imitarEspaciosC(self, otro):
    self.cierra = self.cierra + otro.cierra
  def agregar_decorador_pre(self, decorador):
    decorador.clausura(self.abre)
    self.abre = []
    self.decoradores_pre.insert(0, decorador)
  def agregar_decorador(self, decorador):
    decorador.apertura(self.cierra)
    self.cierra = []
    self.decoradores.append(decorador)
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
    return f"{''.join(map(restore, self.abre))}{''.join(map(restore, self.decoradores_pre))}{contenido}{''.join(map(restore, self.decoradores))}{''.join(map(restore, self.cierra))}"

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

class AST_salto(AST_skippeable):
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
    if isinstance(otro, AST_nodo):
      self.adicional.append(otro)
    elif len(self.adicional) > 0:
      self.adicional[-1].clausura(otro)
    else:
      self.clausura(otro)

class AST_declaracion_funcion(AST_declaracion):
  def __init__(self, nombre, funcion_incompleta):
    super().__init__()
    self.nombre = nombre                                    # AST_identificador
    self.parametros = funcion_incompleta.parametros         # AST_parametros
    self.cuerpo = funcion_incompleta.cuerpo                 # AST_cuerpo
    self.imitarEspaciosYDecoradores(funcion_incompleta)
  def __str__(self):
    return f"DeclaraciónFunción : {show(self.nombre)}"
  def restore(self):
    return super().restore(f"{restore(self.nombre)}{restore(self.parametros)}{restore(self.cuerpo)}")

class AST_declaracion_clase(AST_declaracion):
  def __init__(self, nombre, definicion):
    super().__init__()
    self.nombre = nombre            # AST_tipo
    self.definicion = definicion    # AST_cuerpo
  def __str__(self):
    return f"Declaración clase : {show(self.nombre)}"
  def restore(self):
    return super().restore(f"{restore(self.nombre)}{restore(self.definicion)}")

class AST_declaracion_tipo(AST_declaracion):
  def __init__(self, nombre, definicion):
    super().__init__()
    self.nombre = nombre            # AST_tipo
    self.definicion = definicion    # AST_tipo
  def __str__(self):
    return f"Declaración tipo : {show(self.nombre)}"
  def restore(self):
    return super().restore(f"{restore(self.nombre)}{restore(self.definicion)}")

class AST_cuerpo(AST_modificador):
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

class AST_expresion_lista(AST_expresion):
  def __init__(self, elementos):
    super().__init__()
    self.elementos = elementos        # AST_elementos
  def __str__(self):
    return f"Objeto : {show(self.elementos)}"
  def restore(self):
    return super().restore(f"{restore(self.elementos)}")

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
    self.parametros = funcion_incompleta.parametros     # AST_parametros
    self.cuerpo = funcion_incompleta.cuerpo             # AST_cuerpo
    self.imitarEspaciosYDecoradores(funcion_incompleta)
  def __str__(self):
    return f"FunciónAnónima {show(self.cuerpo)}"
  def restore(self):
    return super().restore(f"{restore(self.parametros)}{restore(self.cuerpo)}")

class AST_declaracion_variable(AST_declaracion):
  def __init__(self, nombre, asignacion=None):
    super().__init__()
    self.nombre = nombre          # AST_identificador
    self.asignacion = asignacion  # AST_expresion
    self.otros = []               # [AST_declaracion_variable]
  def identificador_adicional(self, declaracion):
    self.otros.append(declaracion)
  def asignar(self, expresion):
    self.asignacion = expresion
  def __str__(self):
    valor = "" if (self.asignacion is None) else " = " + show(self.asignacion)
    mas = ""
    for o in self.otros:
      mas += f" {show(o.nombre)}"
      if not(o.asignacion is None):
        mas += f" = {show(o.asignacion)}"
    return f"DeclaraciónVariable : {show(self.nombre)}{valor}{mas}"
  def restore(self):
    return super().restore(f"{restore(self.nombre)}{restore(self.asignacion)}{restore(self.otros)}")

class AST_invocacion(AST_expresion):
  def __init__(self, funcion, argumentos):
    super().__init__()
    if type(funcion) is AST_funcion_incompleta:
      self.funcion = crearExpresionFuncion(funcion) # AST_identificador | AST_expresion_funcion
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
    self.campo = modificador_campo.campo  # AST_identificador | AST_argumentos
    self.campo.imitarEspaciosYDecoradores(modificador_campo)
  def __str__(self):
    return f"Acceso : {show(self.objeto)}.{show(self.campo)}"
  def restore(self):
    return super().restore(f"{restore(self.objeto)}{restore(self.campo)}")

class AST_expresion_index(AST_expresion):
  def __init__(self, objeto, modificador_indice):
    super().__init__()
    self.objeto = objeto                      # AST_expresion
    self.indice = modificador_indice.indice   # AST_expresion
    self.indice.imitarEspaciosYDecoradores(modificador_indice)
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
    if isinstance(cuerpo, AST_cuerpo):
      cuerpo.apertura(self.cierra)
      self.cierra = []
      self.cuerpo = cuerpo        # AST_cuerpo
    else:
      self.clausura(cuerpo)
  def __str__(self):
    return f"{self.clase} : {show(self.expresion)} {show(self.cuerpo)}"
  def restore(self):
    return super().restore(f"{restore(self.expresion)}{restore(self.cuerpo)}")

class AST_operador(AST_expresion):
  def __init__(self, izq, op, der, other=None): # El último es para el ternario
    super().__init__()
    self.izq = izq        # AST_expresion | None
    self.op = op          # string
    self.der = der        # AST_expresion | None
    self.other = other    # AST_expresion | None
    self.parentesis = False
  def esBinario(self):
    return (self.other is None) and not (self.izq is None) and not (self.der is None)
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
    if self.other is None:
      if self.der is None:
        self.izq.clausura(c)
      else:
        self.der.clausura(c)
    else:
      self.other.clausura(c)
  def __str__(self):
    resultado = ""
    if not (self.izq is None):
      resultado += f" {show(self.izq)}"
    resultado += "?" if self.op == "?:" else self.op;
    if not (self.der is None):
      resultado += f" {show(self.der)}"
    if self.op == "?:" and not (self.other is None):
      resultado += f" : {show(self.other)}"
    return f"{resultado}"
  def restore(self):
    return super().restore(f"{restore(self.izq)}{restore(self.der)}{restore(self.other)}")

class AST_parametros(AST_declaracion):
  def __init__(self, parametros, decoradores=[]):
    super().__init__()
    self.parametros = parametros            # [AST_identificador | AST_expresion_lista]
    self.decoradoresProximoParametro = []   # [AST_decorador]
    self.decoradoresFuncion = []            # [AST_decorador]
    for decorador in decoradores:           # Tengo que hacer una copia de la lista para que no quede linkeada
      self.decoradoresFuncion.append(decorador)
  def primerParametro(self, parametro):
    for decorador in self.decoradoresProximoParametro:
      parametro = aplicarModificador(parametro, decorador)
    self.parametros.insert(0, parametro)
    self.decoradoresProximoParametro = []
  def agregar_decorador_parametro(self, decorador):
    adicionales = decorador.adicional
    decorador.adicional = []
    self.decoradoresProximoParametro.append(decorador)
    for ad in adicionales:
      if not isinstance(ad, AST_decorador):
        fallaDebug()
      self.agregar_decorador_parametro(ad)
  def agregar_decorador_funcion(self, decorador):
    adicionales = decorador.adicional
    decorador.adicional = []
    self.decoradoresFuncion.append(decorador)
    for ad in adicionales:
      if not isinstance(ad, AST_decorador):
        fallaDebug()
      self.agregar_decorador_funcion(ad)
  def __str__(self):
    return f"Parámetros : {show(self.parametros)}"
  def restore(self):
    return super().restore(f"{''.join(map(restore, self.parametros))}") + f"{restore(self.decoradoresFuncion)}"

class AST_campo(AST_declaracion):
  def __init__(self, clave, valor):
    super().__init__()
    self.clave = clave  # AST_identificador | AST_declaracion_funcion | ¿AST_invocacion? | AST_expresion_literal (string)
    self.valor = valor  # AST_expresion | None
  def __str__(self):
    valor = '' if self.valor is None else f":{show(self.valor)}"
    return f"{show(self.clave)}{show(valor)}"
  def restore(self):
    return super().restore(f"{restore(self.clave)}{restore(self.valor)}")

class AST_campos(AST_declaracion):
  def __init__(self):
    super().__init__()
    self.lista = []  # [AST_campo]
    self.tmp = None
  def agregar_campo(self, campo):
    if not (self.tmp is None):
      campo.clausura(self.tmp)
      self.tmp = None
    self.lista.insert(0, campo)
  def cantidad(self):
    return len(self.lista)
  def apertura(self, c):
    if self.cantidad() > 0:
      self.lista[0].apertura(c)
    else:
      self.tmp = c
  def __str__(self):
    return f"{show(self.lista)}"
  def restore(self):
    return super().restore(f"{restore(self.lista)}")

class AST_argumentos(AST_modificador):
  def __init__(self):
    super().__init__()
    self.lista = []  # [AST_expresion]
    self.tmp = []
  def agregar_argumento(self, arg):
    if len(self.tmp) > 0:
      arg.clausura(self.tmp)
      self.tmp = []
    self.lista.insert(0, arg)
  def apertura(self, s):
    if len(self.lista) > 0:
      self.lista[0].apertura(s)
    else:
      self.tmp = concatenar(s, self.tmp)
  def cantidad(self):
    return len(self.lista)
  def __str__(self):
    return f"{show(self.lista)}"
  def restore(self):
    return super().restore(f"{restore(self.tmp)}{restore(self.lista)}")

class AST_elementos(AST_modificador):
  def __init__(self):
    super().__init__()
    self.lista = []  # [AST_expresion]
    self.tmp = []
  def agregar_elemento(self, arg):
    if len(self.tmp) > 0:
      arg.clausura(self.tmp)
      self.tmp = []
    self.lista.insert(0, arg)
  def apertura(self, s):
    if len(self.lista) > 0:
      self.lista[0].apertura(s)
    else:
      self.tmp = concatenar(s, self.tmp)
  def cantidad(self):
    return len(self.lista)
  def __str__(self):
    return f"{show(self.lista)}"
  def restore(self):
    return super().restore(f"{restore(self.tmp)}{restore(self.lista)}")

class AST_modificador_asignacion(AST_modificador):
  def __init__(self, expresion):
    super().__init__()
    self.expresion = expresion
  def restore(self):
    return super().restore(f"{restore(self.expresion)}")

class AST_asignable(AST_declaracion):
  def __init__(self):
    super().__init__()

class AST_identificador(AST_asignable):
  def __init__(self, identificador):
    super().__init__()
    self.identificador = identificador    # String
    self.esModificador = es_identificador_sp(identificador)
  def __str__(self):
    return f"{self.identificador}"
  def restore(self):
    return super().restore(f"{self.identificador}")

class AST_identificadores(AST_asignable):
  def __init__(self, identificadores):
    super().__init__()
    self.identificadores = identificadores # [AST_identificador]
    self.tmp = []
  def agregar_decorador(self, decorador):
    if len(self.identificadores) > 0:
      self.identificadores[-1] = aplicarModificador(self.identificadores[-1], decorador)
    else:
      self.tmp.append(decorador)
  def __str__(self):
    return f"{show(self.identificadores)}"
  def restore(self):
    return super().restore(f"{''.join(map(restore, self.identificadores))}")

class AST_indexacion_clase(AST_asignable):
  def __init__(self, identificador):
    super().__init__()
    self.identificador = identificador    # AST_identificador
  def __str__(self):
    return f"[{show(self.identificador)}]"
  def restore(self):
    return super().restore(f"{restore(self.identificador)}")

class AST_identificador_objeto(AST_asignable):
  def __init__(self, campos):
    super().__init__()
    self.campos = campos        # AST_campos
  def __str__(self):
    return f"{show(self.campos)}"
  def restore(self):
    return super().restore(f"{restore(self.campos)}")

class AST_import(AST_declaracion):
  def __init__(self, archivo, importables=None, opt_alias=[], es_tipo=False):
    super().__init__()
    self.archivo = archivo          # AST_expresion_literal
    self.importables = importables  # AST_identificador | AST_identificadores | AST_sintaxis | None
    self.opt_alias = opt_alias      # AST_identificador | [AST_skippeable]
    self.es_tipo = es_tipo          # Bool
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
    self.parametros = parametros          # AST_parametros
    if isinstance(cuerpo, AST_cuerpo):
      self.cuerpo = cuerpo                # AST_cuerpo
    else:
      self.cuerpo = AST_cuerpo([])
      self.clausura(cuerpo)
  def agregar_decorador(self, decorador):
    self.parametros.agregar_decorador_funcion(decorador)

class AST_decorador(AST_modificador):
  def __init__(self):
    super().__init__()

class AST_decorador_tipo(AST_decorador):
  def __init__(self, tipo):
    super().__init__()
    adicionales = tipo.adicional
    tipo.adicional = []
    for m in adicionales:
      tipo = aplicarModificador(tipo, m)
    self.tipo = tipo                      # AST_tipo
  def restore(self):
    return super().restore(f"{restore(self.tipo)}")

class AST_decorador_subtipo(AST_decorador):
  def __init__(self, tipo):
    super().__init__()
    adicionales = tipo.adicional
    tipo.adicional = []
    for m in adicionales:
      tipo = aplicarModificador(tipo, m)
    self.tipo = tipo                      # AST_tupla
  def restore(self):
    return super().restore(f"{restore(self.tipo)}")

class AST_decorador_opcional(AST_decorador):
  def __init__(self):
    super().__init__()
  def restore(self):
    return super().restore("")

class AST_decorador_default(AST_decorador):
  def __init__(self, default):
    super().__init__()
    self.default = default      # AST_expresion
  def restore(self):
    return super().restore(f"{restore(self.default)}")

class AST_decorador_alias(AST_decorador):
  def __init__(self, alias):
    super().__init__()
    self.alias = alias          # AST_identificador
  def restore(self):
    return super().restore(f"{restore(self.alias)}")

class AST_decorador_comotipo(AST_decorador):
  def __init__(self, tipo):
    super().__init__()
    self.tipo = tipo          # AST_tipo
  def restore(self):
    return super().restore(f"{restore(self.tipo)}")

class AST_decorador_keyword(AST_decorador):
  def __init__(self, identificador):
    super().__init__()
    self.identificador = identificador    # AST_identificador
  def restore(self):
    return super().restore(f"{restore(self.identificador)}")

class AST_decorador_implementacion(AST_decorador):
  def __init__(self, nombre):
    super().__init__()
    self.nombre = nombre          # AST_tipo | [AST_tipo]
  def restore(self):
    return super().restore(f"{restore(self.nombre)}")

class AST_decorador_extension(AST_decorador):
  def __init__(self, nombre):
    super().__init__()
    self.nombre = nombre          # AST_tipo
  def restore(self):
    return super().restore(f"{restore(self.nombre)}")

class AST_modificador_operador_binario(AST_modificador_operador):
  def __init__(self, clase, expresion):
    super().__init__()
    self.clase = clase          # string
    self.expresion = expresion  # AST_expresion

class AST_modificador_operador_ternario(AST_modificador_operador):
  def __init__(self, expresion1, expresion2):
    super().__init__()
    self.expresion1 = expresion1  # AST_expresion
    self.expresion2 = expresion2  # AST_expresion

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
    self.campo = identificador    # AST_identificador | AST_argumentos

class AST_modificador_objeto_index(AST_modificador_objeto):
  def __init__(self, expresion):
    super().__init__()
    self.indice = expresion       # AST_expresion

class AST_iterador(AST_modificador):
  def __init__(self, expresion):
    super().__init__()
    self.expresion = expresion    # AST_expresion

class AST_modificador_variable_adicional(AST_modificador):
  def __init__(self, identificador):
    super().__init__()
    self.declaracion = AST_declaracion_variable(identificador)    # AST_declaracion_variable
  def modificador_adicional(self, otro):
    if isinstance(otro, AST_modificador_asignacion):
      expresion = otro.expresion
      expresion.imitarEspaciosYDecoradores(otro)
      self.asignar(expresion)
    else:
      super().modificador_adicional(otro)
  def asignar(self, expresion):
    self.declaracion.asignar(expresion)

class AST_format_string(AST_expresion):
  def __init__(self, completo):
    super().__init__()
    # TODO: parsing auxiliar para identificar las expresiones dentro de "completo". Luego eliminar el campo self.tmp y la primera línea de la función restore
    self.elementos = []    # [AST_expresion]
    self.tmp = completo
  def restore(self):
    return super().restore(f"{self.tmp}")
    return super().restore(f"{''.join(map(restore, self.elementos))}")

class AST_tipo(AST_modificador):
  def __init__(self):
    super().__init__()
    self.alias = []
  def nuevo_alias(self, otro):
    self.alias.append(otro)
  def restore(self,contenido=''):
    return super().restore(f"{contenido}{restore(self.alias)}")

class AST_tipo_base(AST_tipo):
  def __init__(self, base):
    super().__init__()
    self.base = base                    # AST_identificador | AST_expresion_acceso | string
  def __str__(self):
    return f"Tipo : {show(self.base)}"
  def restore(self):
    return super().restore(f"{restore(self.base)}")

class AST_tipo_lista(AST_tipo):
  def __init__(self):
    super().__init__()
    self.rec = None
  def __str__(self):
    return f"Tipo : [{show(self.rec)}]"
  def set_rec(self, rec):
    self.rec = rec
    self.rec.clausura(self.abre)
    self.rec.clausura(self.cierra)
    self.anularEspacios()
  def restore(self):
    return super().restore(f"{restore(self.rec)}")

class AST_tipo_objeto(AST_tipo):
  def __init__(self, campos):
    super().__init__()
    self.campos = campos                # AST_campos_tipo
  def __str__(self):
    return f"Tipo : {show(self.campos)}"
  def restore(self):
    return super().restore(f"{restore(self.campos)}")

class AST_tipo_flecha(AST_tipo):
  def __init__(self, parametros, tipo_salida):
    super().__init__()
    self.parametros = parametros        # AST_parametros
    self.tipo_salida = tipo_salida      # AST_tipo
  def primerParametro(self, parametro):
    self.parametros.primerParametro(parametro)
  def __str__(self):
    return f"Tipo : {show(self.parametros)} => {show(self.tipo_salida)}"
  def restore(self):
    return super().restore(f"{restore(self.parametros)}{restore(self.tipo_salida)}")

class AST_tipo_suma(AST_tipo):
  def __init__(self, sub_tipos):
    super().__init__()
    self.sub_tipos = sub_tipos          # [AST_tipo]
  def o(self, o):
    self.sub_tipos.insert(0, o)
  def cantidad(self):
    return len(self.sub_tipos)
  def apertura(self, c):
    if self.cantidad() > 0:
      self.sub_tipos[0].apertura(c)
    else:
      self.clausura(c)
  def __str__(self):
    return f"Tipo : {' | '.join(list(map(show, self.sub_tipos)))}"
  def restore(self):
    return super().restore(f"{restore(self.sub_tipos)}")

class AST_tipo_producto(AST_tipo):
  def __init__(self, sub_tipos):
    super().__init__()
    self.sub_tipos = sub_tipos          # [AST_tipo]
  def y(self, y):
    self.sub_tipos.insert(0, y)
  def cantidad(self):
    return len(self.sub_tipos)
  def apertura(self, c):
    if self.cantidad() > 0:
      self.sub_tipos[0].apertura(c)
    else:
      self.clausura(c)
  def __str__(self):
    return f"Tipo : {' & '.join(list(map(show, self.sub_tipos)))}"
  def restore(self):
    return super().restore(f"{restore(self.sub_tipos)}")

class AST_tipo_tupla(AST_tipo):
  def __init__(self, sub_tipos=[]):
    super().__init__()
    self.sub_tipos = sub_tipos          # [AST_tipo]
  def fst(self, t):
    self.sub_tipos.insert(0, t)
  def cantidad(self):
    return len(self.sub_tipos)
  def apertura(self, c):
    if self.cantidad() > 0:
      self.sub_tipos[0].apertura(c)
    else:
      self.clausura(c)
  def __str__(self):
    return f"Tipo : <{', '.join(list(map(show, self.sub_tipos)))}>"
  def restore(self):
    return super().restore(f"{restore(self.sub_tipos)}")

class AST_tipo_compuesto(AST_tipo):
  def __init__(self, base, sub_tipos):
    super().__init__()
    self.base = base                    # AST_tipo_base
    self.sub_tipos = sub_tipos          # AST_tupla
  def __str__(self):
    return f"Tipo : {self.base}<{', '.join(list(map(show, self.sub_tipos.sub_tipos)))}>"
  def restore(self):
    return super().restore(f"{restore(self.base)}{restore(self.sub_tipos)}")

class AST_tipo_varios(AST_tipo):
  def __init__(self, sub_tipos):
    super().__init__()
    self.sub_tipos = sub_tipos          # [AST_tipo]
  def agregar_tipo(self, o):
    self.sub_tipos.insert(0, o)
  def cantidad(self):
    return len(self.sub_tipos)
  def apertura(self, c):
    if self.cantidad() > 0:
      self.sub_tipos[0].apertura(c)
    else:
      self.clausura(c)
  def __str__(self):
    return f"Tipo : {' , '.join(list(map(show, self.sub_tipos)))}"
  def restore(self):
    return super().restore(f"{restore(self.sub_tipos)}")

class AST_tipo_derivado(AST_tipo):
  def __init__(self, expresion):
    super().__init__()
    self.expresion = expresion        # AST_expresion
  def __str__(self):
    return f"El tipo de {show(self.expresion)}"
  def restore(self):
    return super().restore(f"{restore(self.expresion)}")

class AST_tipo_void(AST_tipo):
  def __init__(self):
    super().__init__()
  def __str__(self):
    return f"VOID"
  def restore(self):
    return super().restore()

class AST_campos_tipo(AST_declaracion):
  def __init__(self):
    super().__init__()
    self.lista = []            # [AST_campo_tipo]
  def agregar_campo(self, campo):
    self.lista.insert(0, campo)
  def cantidad(self):
    return len(self.lista)
  def apertura(self, c):
    if self.cantidad() > 0:
      self.lista[0].apertura(c)
    else:
      self.cierra = concatenar(c, self.cierra)
  def __str__(self):
    return f"{show(self.lista)}"
  def restore(self):
    return super().restore(f"{restore(self.lista)}")

class AST_campo_tipo(AST_declaracion):
  def __init__(self, clave, tipo):
    super().__init__()
    self.clave = clave  # AST_identificador | AST_expresion_literal (string) | None
    self.tipo = tipo    # AST_tipo
  def __str__(self):
    clave = "" if (self.clave is None) else f"{show(self.clave)}:"
    return f"{clave}{show(self.tipo)}"
  def restore(self):
    return super().restore(f"{restore(self.clave)}{restore(self.tipo)}")

class AST_return(AST_declaracion):
  def __init__(self, expresion):
    super().__init__()
    self.expresion = expresion  # AST_expresion | [AST_skippeable]
  def __str__(self):
    resultado = f" {show(self.expresion)}" if isinstance(self.expresion, AST_expresion) else ""
    return f"Return {resultado}"
  def restore(self):
    return super().restore(f"{restore(self.expresion)}")

class AST_expresion_new(AST_expresion):
  def __init__(self, tipo):
    super().__init__()
    self.tipo = tipo      # AST_tipo
  def __str__(self):
    return f"New {show(self.tipo)}"
  def restore(self):
    return super().restore(f"{restore(self.tipo)}")

class AST_programa(AST_nodo):
  def __init__(self, declaraciones):
    super().__init__()
    self.declaraciones = sanitizar(declaraciones)   # [AST_nodo]
  def __str__(self):
    return '\n'.join(list(map(show, self.declaraciones)))
  def restore(self):
    return super().restore(f"{''.join(map(restore, self.declaraciones))}")

class AST_TMP(AST_nodo):
  def __init__(self, identificador, contenido, rec=None):
    super().__init__()
    self.identificador = identificador
    self.contenido = contenido
    self.rec = rec

def aplicarModificador(nodo, mod):
  resultado = nodo
  adicionales = []
  if isinstance(mod, AST_modificador):
    adicionales = mod.adicional
    mod.adicional = []
  if type(mod) is AST_modificador_objeto_acceso:
    if isinstance(nodo, AST_tipo):
      # TIPO {nodo}.{mod}
      nodo.base = AST_expresion_acceso(nodo.base, mod)
    else:
      # ACCESO OBJETO: {nodo}.{mod}
      resultado = AST_expresion_acceso(nodo, mod)
  elif type(mod) is AST_modificador_objeto_index:
    # INDEX OBJETO: {nodo} [ {mod} ]
    resultado = AST_expresion_index(nodo, mod)
  elif isinstance(mod, AST_modificador_operador_binario):
    # OPERACIÓN: {nodo} + {mod}
    mod.expresion.imitarEspaciosYDecoradores(mod)
    resultado = AST_operador(nodo, mod.clase, mod.expresion)
  elif isinstance(mod, AST_modificador_operador_ternario):
    # OPERACIÓN: {nodo} { ? .. : .. }
    mod.expresion1.imitarEspaciosA(mod)
    mod.expresion2.imitarEspaciosC(mod)
    resultado = AST_operador(nodo, "?:", mod.expresion1, mod.expresion2)
  elif isinstance(mod, AST_modificador_operador_posfijo):
    # OPERACIÓN: {nodo} {mod}
    nodo.clausura(AST_sintaxis(mod.restore()))
    resultado = AST_operador(nodo, mod.clase, None)
  elif isinstance(mod, AST_argumentos):
    # INVOCACIÓN: {nodo} ( {mod} )
    resultado = AST_invocacion(nodo, mod)
  elif isinstance(mod, AST_funcion_incompleta):
    # DECLARACIÓN (dentro de clase): {nodo} ( {mod.parametros} ) { {mod.cuerpo} }
    resultado = crearDeclaracionFuncion(nodo, mod)
  elif isinstance(mod, AST_modificador_variable_adicional):
    # DECLARACIÓN CON MÁS VARIABLES: {nodo} , {mod}
    declaracion = mod.declaracion
    declaracion.imitarEspaciosYDecoradores(mod)
    resultado.identificador_adicional(declaracion)
  elif isinstance(mod, AST_decorador):
    # DECORADOR: {nodo} : {mod} | {nodo} ? | {nodo} = {mod} | {nodo} as {mod} | {nodo} extends {mod} | {nodo} implements {mod}
    resultado.agregar_decorador(mod)
  elif type(mod) is AST_tipo_lista:
    # TIPO LISTA: {nodo} []
    tipo_rec = tipoDesdeNodo(nodo)
    mod.set_rec(tipo_rec)
    resultado = mod
  elif type(mod) is AST_tipo_suma:
    # TIPO SUMA: {nodo} | {mod}
    mod.o(nodo)
    resultado = mod
  elif type(mod) is AST_tipo_producto:
    # TIPO PRODUCTO: {nodo} & {mod}
    mod.y(nodo)
    resultado = mod
  elif type(mod) is AST_tipo_tupla:
    # TIPO COMPUESTO: {nodo} < {mod} >
    tipo_base = tipoDesdeNodo(nodo)
    resultado = AST_tipo_compuesto(tipo_base, mod)
  elif isinstance(mod, AST_tipo_void):
    parametros = parametrosDesdeNodo(nodo)
    resultado = AST_tipo_flecha(parametros, mod)
  elif isinstance(mod, AST_cuerpo):
    # FUNCIÓN ANÓNIMA: {nodo} => {mod}
    parametros = parametrosDesdeNodo(nodo)
    resultado = crearExpresionFuncion(AST_funcion_incompleta(parametros, mod))
  elif isinstance(mod, AST_iterador):
    # ITERACIÓN: {nodo} in {mod}
    mod.expresion.imitarEspaciosYDecoradores(mod)
    resultado = AST_iteracion(nodo, mod.expresion)
  elif isinstance(mod, AST_modificador_asignacion):
    expresion = mod.expresion
    expresion.imitarEspaciosYDecoradores(mod)
    if isinstance(nodo, AST_declaracion_variable) or isinstance(nodo, AST_modificador_variable_adicional):
      # ASIGNACIÓN VARIABLE: Var {nodo} = {mod}
      resultado.asignar(expresion)
    else:
      # ASIGNACIÓN GENÉRICA: {nodo} = {mod}
      resultado = AST_asignacion(nodo, expresion)
  else: # [AST_skippeable]
    if isinstance(mod, AST_nodo):
      # ERROR
      fallaDebug()
    resultado.clausura(mod)
  for ad in adicionales:
    resultado = aplicarModificador(resultado, ad)
  return resultado

def parametrosDesdeNodo(nodo):
  parametros = None
  identificador = nodo
  if type(identificador) is AST_expresion_identificador:
    identificador = nodo.identificador
    identificador.imitarEspaciosYDecoradores(nodo)
  if type(identificador) is AST_identificador:
    identificadores = [identificador]
    parametros = AST_parametros(identificadores)
  elif type(nodo) is AST_expresion_lista:
    lista = nodo
    decoradores = lista.decoradores
    lista.decoradores = []
    lista = [lista]
    parametros = AST_parametros(lista, decoradores)
  elif isinstance(nodo, AST_parametros):
    parametros = nodo
  elif isinstance(nodo, AST_nodo):
    print(f"ERROR : no se puede usar un tipo {type(nodo)} como parámetros de una función anónima")
    exit(0)
  return parametros

def tipoDesdeNodo(nodo):
  tipo = None
  if isinstance(nodo, AST_tipo):
    tipo = nodo
  elif isinstance(nodo, AST_expresion_lista):
    elementos = nodo.elementos
    tipo = AST_tipo_varios(list(map(tipoDesdeNodo, elementos.lista)))
    tipo.imitarEspaciosYDecoradores(elementos)
    tipo.imitarEspaciosYDecoradores(nodo)
  elif isinstance(nodo, AST_expresion_identificador):
    identificador = nodo.identificador
    tipo = AST_tipo_base(identificador)
    tipo.imitarEspaciosYDecoradores(nodo)
  elif isinstance(nodo, AST_identificador):
    tipo = AST_tipo_base(nodo)
  elif isinstance(nodo, AST_operador):
    if nodo.op == '|':
      tipo = AST_tipo_suma(list(map(tipoDesdeNodo, [nodo.izq, nodo.der])))
      tipo.imitarEspaciosYDecoradores(nodo)
  else:
    # ERROR
    fallaDebug()
  return tipo

def crearDeclaracionFuncion(nombre, funcion_incompleta):
  adicionales = funcion_incompleta.adicional
  funcion_incompleta.adicional = []
  declaracion = AST_declaracion_funcion(nombre, funcion_incompleta)
  for ad in adicionales:
    declaracion = aplicarModificador(declaracion, ad)
  return declaracion

def crearExpresionFuncion(funcion_incompleta):
  adicionales = funcion_incompleta.adicional
  funcion_incompleta.adicional = []
  expresion = AST_expresion_funcion(funcion_incompleta)
  for ad in adicionales:
    expresion = aplicarModificador(expresion, ad)
  return expresion

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

def fallaDebug():
  breakpoint()

parser = yacc()

def parsear(contenido):
  return parser.parse(contenido, lex())

def mostrarTokens(tokens):
  for t in tokens:
    print(fill(str(t.lineno),3) + ":" + fill(str(t.colno),6) + fill(t.type,15) + clean(t.value))

def mostrarAST(ast):
  print(show(ast))

def mostrarDiff(a, b):
  lineas_a = a.split('\n')
  lineas_b = b.split('\n')
  i = 0
  m = min(len(lineas_a), len(lineas_b))
  while i < m and eq_string(lineas_a[i], lineas_b[i]):
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
    pre = 1
    post = 5
    print(f"[{i+1}]")
    print_others(i-pre, i, lineas_a)
    print(f"> {V(lineas_a[i])}")
    print_others(i+1, i+post+1, lineas_a)
    print("--")
    print_others(i-pre, i, lineas_b)
    print(f"> {V(lineas_b[i])}")
    print_others(i+1, i+post+1, lineas_b)

def print_others(desde, hasta, src):
  for i in range(desde, hasta):
    if i >= 0 and i < len(src):
      print(f"  {V(src[i])}")

def V(s):
  return s.replace(' ', '_')

def eq_string(a, b):
  if len(a) != len(b):
    return False
  if len(a) == 1:
    return a[0] == b[0]
  return functools.reduce(lambda x, rec: a[x]==b[x] and rec, range(len(a)), True)

def fill(s,k):
  resultado = s
  while len(resultado) < k:
    resultado += ' '
  return resultado

def clean(s):
  return s.replace('\n','\\n')

def sanitizar(declaraciones):
  resultado = []
  for d in declaraciones:
    if type(d) is AST_identificador:
      decoradores_pre = []
      for p in d.decoradores_pre:
        if type(p) is AST_decorador_keyword and es_identificador_sp(p.identificador.identificador):
          decoradores_pre.append(p)
        else:
          p.decoradores_pre = decoradores_pre
          identificador = p.identificador
          identificador.imitarEspaciosYDecoradores(p)
          resultado.append(identificador)
          decoradores_pre = []
      d.decoradores_pre = decoradores_pre
      resultado.append(d)
    else:
      resultado.append(d)
  return resultado

def logParser():
  print(parser.statestack)
  print(parser.symstack)