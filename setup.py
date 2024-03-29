from os import system, name
from urllib.request import urlretrieve as download

from db import *
config = {}

# Устанавливаем зависимости
system("pip install -r requirements.txt")

# Скачиваем bore (для проброса портов)
if name == "posix":
	download("https://github.com/ekzhang/bore/releases/download/v0.5.0/bore-v0.5.0-x86_64-unknown-linux-musl.tar.gz", "bore.tar.gz")
	system("tar -zxvf bore.tar.gz")
	system("rm -rf bore.tar.gz")

	import getpass
	user = getpass.getuser()

	system("mkdir ~/.streamlit")
	with open(f"/home/{user}/.streamlit/credentials.toml", "w") as f:
		f.write('[general]\nemail = "a@a.a"')
	f.close()
elif name == "nt":
	from shutil import unpack_archive as unpack
	download("https://github.com/ekzhang/bore/releases/download/v0.5.0/bore-v0.5.0-x86_64-pc-windows-msvc.zip", "bore.zip")
	unpack("bore.zip")
	system("del bore.zip")

	system("mkdir C:\\Users\\windows\\.streamlit")
	with open("C:\\Users\\windows\\.streamlit\\credentials.toml", "w") as f:
		f.write('[general]\nemail = "a@a.a"')
	f.close()
else:
	print("Увы, вероятно Ваша ОС не поддерживается.")
	print("Завершение работы...")
	exit()

# Создаём папку для кэшированных сайтов
system("mkdir cached")
system("mkdir verify")
system("mkdir mysites")

print("Максимальный размер для кэшированных файлов. (в гигабайтах)")
print("Укажите 0 для отключения ограничения.")
max = input(">> ")

# Записываем в конфиг
config["max"] = max
write(config)

print("\nЧтобы подключится к jetwork выполните: python main.py")
