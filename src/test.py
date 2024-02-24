import os
from utils import leerArchivo_
from parser import tokenizar, parsear
from parser import token as t
from parser import AST_comando as comando
from parser import AST_espacios as espacios
from parser import AST_invocacion as invocacion

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
    t('IDENTIFICADOR','hola',1,0),
    t('ABRE_PAREN','(',1,4),
    t('CIERRA_PAREN',')',1,5),
    t('PUNTO_Y_COMA',';',1,6)
  ], [comando(invocacion('hola'), ';')
  ]),
  Test("Dos comandos",
    "hola();\nchau();",[
    t('IDENTIFICADOR','hola',1,0),
    t('ABRE_PAREN','(',1,4),
    t('CIERRA_PAREN',')',1,5),
    t('PUNTO_Y_COMA',';',1,6),
    t('SALTO_DE_LINEA','\n',1,7),
    t('IDENTIFICADOR','chau',2,8),
    t('ABRE_PAREN','(',2,12),
    t('CIERRA_PAREN',')',2,13),
    t('PUNTO_Y_COMA',';',2,14)
  ], [comando(invocacion('hola'), ';'),
      espacios('\n'),
      comando(invocacion('chau'), ';')
  ]),
  Test("Blancos",
    " \t\n",[
    t('ESPACIO',' ',1,0),
    t('TAB','\t',1,1),
    t('SALTO_DE_LINEA','\n',1,2)
  ], [espacios(' \t\n')
  ]),
  Test("Comandos con blancos",
    "\t \t hola();\t \n\t \tchau();  \n\n  ",[
    t('TAB','\t',1,0),
    t('ESPACIO',' ',1,1),
    t('TAB','\t',1,2),
    t('ESPACIO',' ',1,3),
    t('IDENTIFICADOR','hola',1,4),
    t('ABRE_PAREN','(',1,8),
    t('CIERRA_PAREN',')',1,9),
    t('PUNTO_Y_COMA',';',1,10),
    t('TAB','\t',1,11),
    t('ESPACIO',' ',1,12),
    t('SALTO_DE_LINEA','\n',1,13),
    t('TAB','\t',2,14),
    t('ESPACIO',' ',2,15),
    t('TAB','\t',2,16),
    t('IDENTIFICADOR','chau',2,17),
    t('ABRE_PAREN','(',2,21),
    t('CIERRA_PAREN',')',2,22),
    t('PUNTO_Y_COMA',';',2,23),
    t('ESPACIO',' ',2,24),
    t('ESPACIO',' ',2,25),
    t('SALTO_DE_LINEA','\n',2,26),
    t('SALTO_DE_LINEA','\n',3,27),
    t('ESPACIO',' ',4,28),
    t('ESPACIO',' ',4,29)
  ], [espacios('\t \t '),
      comando(invocacion('hola'), ';'),
      espacios('\t \n\t \t'),
      comando(invocacion('chau'), ';'),
      espacios('  \n\n  ')
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
  esperado = test.ast
  obtenido = parsear(test.input)
  i = 0
  while i < len(esperado) and i < len(obtenido):
    if str(obtenido[i]) != str(esperado[i]):
      print("Error en test: "+test.desc)
      print("Se esperaba "+str(esperado[i])+" pero se obtuvo "+str(obtenido[i]))
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

if __name__ == '__main__':
  main()