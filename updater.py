# Здесь ищём порты и обновляем все сайты

from time import sleep
from db import *
from network import *

# Логирование ошибок
import logging

def update_demon(serv_port):
	while True:
		try:
			# Собираем порты
			ports = port_check(serv_port)

			conf = read()
			conf["ports"] = ports
			write(conf)

			# Перебираем всех клиентов
			for port in ports:
				try:
					# Проверяем у клиента его сайты и сравниваем
					raw = client(port, "check_all").split("<>")
					dest = [] # Приводим к виду ["just.j et", "2"]
					for i in raw:
						dest.append(i.split("_"))
					# Проверяем наши сайты
					raw = client(8001, "check_all", '127.0.0.1').split("<>")
					our = [] # Приводим к виду ["just.jet", "2"]
					for i in raw:
						our.append(i.split("_"))
					# Сравниваем
					for i in range(len(dest)):
						el = dest[i][0]
						ver = dest[i][1]
						# Проверяем есть ли у нас такое
						found = False
						for check in our:
							if check[0] == el:
								# Сверяем версии
								if check[1] >= ver:
									print("Ver_ok: ", el)
									pass
								else:
									# Если версия новее
									print("Ver_new: ", el)
									http_port = client(port, f"is_{el}")
									client(http_port, f"get_{el}")
								found = True
								break # Если нашли - выходим

						if not found:
							print("Not_found: ", el)
							http_port = client(port, f"is_{el}")
							client(http_port, f"get_{el}")
				except:
					pass

		except Exception as e:
			print("UPDATER FALLED")
			logging.critical(e, exc_info=True)
