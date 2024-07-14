import sys
from parser import tokenizar, parsear
from parser import token as t
from parser import AST_espacios as espacios
from parser import AST_invocacion
from parser import AST_declaracion_variable as variable
from parser import AST_asignacion as asignacion
from parser import AST_acceso
from parser import AST_index
from parser import AST_identificador as identificador
from parser import AST_expresion_literal as literal
from parser import AST_declaracion_funcion
from parser import AST_comentario as comentario
from parser import AST_modificador_objeto_acceso
from parser import AST_modificador_objeto_index

def id(s,i,f):
  return t('IDENTIFICADOR',s,i,f)

def n(s,i,f):
  return t('NUMERO',s,i,f)

def invocacion(funcion, argumentos=[]):
  return AST_invocacion(funcion, argumentos)

def funcion(nombre, parametros, cuerpo):
  return AST_declaracion_funcion(nombre, parametros, cuerpo)

def acceso(objeto, campo):
  return AST_acceso(objeto, AST_modificador_objeto_acceso(identificador(campo)))

def index(objeto, indice):
  return AST_index(objeto, AST_modificador_objeto_index(literal(indice)))

def main():
  if len(sys.argv) > 1:
    ntest = int(sys.argv[1])
    if ntest >= 0 and ntest < len(casos_de_test):
      test = casos_de_test[ntest]
      print(f"{ntest} {test.desc}")
      if evaluar(test):
        exit(1)
      print(f"OK")
      exit(0)
    print(f"Número de test {ntest} inválido. Debe estar entre 0 y {len(casos_de_test)-1}.")
    exit(1)
  i = 0
  for test in casos_de_test:
    if evaluar(test):
      exit(1)
    print(f"{i} {test.desc} OK")
    i += 1
  print("Todos los test pasaron correctamente")
  exit(0)

class Test(object):
  def __init__(self, desc, input, tokens, ast):
    self.desc = desc
    self.input = input
    self.tokens = tokens
    self.ast = ast

casos_de_test = [
  Test("Vacío",
    "",[], []),
  Test("Un comando",
    "hola();",[
    id('hola',1,0),
    t('ABRE_PAREN','(',1,4),
    t('CIERRA_PAREN',')',1,5),
    t('PUNTO_Y_COMA',';',1,6)
  ], [invocacion('hola')
  ]),
  Test("Dos comandos",
    "hola();\nchau();",[
    id('hola',1,0),
    t('ABRE_PAREN','(',1,4),
    t('CIERRA_PAREN',')',1,5),
    t('PUNTO_Y_COMA',';',1,6),
    t('SKIP','\n',1,7),
    id('chau',2,8),
    t('ABRE_PAREN','(',2,12),
    t('CIERRA_PAREN',')',2,13),
    t('PUNTO_Y_COMA',';',2,14)
  ], [invocacion('hola'),
      invocacion('chau')
  ]),
  Test("Blancos",
    " \t\n",[
    t('SKIP',' \t\n',1,0)
  ], [espacios(' \t\n')
  ]),
  Test("Comandos con blancos",
    "\t \t hola();\t \n\t \tchau();  \n\n  ",[
    t('SKIP','\t \t ',1,0),
    id('hola',1,4),
    t('ABRE_PAREN','(',1,8),
    t('CIERRA_PAREN',')',1,9),
    t('PUNTO_Y_COMA',';',1,10),
    t('SKIP','\t \n\t \t',1,11),
    id('chau',2,17),
    t('ABRE_PAREN','(',2,21),
    t('CIERRA_PAREN',')',2,22),
    t('PUNTO_Y_COMA',';',2,23),
    t('SKIP','  \n\n  ',2,24)
  ], [espacios('\t \t '),
      invocacion('hola'),
      invocacion('chau'),
  ]),
  Test("Una variable",
    "\tlet x\t=  5",[
    t('SKIP','\t',1,0),
    t('DECL_VAR','let',1,1),
    t('SKIP',' ',1,4),
    id('x',1,5),
    t('SKIP','\t',1,6),
    t('ASIGNACION','=',1,7),
    t('SKIP','  ',1,8),
    n('5',1,10)
  ], [espacios('\t'),
      variable('x',literal('5'))
  ]),
  Test("Declaración y asignación de variable con strings",
    "const\tx;x =\n'2'x=\"true\"",[
    t('DECL_VAR','const',1,0),
    t('SKIP','\t',1,5),
    id('x',1,6),
    t('PUNTO_Y_COMA',';',1,7),
    id('x',1,8),
    t('SKIP',' ',1,9),
    t('ASIGNACION','=',1,10),
    t('SKIP','\n',1,11),
    t('STRING',"'2'",2,12),
    id('x',2,15),
    t('ASIGNACION','=',2,16),
    t('STRING','"true"',2,17)
  ], [variable('x'),
      asignacion('x',literal("'2'")),
      asignacion('x',literal('"true"'))
  ]),
  Test("Declaración de función",
    "function HOLA() {x=2.5;let y = .66\t;}",[
    t('DECL_FUNC','function',1,0),
    t('SKIP',' ',1,8),
    id('HOLA',1,9),
    t('ABRE_PAREN','(',1,13),
    t('CIERRA_PAREN',')',1,14),
    t('SKIP',' ',1,15),
    t('ABRE_LLAVE','{',1,16),
    id('x',1,17),
    t('ASIGNACION','=',1,18),
    n('2.5',1,19),
    t('PUNTO_Y_COMA',';',1,22),
    t('DECL_VAR','let',1,23),
    t('SKIP',' ',1,26),
    id('y',1,27),
    t('SKIP',' ',1,28),
    t('ASIGNACION','=',1,29),
    t('SKIP',' ',1,30),
    n('.66',1,31),
    t('SKIP','\t',1,34),
    t('PUNTO_Y_COMA',';',1,35),
    t('CIERRA_LLAVE','}',1,36)
  ], [funcion('HOLA',[],[
        asignacion('x',literal('2.5')),
        variable('y',literal('.66'))
    ])
  ]),
  Test("Comentarios",
    "/**/a // b \n// // hola /* */\nc\n/*\n\nhola\n\n*/\nd\n/*\n\nchau\n\n*/",[
    t('COMENTARIO_ML','/**/',1,0),
    id('a',1,4),
    t('SKIP',' ',1,5),
    t('COMENTARIO_UL','// b ',1,6),
    t('SKIP','\n',1,11),
    t('COMENTARIO_UL','// // hola /* */',2,12),
    t('SKIP','\n',2,28),
    id('c',3,29),
    t('SKIP','\n',3,30),
    t('COMENTARIO_ML','/*\n\nhola\n\n*/',4,31),
    t('SKIP','\n',8,43),
    id('d',9,44),
    t('SKIP','\n',9,45),
    t('COMENTARIO_ML','/*\n\nchau\n\n*/',10,46)
  ], [comentario('/**/'), # Nota: los comentarios siguientes pasan a ser la clausura de los nodos anteriores
      identificador('a'),
      # comentario('// b '),
      # comentario('// // hola /* */'),
      identificador('c'),
      # comentario('/*\n\nhola\n\n*/'),
      identificador('d'),
      # comentario('/*\n\nchau\n\n*/')
  ]),
  Test("Invocación a una función",
    "a(5, chau(  ),  3)",[
    id('a',1,0),
    t('ABRE_PAREN','(',1,1),
    n('5',1,2),
    t('COMA',',',1,3),
    t('SKIP',' ',1,4),
    id('chau',1,5),
    t('ABRE_PAREN','(',1,9),
    t('SKIP','  ',1,10),
    t('CIERRA_PAREN',')',1,12),
    t('COMA',',',1,13),
    t('SKIP','  ',1,14),
    n('3',1,16),
    t('CIERRA_PAREN',')',1,17)
  ], [invocacion('a', [literal('5'),invocacion('chau'),literal('3')])
  ]),
  Test("Acceso a objetos",
    "a.b;a[1];b[a]",[
      id('a',1,0),
      t('PUNTO','.',1,1),
      id('b',1,2),
      t('PUNTO_Y_COMA',';',1,3),
      id('a',1,4),
      t('ABRE_CORCHETE','[',1,5),
      n('1',1,6),
      t('CIERRA_CORCHETE',']',1,7),
      t('PUNTO_Y_COMA',';',1,8),
      id('b',1,9),
      t('ABRE_CORCHETE','[',1,10),
      id('a',1,11),
      t('CIERRA_CORCHETE',']',1,12)
  ], [acceso('a','b'),
      index('a','1'),
      index('b','a')
  ]),
]

