# Работа с сетью
import socket
from requests import get
# Очевидно
import os
from random import randint
# Работа с архивами
from shutil import unpack_archive, copytree, rmtree
# Убираем ненужное (../some => some)
from re import compile, sub
# Работа с БД и json
from db import read
from json import loads

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
	while True:
		try:
			os.chdir("cached")
			os.system("python -m http.server")
		except:
			print("SERVER_HTTP FALLED")

def server(http_port):
	while True:
		try:
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

		except:
			print("SERVER FALLED")

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

	# Если порт не определён
	if not port:
		return None

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

		# Проверяем версию если сайт кеширован
		if os.path.exists(f"cached/{site}"):
			# Версия запрашиваемого
			dest_conf = get(f"http://{host}:{str(port)}/{site}/config.json")
			conf_unform = dest_conf.content.decode('utf8')
			conf = loads(conf_unform)
			dest_ver = conf["ver"]
			# Версия нашего сайта
			our_conf = read(f"cached/{site}/config.json")
			our_ver = our_conf["ver"]
			# Если версия не новее - не скачиваем
			if our_ver >= dest_ver:
				return "old"

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

		# Распаковываем архив с сайтом
		unpack_archive(f"verify/{site}.zip", f"verify/{site}")

		# Вторичная проверка версии если сайт в кэше
		# (мало ли какие гении нехорошие появятся)
		if os.path.exists(f'cached/{site}'):
			# Версия полученного
			dest_conf = read(f"verify/{site}/config.json")
			dest_ver = dest_conf["ver"]
			# Версия нашего сайта
			our_conf = read(f"cached/{site}/config.json")
			our_ver = our_conf["ver"]
			# Если версия не новее - злоумышленник
			if our_ver >= dest_ver:
				print("[!] Обнаружена подмена версии сайта.")
				# Сохраняем ключ злоумышленника
				os.replace(f"verify/{site}.pem", f"verify/{site}.pem.FAKE")
				print(f"[!] Порт злоумышленника: {port}")
				# Удаляем фальшивые файлы
				os.remove(f"verify/{site}.zip")
				os.remove(f"verify/{site}.sig")
				rmtree(f"verify/{site}")
				return "fake"

		if okay:
			# Перемещаем файлы, т.к. всё хорошо
			os.replace(f"verify/{site}.zip", f"cached/{site}.zip")
			os.replace(f"verify/{site}.sig", f"cached/{site}.sig")
			os.replace(f"verify/{site}.pem", f"cached/{site}.pem")
			# Переносим папку с файлами
			if os.path.exists(f'cached/{site}'):
				rmtree(f"cached/{site}")
			copytree(f"verify/{site}", f"cached/{site}")
			rmtree(f"verify/{site}")
		else:
			print("[!] Обнаружена подмена сайта.")
			# Сохраняем ключ злоумышленника
			os.replace(f"verify/{site}.pem", f"verify/{site}.pem.FAKE")
			print(f"[!] Порт злоумышленника: {port}")
			print(f"[!] Ключ (вероятно) злоумышленника сохранён в verify/{site}.pem.FAKE\n")
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
