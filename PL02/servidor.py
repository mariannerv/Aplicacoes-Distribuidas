import sys, socket as s
import pickle, struct
#import sock_utils



resp = ['ack']
def receive_all(socket, length):
    msg = b''
    qty = 0
    while qty < length:
        ms = socket.recv(length - qty)
        qty += len(ms)
        msg+=ms
    return msg


HOST = ''

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 9999

#sock = sock_utils.create_tcp_server_socket(HOST, PORT, 1):
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)

lista = []
while True:
    try:
        (conn_sock, addr) = sock.accept()

        #obter mensagem
        size_bytes = receive_all(conn_sock,4)
        size = struct.unpack('i',size_bytes)[0]


        #desserializar a mensagem
        msg_bytes = receive_all(conn_sock,size)
        msg = pickle.loads(msg_bytes)
        
        if msg[0] == 'LIST':
            resp = lista
            msg_bytes = pickle.dumps(resp, -1)
        elif msg[0] == 'CLEAR':
            lista = []
            resp = 'Lista apagada'
        elif 'REMOVE' == msg[0]:
            try:
                pos = msg[1]
                lista.pop(pos)
            except Exception as e:
                lista.append(e)
        else:
            print(msg)
            lista.append(' '.join(msg))



        #serializar a resposta

        resp_bytes = pickle.dumps(resp,-1)
        size_bytes = struct.pack('i',len(resp_bytes))

        #enviar resposta

        conn_sock.sendall(size_bytes)
        conn_sock.sendall(resp_bytes)

        print('list= %s' % lista)
        conn_sock.close()

    except Exception as e:
        print('Vou encerrar!', e)
        break