def evaluar(test):
  esperado = test.tokens
  obtenido = tokenizar(test.input)
  i = 0
  while i < len(obtenido) and i < len(esperado):
    if str(obtenido[i]) != str(esperado[i]):
      print("Error en test: "+test.desc)
      print("El token "+str(i)+" debería ser "+str(esperado[i])+" pero es "+str(obtenido[i]))
      return True
    i += 1
  if len(obtenido) > i:
    print("Error en test: "+test.desc)
    print("Se generaron " + str(len(obtenido)-i) + " tokens adicionales")
    return True
  if len(esperado) > i:
    print("Error en test: "+test.desc)
    print("Faltó generar " + str(len(esperado)-i) + " tokens")
    return True
  restore = "".join(list(map(lambda x : x.value, obtenido)))
  if restore != test.input:
    print("Error en test: "+test.desc)
    print("La entrada original era:")
    print(clean_str(test.input))
    print("Pero el resultado recuperado de los tokens es:")
    print(clean_str(restore))
    return True
  esperado = test.ast
  obtenido = parsear(test.input)
  i = 0
  while i < len(esperado) and i < len(obtenido):
    if str(obtenido[i]) != str(esperado[i]):
      print("Error en test: "+test.desc)
      print("Se esperaba "+clean_str(esperado[i])+" pero se obtuvo "+clean_str(obtenido[i]))
      return True
    i += 1
  if len(obtenido) > i:
    print("Error en test: "+test.desc)
    print("Se generaron " + str(len(obtenido)-i) + " términos adicionales")
    return True
  if len(esperado) > i:
    print("Error en test: "+test.desc)
    print("Faltó generar " + str(len(esperado)-i) + " términos")
    return True
  restore = "".join(list(map(lambda x : x.restore(), obtenido)))
  if restore != test.input:
    print("Error en test: "+test.desc)
    print("La entrada original era:")
    print(clean_str(test.input))
    print("Pero el resultado recuperado del ast es:")
    print(clean_str(restore))
    return True
  return False

def clean_str(s):
  return str(s).replace('\n','\\n').replace('\t','\\t')

if __name__ == '__main__':
  main()