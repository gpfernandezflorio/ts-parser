import os, io, shutil

def Boom(msg):
  ''' Fallar con un mensaje personalizado.
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

def existeCarpeta_(ruta):
  ''' Indicar si existe la carpeta con la ruta dada.
    @param ruta : string
    @tipo bool
  '''
  return os.path.isdir(ruta)

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

def IrA_(ruta):
  ''' Ubicarse en la ruta dada.
    @pre existe una carpeta con la ruta dada.
    @param ruta : string
  '''
  os.chdir(ruta)

def nombreDe_(ruta):
  ''' Obtener el nombre de un archivo o una carpeta.
    @param ruta : string
    @tipo string
  '''
  nombre = os.path.basename(ruta)
  if len(nombre) == 0:
    nombre = os.path.basename(os.path.dirname(ruta))
  return nombre

def rutaRaizDe_(ruta):
  ''' Obtener la ruta a la carpeta que contiene al archivo o carpeta dada.
    @param ruta : string
    @tipo string
  '''
  nombre = os.path.basename(ruta)
  if len(nombre) == 0:
    return os.path.dirname(os.path.dirname(ruta))
  return os.path.dirname(ruta)

def CrearCarpeta_(nombre):
  ''' Crear una carpeta con el nombre dado en la carpeta actual.
    @pre no existe una carpeta con el nombre dado en la carpeta actual.
    @param nombre : string
  '''
  CrearCarpeta_En_(nombre, '.')

def CrearCarpeta_En_(nombre, ruta):
  ''' Crear una carpeta con el nombre dado en la carpeta dada.
    @pre no existe una carpeta con el nombre dado en la carpeta dada.
    @param nombre : string
    @param ruta : string
  '''
  os.mkdir(os.path.join(ruta, nombre))

def BorrarCarpeta_(ruta):
  ''' Borrar la carpeta en la ruta dada.
    @pre existe una carpeta en la ruta dada.
    @param ruta : string
  '''
  shutil.rmtree(ruta)

def listaDeArchivosEn_(ruta):
  ''' Obtener la lista de nombres de archivos en la ruta dada.
    @pre existe una carpeta en la ruta dada.
    @param ruta : string
    @tipo [string]
  '''
  return list(filter(lambda x : existeArchivo_(nuevaRuta_(ruta, x)), os.listdir(ruta)))

def listaDeCarpetasEn_(ruta):
  ''' Obtener la lista de nombres de carpetas en la ruta dada.
    @pre existe una carpeta en la ruta dada.
    @param ruta : string
    @tipo [string]
  '''
  return list(filter(lambda x : existeCarpeta_(nuevaRuta_(ruta, x)), os.listdir(ruta)))

def nuevaRuta_(ruta1, ruta2):
  ''' Obtener una ruta compuesta de las 2 rutas dadas.
    @pre existe una carpeta con ruta 'ruta2 en la ruta 'ruta1'.
    @param ruta1 : string
    @param ruta2 : string
    @tipo string
  '''
  return os.path.join(ruta1, ruta2)