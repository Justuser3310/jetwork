from os import system
from db import *

print("(1) Создать сайт")
print("(2) Обновить сайт")
print("(3) Сменить тип")
op = input(">> ")

if op == "1":
	from verify import *
	from shutil import copyfile, make_archive
	from domain_check import *

	print("\nДомены: .jet")
	domain = input("Домен сайта: ")
	if not domain_ok(domain):
		print("Неправильный формат или домен.")
		exit()
	print("\n(1) Статичный / (2) Динамичный")
	type = input("Тип: ")

	system(f"mkdir mysites/{domain}")
	key_gen(f"mysites/{domain}")
	copyfile(f"mysites/{domain}.pem", f"mysites/{domain}/{domain}.pem")

	if type == "1":
		conf = {"type": "static", "ver": 1}
		write(conf, f"mysites/{domain}/config.json")
	elif type == "2":
		port = input("Порт: ")
		conf = {"type": "dynamic", "ver": 1, "port": int(port)}
		write(conf, f"mysites/{domain}/config.json")

	make_archive(f"mysites/{domain}", "zip", f"mysites/{domain}")
	sign(f"mysites/{domain}.zip", f"mysites/{domain}.key", f"mysites/{domain}")

elif op == "2":
	pass
elif op == "3":
	pass
