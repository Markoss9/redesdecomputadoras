
def getListTramas(archivo):
    archivo=archivo.read()
    archivoModificado = archivo.replace("7D7E", "LAURE")
    tramas = archivoModificado.split("7E")
    tramas.pop(0)
    tramasTotales=len(tramas)
    for i in range(tramasTotales):
        tramas[i] = tramas[i].replace("LAURE", "reemplazo")
    return tramas

def getLongitudCorrecta(trama):
    longitud = (int(trama[:4], 16))*2
    longTrama = len(trama)-6
    if longitud==longTrama:
        return True
    else:
        return False

def checksum(trama):
    posInicialCheckSum = len( trama ) - 2
    byteCheckSum = int( trama[ posInicialCheckSum : len(trama) ] , 16 )

    cargaUtil = trama[4 :len(trama)-2]
    sumaChecksum = 0
    for i in range(0, len(cargaUtil), 2):
        sumaChecksum += int( cargaUtil[i:i+2] , 16 )
    sumaVerificacion = 255-(sumaChecksum & 255)
    return sumaVerificacion == byteCheckSum



tramasConLongitudCorrecta=0
tramasConLogitudIncorrecta=0
tramasConLongitudYchecksum=0
tramasConLongitudYchecksumIncorrecto=0
tramasConSecuenciaDeEscape=0

archivo = open('Tramas_802-15-4.log', "r")
tramas = getListTramas(archivo)
for trama in tramas:
    if getLongitudCorrecta(trama):
        tramasConLongitudCorrecta+=1
        if checksum(trama):
            tramasConLongitudYchecksum+=1
        else:
            tramasConLongitudYchecksumIncorrecto+=1
    else:
        tramasConLogitudIncorrecta+=1
    if "7D7E" in trama:
        tramasConSecuenciaDeEscape+=1

print("Tramas totales: ", len(tramas))
print("Tramas con longitud correcta = ", tramasConLongitudCorrecta)
print("Tramas con longitud incorrecta = ", tramasConLogitudIncorrecta)
print("Tramas con longitud correcta y checksum correcto = ", tramasConLongitudYchecksum)
print("Tramas con longitud correcta y checksum incorrecto = ", tramasConLongitudYchecksumIncorrecto)
print("Tramas con secuencia de escape = ", tramasConSecuenciaDeEscape)


