import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5211
CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = 5000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind((CLIENT_HOST, CLIENT_PORT))
client.connect((SERVER_HOST, SERVER_PORT))
print("Connected to server successfully")
client.sendall(b"Hello from cient")
reply = client.recv(1024)
print(f"Server replied with {reply.decode()}")
client.close()