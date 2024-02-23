from os import system, name
from threading import Thread
from time import sleep

from network import *

# Здесь общий запуск всех файлов и команд
'''
# Проверка обновлений
from sys import argv
if len(argv) == 1:
	print("Проверка обновлений...")
	system("git pull")
	print("Перезагрузка скрипта...")
	system("python main.py updated")
	exit()
print("\nУспешно перезагружено!")
'''

# Порт для приёма всяких запросов
def reverse_proxy(dest, port = 8000):
	if name == "posix":
		system(f"./bore local {port} --to jetwork.404.mn --port {dest}")
	elif name == "nt":
		system(f"bore.exe local {port} --to jetwork.404.mn --port {dest}")

# Стартуем проброс порта
# http сервер
global http_port
http_port = port_gen()
rp_http = Thread(target = reverse_proxy, args=(http_port,))
rp_http.start()
print(f"Порт http сервера: {http_port}")
# сервер для пинга
serv_port = port_gen()
rp = Thread(target = reverse_proxy, args=(serv_port, 8001))
rp.start()
print(f"Порт сервера: {serv_port}")



# Стартуем сервисы
#http сервер
http = Thread(target = server_http)
http.start()
sleep(1)
os.chdir("../") # возвращаемся в корень
# сервер для пинга
server = Thread(target = server, args=(serv_port,))
server.start()


'''
# Режим отладки
mode = 1

if mode == 0:
	serv_http = Thread(target = server_http)
	serv_http.start()

	sleep(1)
	os.chdir("../") # возвращаемся в корень

	serv = Thread(target = server, args=(http_port,))
	serv.start()
elif mode == 1:
	pport = int(input())
	port_dest = client(pport, f"publish_just.jet<>{http_port}")
	print(port_dest)
#	if port_dest != "not exist":
#		client(port_dest, "get_just.jet")

'''
