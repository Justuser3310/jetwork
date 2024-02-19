import socket
import os

# Здесь идёт обработка всех запросов через сеть

# TODO:
# 1. [+] Пинг
# 2. [+] Проверка существования .zip сайта
# 3. Передача сайта
# 4. Приём рассылки сайтов

def server(port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind (('127.0.0.1', port))

	while 1 :
		data , addres = sock.recvfrom(1024)
		#print (addres[0], addres[1])
		op = data.decode('utf-8')

		if op == "ping":
			sock.sendto("Pinged success".encode('utf-8'), addres)
		elif op[:3] == "is_":
			check = op[3:]
			if os.path.exists(f'cached/{check}'):
				sock.sendto("exist".encode('utf-8'), addres)
			else:
				sock.sendto("not exist".encode('utf-8'), addres)
		else:
			sock.sendto(data, addres)


# op = operation
def client(dest_port, op = "ping"):
	server = '127.0.0.1', dest_port

	sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sor.sendto((op).encode('utf-8'), server)
	sor.settimeout(5)

	try:
		data = sor.recv(1024)
		res = data.decode('utf-8')
		return res
	except:
		print(f"[:{dest_port}] Недоступен.")
		return None
