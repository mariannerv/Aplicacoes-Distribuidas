import pickle


class ListSkeleton:
    def __init__(self):
        self.servicoLista = []

    def processMessage(self, msg_bytes):
        pedido = self.bytesToList(msg_bytes)
        resposta = []

        if pedido is None or len(pedido) == 0:
            resposta.append('INVALID MESSAGE')
        else:
            cmd, *args = pedido
            if cmd == 'APPEND' and len(pedido) > 1:
                self.servicoLista.append(args[0])
                resposta.append('OK')
            elif cmd == 'LIST':
                resposta = self.servicoLista
            elif cmd == 'CLEAR':
                self.servicoLista.clear()
                resposta.append('OK')
            elif cmd == 'REMOVE':
                try:
                    self.servicoLista.remove(args[0])
                    resposta.append('OK')
                except ValueError:
                    resposta.append('VALUE NOT IN LIST')
            elif cmd == 'REMOVE-ALL':
                pre_len = len(self.servicoLista)
                while True:
                    try:
                        self.servicoLista.remove(args[0])
                    except ValueError:
                        break

                if pre_len != len(self.servicoLista):
                    resposta.append('VALUE NOT IN LIST')
                else:
                    resposta.append('OK')

            elif cmd == 'POP':
                if len(self.servicoLista) == 0:
                    resposta.append('LIST IS EMPTY')
                else:
                    resposta.append(self.servicoLista.pop())
            else:
                resposta.append('INVALID MESSAGE')

        return self.listToBytes(resposta)

    # fim do metodo processMessage

    def bytesToList(self, msg_bytes):
        return pickle.loads(msg_bytes)

    def listToBytes(self, msg):
        return pickle.dumps(msg)