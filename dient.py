import json
import socket
import struct

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5211

CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = 40001


def receive_exact(connection, size):
    data = b""
    while len(data) < size:
        chunck = connection.recv(size - len(data))
        if not chunck:
            raise ConnectionError("Server disconnected early")
        data += chunck
    return data


def send_message(conection, message):
    payload = json.dumps(message).encode("utf-8")
    header = struct.pack("!I", len(payload))
    conection.sendall(header + payload)


def receive_message(connection):
    header = receive_exact(connection, 4)
    payload_size = struct.unpack("!I", header)[0]
    if payload_size > 1_000_000:
        raise ValueError("Message too large")
    payload = receive_exact(connection, payload_size)
    return json.loads(payload.decode("utf-8"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.bind((CLIENT_HOST, CLIENT_PORT))
    client.connect((SERVER_HOST, SERVER_PORT))
    request = {
        "protocol": "TLAB/1",
        "type": "message",
        "text": "Hello i wrote my own message  protocol",
    }
    send_message(client, request)
    response = receive_message(client)
    print("server response:", response)
