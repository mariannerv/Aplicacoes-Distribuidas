import sys, socket as s

if len(sys.argv) > 1:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
else:
	HOST = '127.0.0.1'
	PORT = 9999


sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
	msg = input('Mensagem: ')
	if msg == 'EXIT':
		break

	sock.sendall(msg.encode())
	resposta = sock.recv(1024)

	print('Recebi: %s' % resposta.decode())

sock.close()