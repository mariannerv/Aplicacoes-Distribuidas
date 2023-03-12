import sys, socket as s
import pickle,struct


def receive_all(socket, length):
    msg = b''
    qty = 0
    while qty < length:
        ms = socket.recv(length - qty)
        qty += len(ms)
        msg+=ms
    return msg
        

if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = '127.0.0.1'
    PORT = 9999

while True:
    msg = str(input('Mensagem: '));
    if msg == 'EXIT':
        break

    #conn_sock = sock_utils.create_tcp_client_socket(HOST, PORT)
    conn_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    conn_sock.connect((HOST, PORT))


    msg_lista = msg.split()


    #serializar a mensagem

    msg_bytes = pickle.dumps(msg_lista, -1) #usamos o -1 para especificar o nivel de protocolo mais alto
    size_bytes = struct.pack('i', len(msg_bytes))


    #Enviar a mensagem

    conn_sock.sendall(size_bytes)
    conn_sock.sendall(msg_bytes)


    #Receber a resposta

    size_bytes = receive_all(conn_sock, 4)
    size = struct.unpack('i', size_bytes)[0]


    # Desserializar a resposta
    msg_bytes = receive_all(conn_sock, size)
    msg = pickle.loads(msg_bytes)

    print('Recebi: %s' % msg)
    conn_sock.close()
