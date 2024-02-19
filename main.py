from os import system, name
from threading import Thread
from time import sleep

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
from random import randint
dest = randint(4000, 4200)
def reverse_proxy():
	global dest
	port = 8000
	if name == "posix":
		system(f"./bore local {port} --to jetwork.404.mn --port {dest}")
	elif name == "nt":
		system(f"bore.exe local {port} --to jetwork.404.mn --port {dest}")

'''
# Стартуем проброс порта
rp = Thread(target = reverse_proxy)
rp.start()
sleep(0.5)
'''
print(f"\nВаш порт: {dest}")

from network import *

#server(8001)
client(8001)

