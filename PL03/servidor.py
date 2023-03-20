import pickle
import struct
import sys, socket as s
from skeleton import ListSkeleton

# Para ficar no root da pasta, por causa do sock_utils
sys.path.insert(0, '..')
import sock_utils

HOST = ''

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 9999

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)

l = ListSkeleton()

while True:
    try:
        (conn_sock, addr) = sock.accept()

        res_size_bytes = sock_utils.receive_all(conn_sock, 4)
        size = struct.unpack('i', res_size_bytes)[0]

        res_bytes = sock_utils.receive_all(conn_sock, size)
        resp = l.processMessage(res_bytes)

        size_bytes = struct.pack('i', len(resp))
        conn_sock.sendall(size_bytes)
        conn_sock.sendall(resp)

        conn_sock.close()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print ('socket fechado!')
        conn_sock.close()

sock.close()