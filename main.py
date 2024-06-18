from os import system, name
from time import sleep

from threading import Thread
from multiprocessing import Process

from network import *
from updater import *
from proxy import *
from status import *

# Здесь общий запуск всех файлов и команд



def main():
	# Проверка обновлений
	from sys import argv
	if len(argv) == 1:
		print("Проверка обновлений...")
		system("git pull")
		print("Перезагрузка скрипта...")
		system("python main.py updated")
		exit()
	print("\nУспешно перезагружено!")

	# Запуск прокси для сервисов
	# проксируем http сервер
	http_port = port_gen()
	print(f"HTTP: {http_port}")
	rp_http = Thread(target = watch_http, args=(http_port,))
	rp_http.start()

	# проксируем сервер обработки запросов
	serv_port = port_gen()
	print(f"SERV: {serv_port}")
	rp_serv = Thread(target = watch_serv, args=(serv_port,))
	rp_serv.start()

	# Стартуем сервисы
	# http сервер
	http = Thread(target = server_http)
	http.start()
	# сервер обработки запросов
	srv = Thread(target = server, args=(http_port,))
	srv.start()

	# Стартуем авто-поиск портов и авто-обновление сайтов
	updater = Thread(target = update_demon, args=(serv_port,))
	updater.start()

	# !!! ИДЁТ ПЕРЕРАБОТКА !!!
	# Стартуем интерфейс
	system(f"python -m streamlit run --server.address=127.0.0.1 interface.py {serv_port}")

if __name__ == "__main__":
	# Запускаем главный процесс, чтобы потом легко убить его
	p = Process(target=main)
	p.start()

	status_set(True) # Устанавливаем статус, что программа работает

	st = status_check()
	while st:
		try:
			st = status_check()
			sleep(0.01)
		except KeyboardInterrupt:
			p.terminate()
			exit()
		except:
			pass

	# Когда послан код завершения
	p.terminate()
	exit()
