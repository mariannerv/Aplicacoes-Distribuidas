import sys, socket as s
import socketserver

HOST = 'localhost'
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 9999

lista = []


class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global lista
        # self.request é a socket ligada ao cliente
        data = self.request.recv(1024)
        print('ligado a ', self.client_address)

        decoded = data.decode()
        resp = 'Ack'
        if decoded == 'LIST':
            resp = str(lista)
        elif decoded == 'CLEAR':
            lista.clear()
            resp = "Lista apagada"
        else:
            lista.append(decoded)

        # Respondemos com a string invertida
        self.request.sendall(resp.encode())


server = socketserver.ThreadingTCPServer((HOST, PORT), MyHandler)
server.serve_forever(2.0)