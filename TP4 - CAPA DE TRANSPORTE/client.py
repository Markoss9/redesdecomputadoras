import socket
import threading

def recibir_mensajes(sock):
    while True:
        try:
            datos = sock.recv(1024)
            if not datos:
                break
            print(f"Servidor dice: {datos.decode()}")
        except:
            break

# -------------------------
# Main del cliente
# -------------------------
SERVER_IP = input("Ingrese la IP del servidor: ")
PORT = 60000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, PORT))

print("Conectado al servidor.")

# Hilo para recibir mensajes
hilo_recibir = threading.Thread(target=recibir_mensajes, args=(sock,))
hilo_recibir.start()

while True:
    texto = input("MANDAR MENSAJE DESDE EL CLIENTE: ")
    sock.send(texto.encode())

    if texto.lower() == "exit":
        print("Desconectado del servidor.")
        sock.close()
        break
