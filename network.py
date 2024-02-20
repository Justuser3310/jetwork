import socket
from requests import get
import os
from random import randint

# Здесь идёт обработка всех запросов через сеть

# TODO:
# 1. [+] Пинг
# 2. [+] Проверка существования сайта
# 3. Передача сайта
# 4. Приём рассылки сайтов

def port_gen():
	port = randint(4000, 4200)
	if client(port) == None:
		return port

	while client(port) != None:
		port = randint(4000, 4200)
	return port

def server_http():
	os.chdir("cached")
	os.system("python -m http.server")

def server(http_port):
	host = "127.0.0.1"
	port = 8001

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
					conn.send(str(http_port).encode())
				else:
					conn.send("not exist".encode())
		conn.close()

# op = operation
def client(port, op = "ping"):
	host = 'jetwork.404.mn'

	#if op == "ping":
	#	r = get(f"http://{host}:{str(port)}/jetwork")
	#	print(r.headers['Content-Length'])

	if op == "ping" or op[:3] == "is_":
		s = socket.socket()
		try:
			s.connect((host, port))
		except:
			return None

		s.send(op.encode())
		okay = False
		while not okay:
			try:
				data = s.recv(1024).decode()
				okay = True
			except:
				pass
		print(data)

		s.close()
		return data
