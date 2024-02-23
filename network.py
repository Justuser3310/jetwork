# Работа с сетью
import socket
from requests import get
# Очевидно
import os
from random import randint
# Работа с архивами
from shutil import unpack_archive
# Убираем ненужное (../some => some)
from re import compile, sub
# Timeout для команды

from verify import *
from domain_check import *

# Здесь идёт обработка всех запросов через сеть

# TODO:
# 1. [+] Пинг
# 2. [+] Проверка существования сайта
# 3. [+] Передача сайта
# 4. [+] Приём рассылки сайтов
# 5. Проверка всех сайтов

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
				# Защита от доступа выше и т.п.
				check = domain_ok(check)

				if os.path.exists(f'cached/{check}'):
					conn.send(str(http_port).encode())
				else:
					conn.send("not_exist".encode())
			elif op[:8] == "publish_":
				data = op[8:]
				site, port = data.split("<>")
				site = domain_ok(site)
				if site:
					conn.send("accepted".encode())
					client(port, f"get_{site}")

		conn.close()

def recv(q, s):
	okay = False
	while not okay:
		try:
			data = s.recv(1024).decode()
			okay = True
		except:
			pass
	q.put(data)

import multiprocessing as mp
# op = operation
def client(port, op = "ping"):
	host = 'jetwork.404.mn'

	if op == "ping" or op[:3] == "is_" or op[:8] == "publish_":
		s = socket.socket()
		try:
			s.connect((host, port))
		except:
			return None

		s.send(op.encode())

		# Канал обмена процесс - наша функция
		q = mp.Queue()
		# Стартуем процесс получения ответа
		p = mp.Process(target=recv, args=(q, s))
		p.start()
		# Ждём 10 секунд - максимум
		p.join(10)

		try:
			data = q.get(block=False)
		except:
			data = None

		# Если процесс жив - убираем
		if p.is_alive():
			p.terminate()

		s.close()

		return data
	elif op[:4] == "get_":
		site = op[4:]
		# Скачиваем файлы
		g_site = get(f"http://{host}:{str(port)}/{site}.zip")
		print('SIZE: ', g_site.headers['Content-Length']) # Размер

		with open(f"verify/{site}.zip", "wb") as f:
			f.write(g_site.content)
			f.close()

		g_sig = get(f"http://{host}:{str(port)}/{site}.sig")
		with open(f"verify/{site}.sig", "wb") as f:
			f.write(g_sig.content)
			f.close()

		g_key = get(f"http://{host}:{str(port)}/{site}.pem")
		with open(f"verify/{site}.pem", "wb") as f:
			f.write(g_key.content)
			f.close()

		# Проверяем подпись
		# Если сайт уже есть в кэше:
		if os.path.exists(f'cached/{site}'):
			okay = verify(f"verify/{site}.zip", f"cached/{site}.pem", f"verify/{site}.sig")
		else:
			okay = verify(f"verify/{site}.zip", f"verify/{site}.pem", f"verify/{site}.sig")

		if okay:
			# Перемещаем файлы, т.к. всё хорошо
			os.replace(f"verify/{site}.zip", f"cached/{site}.zip")
			os.replace(f"verify/{site}.sig", f"cached/{site}.sig")
			os.replace(f"verify/{site}.pem", f"cached/{site}.pem")
			# Распаковываем архив с сайтом
			unpack_archive(f"cached/{site}.zip", f"cached/{site}")
		else:
			print("[!] Обнаружена подмена сайта.")
			# Сохраняем ключ злоумышленника
			os.replace(f"verify/{site}.pem", f"verify/{site}.pem.FAKE")
			print(f"[!] Порт злоумышленника: {port}")
			print(f"[!] Ключ злоумышленника сохранён в verify/{site}.pem.FAKE\n")
			# Удаляем фальшивые файлы
			os.remove(f"verify/{site}.zip")
			os.remove(f"verify/{site}.sig")


from tqdm import tqdm
def port_check(your_port):
	ports = []

	checks = list(range(4000, 4200))
	checks.remove(your_port)
	for port in tqdm(checks):
		if client(port, "ping"):
			ports.append(port)

	return ports
