import sys
from stub import ListStub

if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = '127.0.0.1'
    PORT = 9999

stub = ListStub(HOST, PORT)
while True:
    msg = input('Mensagem: ');
    if msg == 'EXIT':
        exit()

    cmd, *args = msg.split()

    res = []
    if cmd == 'LIST':
        cmd = stub.list()
    elif msg == 'CLEAR':
        res = stub.clear()
    elif cmd == 'REMOVE':
        res = stub.remove(*args)
    elif cmd == 'REMOVE-ALL':
        res = stub.remove_all(*args)
    elif cmd == 'POP':
        res = stub.pop()
        pass
    else:
        res = stub.append(msg)

    print(f'Recebi: {", ".join(res)}')