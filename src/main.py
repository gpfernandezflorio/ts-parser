import sys
import functools
from bibpy.base import Boom
from bibpy.archivos import contenidoDe_, existeArchivo_Acá
from parser import tokenizar, parsear, mostrarAST, mostrarTokens, mostrarDiff

def main():
  if len(sys.argv) == 1:
    Boom("No me pasaste ningún archivo")
  nombreArchivo = sys.argv[1]
  if not existeArchivo_Acá(nombreArchivo):
    Boom("No existe el archivo " + nombreArchivo)
  parsearArchivo(nombreArchivo)

def parsearArchivo(nombreArchivo):
  print(nombreArchivo)
  contenido = contenidoDe_(nombreArchivo)
  tokens = tokenizar(contenido)
  # mostrarTokens(tokens)
  ast = parsear(contenido)
  # mostrarAST(ast)
  z = ""
  for a in ast:
    z += a.restore()
  if eq_string(contenido, z):
    print("Restauración exitosa")
  else:
    print("Falló la restauración")
    mostrarDiff(contenido, z)

def eq_string(a, b):
  return len(a) == len(b) and functools.reduce(lambda x, rec: a[x]==b[x] and rec, range(len(a)), True)

def fill(s,k):
  resultado = s
  while len(resultado) < k:
    resultado += ' '
  return resultado

def clean(s):
  return s.replace('\n','\\n')

if __name__ == '__main__':
  main()