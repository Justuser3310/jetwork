from os import system, mkdir
from db import *
from shutil import copyfile, make_archive, rmtree, copytree
from tqdm import tqdm
from time import sleep

from verify import *
from network import *

print("(1) Создать сайт")
print("(2) Обновить сайт")
print("(3) Сменить тип")
print("(4) Авто-раздача сайта")
print("Enter для просто публикации.")

op = input(">> ")

if op == "1":
	from domain_check import *

	print("\nДомены: .jet")
	domain = input("Домен сайта: ")
	if not domain_ok(domain):
		print("Неправильный формат или домен.")
		exit()
	print("\n(1) Статичный / (2) Динамичный")
	type = input("Тип: ")

	# Создаём папку и ключи для подписи
	mkdir(f"mysites/{domain}")
	key_gen(f"mysites/{domain}")

	if type == "1":
		conf = {"type": "static", "ver": 1}
		print("ПРИМЕЧАНИЕ: index.html обязателен.")
	elif type == "2":
		print("В разработке...")
		exit()
		port = input("Порт: ")
		conf = {"type": "dynamic", "ver": 1, "port": int(port)}
	write(conf, f"mysites/{domain}/config.json")

	# Создаём index.html для загрузки сайта
	with open(f"mysites/{domain}/index.html", "w") as f:
		f.write("<h1> Hello jetwork! </h1>")
	f.close()

	# Архивируем и создаём сигнатуру для подтверждения неизменности архива
	make_archive(f"mysites/{domain}", "zip", f"mysites/{domain}")
	sign(f"mysites/{domain}.zip", f"mysites/{domain}.key", f"mysites/{domain}")

elif op == "2":
	domain = input("\nДомен сайта: ")
	if not os.path.exists(f"mysites/{domain}"):
		print("Не существует такого сайта.")
		exit()

	# Обновляем версию
	conf = read(f"mysites/{domain}/config.json")
	conf["ver"] = conf["ver"] + 1
	write(conf, f"mysites/{domain}/config.json")

	# Архивируем и создаём сигнатуру для подтверждения неизменности архива
	make_archive(f"mysites/{domain}", "zip", f"mysites/{domain}")
	sign(f"mysites/{domain}.zip", f"mysites/{domain}.key", f"mysites/{domain}")

elif op == "3":
	from os import rmdir

	domain = input("\nДомен сайта: ")
	if not os.path.exists(f"mysites/{domain}"):
		print("Не существует такого сайта.")
		exit()

	print("\n(1) Статичный / (2) Динамичный")
	type = input("Тип: ")

	if type == "1":
		conf = read(f"mysites/{domain}/config.json")
		conf["type"] = "static"
		conf.pop("port")
	elif type == "2":
		conf = read(f"mysites/{domain}/config.json")
		port = input("Порт: ")

		clean = input("Удалить все файлы (y/n): ")
		if clean == "y":
			# Удаляем папку, сохраняем конфиг и копируем публичный ключ
			rmtree(f"mysites/{domain}")
			system(f"mkdir mysites/{domain}")
			copyfile(f"mysites/{domain}.pem", f"mysites/{domain}/{domain}.pem")

		conf["type"] = "dynamic"
		conf["port"] = int(port)
	write(conf, f"mysites/{domain}/config.json")

	# Обновляем версию
	conf = read(f"mysites/{domain}/config.json")
	conf["ver"] = conf["ver"] + 1
	write(conf, f"mysites/{domain}/config.json")

	# Архивируем и создаём сигнатуру для подтверждения неизменности архива
	make_archive(f"mysites/{domain}", "zip", f"mysites/{domain}")
	sign(f"mysites/{domain}.zip", f"mysites/{domain}.key", f"mysites/{domain}")

	exit()

elif op == "4":
	domain = input("\nДомен сайта: ")
	if not os.path.exists(f"mysites/{domain}"):
		print("Не существует такого сайта.")
		exit()

	print("\nВведите ваш порт сервера (при запуске main.py)")
	serv_port = int(input(">> "))
	http_port = client(serv_port, f"is_{domain}")

	print("\nСтарт вечной раздачи...")
	while True:
		ports = port_check(serv_port)
		sleep(1)
		for port in tqdm(ports):
			client(port, f"publish_{domain}<>{http_port}")
		sleep(5)

elif op == "":
	domain = input("\nДомен сайта: ")
	if not os.path.exists(f"mysites/{domain}"):
		print("Не существует такого сайта.")
		exit()
	pub = "y"


# Копируем файлы из mysites в cached
try:
	rmtree(f"cached/{domain}")
except:
	pass
copytree(f"mysites/{domain}", f"cached/{domain}")
copyfile(f"mysites/{domain}.pem", f"cached/{domain}.pem")
copyfile(f"mysites/{domain}.sig", f"cached/{domain}.sig")
copyfile(f"mysites/{domain}.zip", f"cached/{domain}.zip")


if op != "":
	print("Опубликовать сайт?")
	pub = input("y/n >> ")

if pub == "n":
	exit()

print("Введите ваш порт сервера (при запуске main.py)")
serv_port = int(input(">> "))
http_port = client(serv_port, f"is_{domain}")

print("Получаем все порты...")
ports = port_check(serv_port)

print(ports)

print("Публикуем сайт...")
for port in tqdm(ports):
	client(port, f"publish_{domain}<>{http_port}")
