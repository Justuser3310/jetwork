from os import system, name
from threading import Thread
from time import sleep

from network import *
from updater import *

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


from proxy import *

http_port = port_gen()
print(f"HTTP: {http_port}")
rp_http = Thread(target = watch_http, args=(http_port,))
rp_http.start()

serv_port = port_gen()
print(f"SERV: {serv_port}")
rp_serv = Thread(target = watch_serv, args=(serv_port,))
rp_serv.start()



# Стартуем сервисы
#http сервер
http = Thread(target = server_http)
http.start()
# сервер для пинга
server = Thread(target = server, args=(http_port,))
server.start()


# Стартуем авто-поиск портов и авто-обновление сайтов
updater = Thread(target = update_demon, args=(serv_port,))
updater.daemon = True
updater.start()

# Стартуем интерфейс
system(f"python -m streamlit run --server.address=127.0.0.1 interface.py {serv_port}")


while True:
	try:
		pass
	except:
		exit()

#print(client(8000, "ping"))
#ports = port_check(serv_port)
#print(ports)

#print(client(4015, "ping"))
#print(client(4137, "is_just.jet"))

#client(4092, "publish_just.jet<>4066")
