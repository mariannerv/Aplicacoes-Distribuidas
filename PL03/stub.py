import pickle
import socket as s
import struct
import sys
from typing import List, Union

# Para ficar no root da pasta, por causa do sock_utils
sys.path.insert(0, '..')
import sock_utils


class ListStub:
    def __init__(self, host, port):
        self.conn_sock: s.socket = None
        self.host = host
        self.port = port

    def connect(self):
        self.conn_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.conn_sock.connect((self.host, self.port))

    def disconnect(self):
        self.conn_sock.close()

    def send(self, cmd: str, data=None):
        parsed = [cmd]
        if data:
            if isinstance(data, List):
                parsed.append(*data)
            else:
                parsed.append(data)

        self.connect()

        msg_bytes = pickle.dumps(parsed, -1)
        size_bytes = struct.pack('i', len(msg_bytes))

        self.conn_sock.sendall(size_bytes)
        self.conn_sock.sendall(msg_bytes)

        res_size_bytes = sock_utils.receive_all(self.conn_sock, 4)
        size = struct.unpack('i', res_size_bytes)[0]

        res_bytes = sock_utils.receive_all(self.conn_sock, size)
        res = pickle.loads(res_bytes)

        self.disconnect()
        return res

    def append(self, element: str):
        return self.send('APPEND', element)

    def list(self):
        return self.send('LIST')

    def clear(self):
        return self.send('CLEAR')

    # Outros métodos possíveis
    def remove(self, element: str):
        return self.send('REMOVE', element)

    def remove_all(self, element: str):
        return self.send('REMOVE-ALL', element)

    def pop(self):
        return self.send('POP')
