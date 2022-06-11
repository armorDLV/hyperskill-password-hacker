import argparse
import socket

parser = argparse.ArgumentParser(description='Stage 1/5: Establishing a connection')
parser.add_argument('ip', help="IP address")
parser.add_argument('port', type=int, help="Port number")
parser.add_argument('message', help="Message to send")
args = parser.parse_args()

with socket.socket() as client_socket:
    hostname = args.ip
    port = args.port
    address = (hostname, port)

    client_socket.connect(address)

    data = args.message
    data = data.encode()

    client_socket.send(data)

    response = client_socket.recv(1024)

    response = response.decode()
    print(response)
