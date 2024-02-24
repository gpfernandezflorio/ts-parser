import io

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