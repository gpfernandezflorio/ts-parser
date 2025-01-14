import sys
from bibpy.base import Boom
from bibpy.archivos import *
from bibpy.listas import elementosDesde_
from parser import tokenizar, parsear, mostrarAST, mostrarTokens, mostrarDiff, eq_string

testDesde = ''

def main():
  if len(sys.argv) == 1:
    Boom("No me pasaste ninguna ruta a un archivo o carpeta")
  nombreArchivo = sys.argv[1]
  verb = True
  archivos = [nombreArchivo]
  if existeCarpeta_Acá(nombreArchivo):
    verb = False
    archivos = todosLosArchivosEn_(nombreArchivo)
    if len(testDesde) > 0:
      archivos = elementosDesde_(archivos, testDesde)
  for nombreArchivo in archivos:
    if not existeArchivo_Acá(nombreArchivo):
      Boom("No existe el archivo " + nombreArchivo)
    parsearArchivo(nombreArchivo, verb)

def parsearArchivo(nombreArchivo, verb=True):
  if verb:
    print(nombreArchivo)
  contenido = contenidoDe_(nombreArchivo)
  tokens = tokenizar(contenido)
  # mostrarTokens(tokens)
  ast = parsear(contenido)
  # mostrarAST(ast)
  z = ast.restore()
  if eq_string(contenido, z):
    if verb:
      print("Restauración exitosa")
  else:
    if not verb:
      print(nombreArchivo)
    print("Falló la restauración")
    mostrarDiff(contenido, z)
  return ast

if __name__ == '__main__':
  main()