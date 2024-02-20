import socket
import os

# Здесь идёт обработка всех запросов через сеть

# TODO:
# 1. [+] Пинг
# 2. [+] Проверка существования сайта
# 3. Передача сайта
# 4. Приём рассылки сайтов

def server(port = 8000):
	host = "127.0.0.1"

	s = socket.socket()
	s.bind((host, port))

	while True:
		s.listen(2)
		conn, address = s.accept()

		print("Connection from: " + str(address))

		while True:
			try:
				op = conn.recv(1024).decode()
			except:
				pass
			if not op:
				break

			if op == "ping":
				conn.send("pong".encode())
			elif op[:3] == "is_":
				check = op[3:]
				if os.path.exists(f'cached/{check}'):
					conn.send("exist".encode())
				else:
					conn.send("not exist".encode())
		conn.close()

# op = operation
def client(port, op = "ping"):
	host = 'jetwork.404.mn'
	s = socket.socket()
	s.connect((host, port))

	s.send(op.encode())
	data = s.recv(1024).decode()
	print('Received from server: ' + data)

	s.close()
	return data
