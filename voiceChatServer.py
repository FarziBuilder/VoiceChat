import socket
import threading

port = 5000
host = "0.0.0.0"

server = socket.socket()
server.bind((host, port))
server.listen(5)

clients = []

def start():
    print("Server started, waiting for connections...")
    while True:
        conn, addr = server.accept()
        print(f"Client connected from {addr}")
        clients.append(conn)
        t = threading.Thread(target=handle_client, args=(conn,))
        t.start()

def handle_client(conn):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            print(f"Received data from {conn.getpeername()}")
            broadcast(data, conn)
    except Exception as e:
        print(f"Client handling error: {e}")
    finally:
        print(f"Client {conn.getpeername()} disconnected")
        clients.remove(conn)
        conn.close()

def broadcast(data, from_conn):
    for cl in clients:
        if cl != from_conn:
            try:
                cl.send(data)
                print("Broadcasted data")
            except Exception as e:
                print(f"Broadcast error: {e}")

start()
