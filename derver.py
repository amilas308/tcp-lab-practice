import json
import socket
import struct

HOST = "127.0.0.1"
PORT = 5211


def receive_exact(connection, size):
    data = b""
    while len(data) < size:
        chunck = connection.recv(size - len(data))
        if not chunck:
            raise ConnectionError("Client disconnected early")
        data += chunck
    return data


def send_message(connection, message):
    payload = json.dumps(message).encode("utf-8")
    header = struct.pack("!I", len(payload))
    connection.sendall(header + payload)


def receive_message(connection):
    header = receive_exact(connection, 4)
    payload_size = struct.unpack("!I", header)[0]
    if payload_size > 1_000_000:
        raise ValueError("Messsage too large")
    payload = receive_exact(connection, payload_size)
    return json.loads(payload.decode("utf-8"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"T/Lab1 server listening on {HOST}:{PORT}")
    connection, client_address = server.accept()
with connection:
    print(f"Client connected: {HOST}")
    request = receive_message(connection)
    print("Received:", request)

    response = {
        "protocol": "TLab/1",
        "type": "reply",
        "text": f"Message received{request['text']}",
    }
    send_message(connection, response)
