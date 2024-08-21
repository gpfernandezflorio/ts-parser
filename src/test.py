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

def id(s,i,c,f):
  return t('IDENTIFICADOR',s,i,c,f)

def n(s,i,c,f):
  return t('NUMERO',s,i,c,f)

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
    id('hola',1,1,0),
    t('ABRE_PAREN','(',1,5,4),
    t('CIERRA_PAREN',')',1,6,5),
    t('PUNTO_Y_COMA',';',1,7,6)
  ], [invocacion('hola')
  ]),
  Test("Dos comandos",
    "hola();\nchau();",[
    id('hola',1,1,0),
    t('ABRE_PAREN','(',1,5,4),
    t('CIERRA_PAREN',')',1,6,5),
    t('PUNTO_Y_COMA',';',1,7,6),
    t('SKIP','\n',1,8,7),
    id('chau',2,1,8),
    t('ABRE_PAREN','(',2,5,12),
    t('CIERRA_PAREN',')',2,6,13),
    t('PUNTO_Y_COMA',';',2,7,14)
  ], [invocacion('hola'),
      invocacion('chau')
  ]),
  Test("Blancos",
    " \t\n",[
    t('SKIP',' \t\n',1,1,0)
  ], [espacios(' \t\n')
  ]),
  Test("Comandos con blancos",
    "\t \t hola();\t \n\t \tchau();  \n\n  ",[
    t('SKIP','\t \t ',1,1,0),
    id('hola',1,5,4),
    t('ABRE_PAREN','(',1,9,8),
    t('CIERRA_PAREN',')',1,10,9),
    t('PUNTO_Y_COMA',';',1,11,10),
    t('SKIP','\t \n\t \t',1,12,11),
    id('chau',2,4,17),
    t('ABRE_PAREN','(',2,8,21),
    t('CIERRA_PAREN',')',2,9,22),
    t('PUNTO_Y_COMA',';',2,10,23),
    t('SKIP','  \n\n  ',2,11,24)
  ], [espacios('\t \t '),
      invocacion('hola'),
      invocacion('chau'),
  ]),
  Test("Una variable",
    "\tlet x\t=  5",[
    t('SKIP','\t',1,1,0),
    t('DECL_VAR','let',1,2,1),
    t('SKIP',' ',1,5,4),
    id('x',1,6,5),
    t('SKIP','\t',1,7,6),
    t('ASIGNACION','=',1,8,7),
    t('SKIP','  ',1,9,8),
    n('5',1,11,10)
  ], [espacios('\t'),
      variable('x',literal('5'))
  ]),
  Test("Declaración y asignación de variable con strings",
    "const\tx;x =\n'2'x=\"true\"",[
    t('DECL_VAR','const',1,1,0),
    t('SKIP','\t',1,6,5),
    id('x',1,7,6),
    t('PUNTO_Y_COMA',';',1,8,7),
    id('x',1,9,8),
    t('SKIP',' ',1,10,9),
    t('ASIGNACION','=',1,11,10),
    t('SKIP','\n',1,12,11),
    t('STRING',"'2'",2,1,12),
    id('x',2,4,15),
    t('ASIGNACION','=',2,5,16),
    t('STRING','"true"',2,6,17)
  ], [variable('x'),
      asignacion('x',literal("'2'")),
      asignacion('x',literal('"true"'))
  ]),
  Test("Declaración de función",
    "function HOLA() {x=2.5;let y = .66\t;}",[
    t('DECL_FUNC','function',1,1,0),
    t('SKIP',' ',1,9,8),
    id('HOLA',1,10,9),
    t('ABRE_PAREN','(',1,14,13),
    t('CIERRA_PAREN',')',1,15,14),
    t('SKIP',' ',1,16,15),
    t('ABRE_LLAVE','{',1,17,16),
    id('x',1,18,17),
    t('ASIGNACION','=',1,19,18),
    n('2.5',1,20,19),
    t('PUNTO_Y_COMA',';',1,23,22),
    t('DECL_VAR','let',1,24,23),
    t('SKIP',' ',1,27,26),
    id('y',1,28,27),
    t('SKIP',' ',1,29,28),
    t('ASIGNACION','=',1,30,29),
    t('SKIP',' ',1,31,30),
    n('.66',1,32,31),
    t('SKIP','\t',1,35,34),
    t('PUNTO_Y_COMA',';',1,36,35),
    t('CIERRA_LLAVE','}',1,37,36)
  ], [funcion('HOLA',[],[
        asignacion('x',literal('2.5')),
        variable('y',literal('.66'))
    ])
  ]),
  Test("Comentarios",
    "/**/a // b \n// // hola /* */\nc\n/*\n\nhola\n\n*/\nd\n/*\n\nchau\n\n*/",[
    t('COMENTARIO_ML','/**/',1,1,0),
    id('a',1,5,4),
    t('SKIP',' ',1,6,5),
    t('COMENTARIO_UL','// b ',1,7,6),
    t('SKIP','\n',1,12,11),
    t('COMENTARIO_UL','// // hola /* */',2,1,12),
    t('SKIP','\n',2,17,28),
    id('c',3,1,29),
    t('SKIP','\n',3,2,30),
    t('COMENTARIO_ML','/*\n\nhola\n\n*/',4,1,31),
    t('SKIP','\n',8,3,43),
    id('d',9,1,44),
    t('SKIP','\n',9,2,45),
    t('COMENTARIO_ML','/*\n\nchau\n\n*/',10,1,46)
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
    id('a',1,1,0),
    t('ABRE_PAREN','(',1,2,1),
    n('5',1,3,2),
    t('COMA',',',1,4,3),
    t('SKIP',' ',1,5,4),
    id('chau',1,6,5),
    t('ABRE_PAREN','(',1,10,9),
    t('SKIP','  ',1,11,10),
    t('CIERRA_PAREN',')',1,13,12),
    t('COMA',',',1,14,13),
    t('SKIP','  ',1,15,14),
    n('3',1,17,16),
    t('CIERRA_PAREN',')',1,18,17)
  ], [invocacion('a', [literal('5'),invocacion('chau'),literal('3')])
  ]),
  Test("Acceso a objetos",
    "a.b;a[1];b[a]",[
      id('a',1,1,0),
      t('PUNTO','.',1,2,1),
      id('b',1,3,2),
      t('PUNTO_Y_COMA',';',1,4,3),
      id('a',1,5,4),
      t('ABRE_CORCHETE','[',1,6,5),
      n('1',1,7,6),
      t('CIERRA_CORCHETE',']',1,8,7),
      t('PUNTO_Y_COMA',';',1,9,8),
      id('b',1,10,9),
      t('ABRE_CORCHETE','[',1,11,10),
      id('a',1,12,11),
      t('CIERRA_CORCHETE',']',1,13,12)
  ], [acceso('a','b'),
      index('a','1'),
      index('b','a')
  ]),
  Test("Combinación objetos y funciones",
    "a.b.c()().c(c[3].b[a()[b]()][2])",[
    id('a',1,1,0),
    t('PUNTO','.',1,2,1),
    id('b',1,3,2),
    t('PUNTO','.',1,4,3),
    id('c',1,5,4),
    t('ABRE_PAREN','(',1,6,5),
    t('CIERRA_PAREN',')',1,7,6),
    t('ABRE_PAREN','(',1,8,7),
    t('CIERRA_PAREN',')',1,9,8),
    t('PUNTO','.',1,10,9),
    id('c',1,11,10),
    t('ABRE_PAREN','(',1,12,11),
    id('c',1,13,12),
    t('ABRE_CORCHETE','[',1,14,13),
    n('3',1,15,14),
    t('CIERRA_CORCHETE',']',1,16,15),
    t('PUNTO','.',1,17,16),
    id('b',1,18,17),
    t('ABRE_CORCHETE','[',1,19,18),
    id('a',1,20,19),
    t('ABRE_PAREN','(',1,21,20),
    t('CIERRA_PAREN',')',1,22,21),
    t('ABRE_CORCHETE','[',1,23,22),
    id('b',1,24,23),
    t('CIERRA_CORCHETE',']',1,25,24),
    t('ABRE_PAREN','(',1,26,25),
    t('CIERRA_PAREN',')',1,27,26),
    t('CIERRA_CORCHETE',']',1,28,27),
    t('ABRE_CORCHETE','[',1,29,28),
    n('2',1,30,29),
    t('CIERRA_CORCHETE',']',1,31,30),
    t('CIERRA_PAREN',')',1,32,31)
  ], [
    invocacion(
      acceso(
        invocacion(invocacion(
          acceso(acceso('a','b'),'c')
        )),
        'c'
      ),
      [
        index(index(
          acceso(index('c','3'),'b'),
          invocacion(index(invocacion('a'),'b'))
        ),'2')
      ]
    )
  ])
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