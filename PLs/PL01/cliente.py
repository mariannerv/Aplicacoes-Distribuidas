import socket as s
import sys


HOST = str(sys.argv[1]) #'127.0.0.1'
PORT = int(sys.argv[2])    #9999


while True:
    msg = input()

    if msg == "EXIT":
        break
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    sock.connect((HOST, PORT))

    sock.sendall(msg.encode())
    resposta = sock.recv(1024)
    print('Recebi %s' % resposta.decode())
    sock.close()





