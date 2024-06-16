import os, io

def boom(msg):
  ''' Falla con un mensaje personalizado.
    @param msg : string
  '''
  print(msg)
  exit(0)

def existeArchivo_(ruta):
  ''' Indicar si existe el archivo con la ruta dada.
    @param ruta : string
    @tipo bool
  '''
  return os.path.isfile(ruta)

def leerArchivo_(ruta):
  ''' Obtener el contenido de un archivo como texto plano.
    @pre existe el archivo solicitado.
    @param ruta : string
    @tipo string
  '''
  f = io.open(ruta, mode='r', encoding='utf-8')
  contenido = f.read()
  f.close()
  return contenido