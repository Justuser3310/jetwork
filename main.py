from os import system, name
from threading import Thread

# Здесь общий запуск всех файлов и команд

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
def reverse_proxy():
	port = 8000
	if name == "posix":
		system(f"./bore local {port} --to jetwork.404.mn")
	elif name == "nt":
		system("")

# Стартуем проброс порта
rp = Thread(target = reverse_proxy)
rp.start()
'''

'''
from network import *

#server(8000)

if client(8001):
	print(1)
else:
	print(2)
'''

