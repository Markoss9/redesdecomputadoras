import socket
import threading

clientes = []
lock = threading.Lock()
servidor_activo = True

def manejar_cliente(conn, addr):
    global clientes
    print(f"Cliente conectado desde {addr}")

    while True:
        try:
            datos = conn.recv(1024)
            if not datos:
                break
            mensaje = datos.decode()
            print(f"Cliente ({addr}) dice: {mensaje}")

            if mensaje.lower() == "exit":
                print(f"Cliente ({addr}) se desconectó")
                break
        except:
            break

    with lock:
        clientes.remove(conn)
    conn.close()


def recibir_conexiones(server_socket):
    global servidor_activo
    while servidor_activo:
        try:
            conn, addr = server_socket.accept()
            with lock:
                clientes.append(conn)
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo.start()
        except:
            break


def enviar_mensajes(server_socket):
    global servidor_activo
    while servidor_activo:
        texto = input("MANDAR MENSAJE DESDE EL SERVIDOR: ")
        if texto.lower() == "exit":
            with lock:
                if len(clientes) > 0:
                    print("No es posible cerrar el proceso servidor si hay un cliente conectado")
                else:
                    print("Servidor cerrado.")
                    servidor_activo = False
                    server_socket.close()
                    break
        else:
            with lock:
                for c in clientes:
                    try:
                        c.send(texto.encode())
                    except:
                        pass


# -------------------------
# Main del servidor
# -------------------------
HOST = "0.0.0.0"
PORT = 60000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Servidor escuchando en {HOST}:{PORT}")

# Hilo para aceptar conexiones
hilo_conexiones = threading.Thread(target=recibir_conexiones, args=(server_socket,))
hilo_conexiones.start()

# Hilo para enviar mensajes desde el servidor
enviar_mensajes(server_socket)
