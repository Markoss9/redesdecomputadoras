
# -----------------------------------------
# Función para obtener la lista de tramas
# -----------------------------------------
def getListTramas(archivo):
    contenido = archivo.read()
    # Evitar confundir secuencias escapadas con banderas
    contenidoModificado = contenido.replace("7D7E", "ESCAPE")
    # Separar por banderas 7E
    tramas = contenidoModificado.split("7E")
    if tramas[0] == "":
        tramas.pop(0)  # eliminar primer elemento vacío
    # Restaurar las secuencias escapadas
    tramas = [t.replace("ESCAPE", "7D7E") for t in tramas]
    return tramas


# -----------------------------------------
# Función para verificar longitud de la trama
# -----------------------------------------
def getLongitudCorrecta(trama):
    try:
        longitud = int(trama[:4], 16) * 2   # longitud en caracteres hex
        longitud_real = len(trama) - 6      # sin contar longitud ni checksum
        return longitud == longitud_real
    except:
        return False

# -----------------------------------------
# Función para verificar checksum
# -----------------------------------------
def checksum(trama):
    try:
        byteCheckSum = int(trama[-2:], 16)
        cargaUtil = trama[4:-2]  # desde tipo trama hasta carga útil
        suma = 0
        for i in range(0, len(cargaUtil), 2):
            suma += int(cargaUtil[i:i+2], 16)
        sumaVerificacion = 255 - (suma & 255)
        return sumaVerificacion == byteCheckSum
    except:
        return False


# -----------------------------------------
# Variables de conteo y listas auxiliares
# -----------------------------------------
total_tramas = 0
longitud_correcta = 0
longitud_incorrecta = 0
checksum_correcto = 0
checksum_incorrecto = 0
tramas_escape = 0

lineas_con_escape = []  # Para inciso 5
lineas_incorrectas = [] # Para inciso 6

# -----------------------------------------
# Abrir y procesar archivo
# -----------------------------------------
with open("Tramas_802-15-4.log", "r") as archivo:
    tramas = getListTramas(archivo)

# Si queremos leer cualquier archivo, descomentar las líneas siguiente y comentar las dos anteriores
# ---------------------------------------------------------
# import sys
# if len(sys.argv) < 2:
    # print("Uso: python REDES-TP1.py <archivo.log>")
    # sys.exit(1)
# nombre_archivo = sys.argv[1]
# with open(nombre_archivo, "r") as archivo:
    # tramas = getListTramas(archivo)
# ---------------------------------------------------------

for idx, trama in enumerate(tramas):
    total_tramas += 1

    # Verificar secuencia de escape
    if "7D7E" in trama:
        tramas_escape += 1
        trama_limpia = trama.replace("7D7E", "7E")
        lineas_con_escape.append((idx, trama_limpia))

    # Verificar longitud
    if getLongitudCorrecta(trama):
        longitud_correcta += 1
        # Verificar checksum solo si longitud correcta
        if checksum(trama):
            checksum_correcto += 1
        else:
            checksum_incorrecto += 1
            lineas_incorrectas.append((idx, trama))
    else:
        longitud_incorrecta += 1
        lineas_incorrectas.append((idx, trama))

# -----------------------------------------
# Imprimir resultados finales
# -----------------------------------------
print(f"Tramas totales: {total_tramas}")
print(f"Tramas con longitud correcta = {longitud_correcta}")
print(f"Tramas con longitud incorrecta = {longitud_incorrecta}")
print(f"Tramas con longitud correcta y checksum correcto = {checksum_correcto}")
print(f"Tramas con longitud correcta y checksum incorrecto = {checksum_incorrecto}")
print(f"Tramas con secuencia de escape = {tramas_escape}\n")

# -----------------------------------------
# Imprimir tramas con secuencia de escape
# -----------------------------------------
print("Líneas con secuencia de escape (limpiadas):")
for idx, trama_limpia in lineas_con_escape:
    print(f"Línea {idx}: {trama_limpia}")

# -----------------------------------------
# Imprimir tramas incorrectas (longitud o checksum)
# -----------------------------------------
print("\nLíneas con longitud o checksum incorrecto:")
for idx, trama_erronea in lineas_incorrectas:
    print(f"Línea {idx}: {trama_erronea}")

