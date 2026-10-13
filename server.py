import socket

HOST = "127.0.0.1"
PORT = 5211
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Server listening on {HOST}:{PORT}")
connection, client_address = server.accept()
print(f"CLient connnected to {client_address}")
message = connection.recv(1024)
print(f"client says: {message.decode()}")
connection.sendall(b"Hello from server")
connection.close()
server.close()