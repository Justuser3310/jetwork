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
# Логирование ошибок
import logging

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
			os.system("python -m http.server --directory cached")
		except Exception as e:
			print("SERVER_HTTP FALLED")
			logging.critical(e, exc_info=True)

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
					elif op == "check_all":
						try:
							sites = next(os.walk('cached/'), (None, None, []))[1]
							sites_comp = ""
							for i in sites:
								# Проверяем версию
								ver = read(f"cached/{i}/config.json")["ver"]
								sites_comp += i + f"_{ver}<>"
							sites_comp = sites_comp[:-2]
							if sites_comp == "":
								conn.send("None".encode())
							else:
								conn.send(sites_comp.encode())
						except:
							conn.send("None".encode())
				conn.close()

		except Exception as e:
			print("SERVER_HTTP FALLED")
			logging.critical(e, exc_info=True)


from time import time
from threading import Thread
from queue import Queue

def recv(s, data_out):
	okay = False
	while not okay:
		try:
			data = s.recv(1024).decode()
			okay = True
		except:
			pass
	print(data)
	data_out.put(data)

# op = operation
def client(port, op = "ping", host = 'jetwork.404.mn'):
	# Если порт не определён
	if not port:
		return None

	if op == "ping" or op[:3] == "is_" or op[:8] == "publish_" or op == "check_all":
		s = socket.socket()
		try:
			s.connect((host, port))
		except:
			return None

		s.send(op.encode())

		data = Queue()

		ping = Thread(target = recv, args=(s, data,))
		# Стартуем пинг
		ping.start()

		# Ждём 8 секунд
		ping.join(6)

		# Закрываем соединение
		s.close()

		if not data.empty():
			return data.get()
		else:
			return None

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

		# Перезаписываем index.html на всякий случай
		# Проверяем тип сайта
		type = read(f"cached/{site}/config.json")["type"]
		# Если динамический
		if type == "dynamic":
			port = read(f"cached/{site}/config.json")["port"]
			with open(f"cached/{site}/index.html", "w") as f:
				f.write(f'<iframe src="http://{host}:{port}" style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;"></iframe>')
			f.close()


global ports
ports = []

def check_current(cur_port):
	global ports
	if client(cur_port, "ping"):
		ports.append(cur_port)

def check_wait(port):
	ping = Thread(target = check_current, args=(port,))
	ping.start()
	ping.join(8)
	exit()

# 1. Стартуем все потоки которые вырубают другие потоки, если прошло 8 секунд
# 2. Ожидающие потоки стартуют проверку порта
# => моментальная проверка 200 портов

from tqdm import tqdm
from time import sleep
def port_check(your_port):
	global ports
	ports = []

	checks = list(range(4000, 4200))
	checks.remove(your_port)

	for port in tqdm(checks):
		wait = Thread(target = check_wait, args=(port,))
		wait.start()

	sleep(10)

	return ports


#print( port_check(4001) )
#print( client(4085, "ping") )
