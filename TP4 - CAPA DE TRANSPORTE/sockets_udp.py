import socket
import threading

# -------------------------
# Pedir nombre de usuario
# -------------------------
username = input("Ingrese el nombre de usuario: ")

# -------------------------
# Crear socket UDP con broadcast
# -------------------------
mi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
mi_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # habilitar broadcast
mi_socket.bind(("0.0.0.0", 60000))  # escuchar en todas las interfaces


# -------------------------
# Función para obtener IP local
# -------------------------
def obtener_mi_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # conecta a cualquier IP
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


mi_ip = obtener_mi_ip()


# -------------------------
# Función para recibir mensajes
# -------------------------
def recibir_mensajes():
    while True:
        try:
            datos, direccion = mi_socket.recvfrom(1024)
            mensaje = datos.decode()
            ip_origen = direccion[0]

            # Ignorar mensajes propios
            # if ip_origen == mi_ip:
                # continue

            # Separar nombre de usuario y contenido
            if ':' in mensaje:
                nombre, contenido = mensaje.split(":", 1)
            else:
                nombre, contenido = "Desconocido", mensaje

            # Revisar tipo de mensaje
            if contenido == "nuevo":
                print(f"El usuario {nombre} ({ip_origen}) se ha unido a la conversación")
            elif contenido == "exit":
                print(f"El usuario {nombre} ({ip_origen}) ha abandonado la conversación")
            else:
                print(f"{nombre} ({ip_origen}) dice: {contenido}")
        except:
            continue


# -------------------------
# Función para enviar mensajes
# -------------------------
def enviar_mensajes():
    while True:
        texto = input()  # Leer mensaje del usuario

        if texto.lower() == "exit":
            mensaje = f"{username}:exit"
            mi_socket.sendto(mensaje.encode(), ("255.255.255.255", 60000))
            print("Has salido del chat.")
            mi_socket.close()   # Cerrar socket al salir
            break
        else:
            mensaje = f"{username}:{texto}"
            mi_socket.sendto(mensaje.encode(), ("255.255.255.255", 60000))
    

# -------------------------
# Enviar mensaje "nuevo" al iniciar
# -------------------------
mensaje_nuevo = f"{username}:nuevo"
mi_socket.sendto(mensaje_nuevo.encode(), ("255.255.255.255", 60000))


# -------------------------
# Crear e iniciar hilos
# -------------------------
hilo_recibir = threading.Thread(target=recibir_mensajes, daemon=True)
hilo_enviar = threading.Thread(target=enviar_mensajes)

hilo_recibir.start()
hilo_enviar.start()

# Esperar a que termine el hilo de envío antes de cerrar
hilo_enviar.join()

