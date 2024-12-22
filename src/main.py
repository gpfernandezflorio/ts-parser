import sys
from bibpy.base import Boom
from bibpy.archivos import contenidoDe_, existeArchivo_Acá
from parser import tokenizar, parsear, mostrarAST, mostrarTokens, mostrarDiff, eq_string

archivosTest = [
  "../../blockly/core/bubbles/bubble.ts",
  "../../blockly/core/bubbles/mini_workspace_bubble.ts",
  "../../blockly/core/bubbles/text_bubble.ts",
  "../../blockly/core/bubbles/textinput_bubble.ts"
]

def main():
  if len(sys.argv) == 1:
    Boom("No me pasaste ningún archivo")
  nombreArchivo = sys.argv[1]
  archivos = [nombreArchivo]
  if nombreArchivo == "TEST":
    archivos = archivosTest
  for nombreArchivo in archivos:
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

if __name__ == '__main__':
  main()