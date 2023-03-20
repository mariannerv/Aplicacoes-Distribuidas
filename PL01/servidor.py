import socket as s
import sys


HOST = str(sys.argv[1]) #pode ser vazio, localhost ou 127.0.0.1
PORT = int(sys.argv[2])
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
#sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)

while True:
    try:


        (conn_sock, (addr, port)) = sock.accept()
        print('ligado a %s no porto %s' % (addr,port))
        msg = conn_sock.recv(1024)
        print('recebi %s' % msg.decode())
        conn_sock.sendall(b'Aqui vai a resposta')
        conn_sock.close()

    except:
        print("Vou encerrar")
        break
