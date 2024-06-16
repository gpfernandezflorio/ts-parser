import sys
from utils import boom, leerArchivo_, existeArchivo_
from parser import tokenizar, parsear

def main():
  if len(sys.argv) == 1:
    boom("No me pasaste ningún archivo")
  nombreArchivo = sys.argv[1]
  if not existeArchivo_(nombreArchivo):
    boom("No existe el archivo " + nombreArchivo)
  contenido = leerArchivo_(nombreArchivo)

  tokens = tokenizar(contenido)
  # mostrarTokens(tokens)
  ast = parsear(contenido)
  mostrarAST(ast)
  z = ""
  for a in ast:
    z += a.restore()
  if contenido == z:
    print("Restauración exitosa")
  else:
    print("Falló la restauración")
    print(z)

def mostrarTokens(tokens):
  for t in tokens:
    print(fill(t.type) + clean(t.value))

def mostrarAST(ast):
  for n in ast:
    print(n)

def fill(s):
  resultado = s
  while len(resultado) < 15:
    resultado += ' '
  return resultado

def clean(s):
  return s.replace('\n','\\n')

if __name__ == '__main__':
  main()