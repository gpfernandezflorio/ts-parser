import sys
import functools
from bibpy.base import Boom
from bibpy.archivos import contenidoDe_, existeArchivo_Acá
from parser import tokenizar, parsear

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