from parser import tokenizar, parsear
from parser import token as t
from parser import AST_espacios as espacios
from parser import AST_invocacion as invocacion
from parser import AST_decl_variable as variable
from parser import AST_asignacion as asignacion
from parser import AST_expresion as expresion
from parser import AST_decl_funcion as funcion

def id(s,i,f):
  return t('IDENTIFICADOR',s,i,f)

def n(s,i,f):
  return t('NUMERO',s,i,f)

def main():
  for test in casos_de_test:
    if evaluar(test):
      exit(1)
    print(test.desc + " OK")
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
    t('SKIP','  \n\n  ',2,24),
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
      variable('x',expresion('5'))
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
      asignacion('x',expresion("'2'")),
      asignacion('x',expresion('"true"'))
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
    t('CIERRA_LLAVE','}',1,36),
  ], [funcion('HOLA',[
        asignacion('x',expresion('2.5')),
        variable('y',expresion('.66'))
    ])
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