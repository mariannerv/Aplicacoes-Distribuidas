import sys, socket as s
import select as sel

HOST = 'localhost'
if len(sys.argv) > 1:
	PORT = int(sys.argv[1])
else:
	PORT = 9999

listen_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
listen_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

socket_list = [listen_socket, sys.stdin]
lista = []

while True:
	print('while')
	try:
		R, W, X = sel.select(socket_list, [], [])
		for sckt in R:
			print('skt')
			if sckt is sys.stdin:
				msg = sys.stdin.readline().strip()
				if msg == 'EXIT':
					raise SystemExit()
			elif sckt is listen_socket:
				conn_sock, addr = listen_socket.accept()
				addr, port = conn_sock.getpeername()
				print(f'Novo cliente ligado desde {addr}:{port}')
				socket_list.append(conn_sock)
			else:
				msg = sckt.recv(1024)
				decoded = msg.decode()

				if decoded:
					resp = 'Ack'

					if decoded == 'LIST':
						resp = str(lista)
					elif decoded == 'CLEAR':
						lista = []
						resp = "Lista apagada"
					else:
						lista.append(decoded)

					sckt.sendall(resp.encode())
				else:  # isto pq o TCP tem o protocolo de finalização, e o select desbloqueia com uma mensagem vazia
					sckt.close()
					socket_list.remove(sckt)
					print('Cliente fechou a ligação')
	except (KeyboardInterrupt, SystemExit):
		break
	except:
		print(sys.exc_info())
		conn_sock.close()

listen_socket.close()