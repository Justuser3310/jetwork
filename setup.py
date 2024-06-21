from os import system
from urllib.request import urlretrieve as download

from db import *

print('''1. Linux
2. Windows
3. Android (Termux)''')
raw_os = input('ОС установки >> ')
oses = {'1': 'Linux', '2': 'Windows', '3': 'Android'}
os = oses[raw_os]

# Записываем ОС в конфиг
conf = read()
conf['os'] = os
write(conf)

print('''---
[1/3] Устанавливаем зависимости python...
---''')
system('pip install -r requirements.txt')

print('''---
[2/3] Скачиваем обратный прокси...
---''')
if os == 'Linux':
	download('https://github.com/ekzhang/bore/releases/download/v0.5.0/bore-v0.5.0-x86_64-unknown-linux-musl.tar.gz', 'bore.tar.gz')
	system('tar -zxvf bore.tar.gz')
	system('rm -rf bore.tar.gz')
elif os == 'Windows':
	from shutil import unpack_archive as unpack
	download('https://github.com/ekzhang/bore/releases/download/v0.5.0/bore-v0.5.0-x86_64-pc-windows-msvc.zip', 'bore.zip')
	unpack('bore.zip')
	system('del bore.zip')
elif os == 'Android':
	system('pkg install bore-cli')
else:
	print('Увы, вероятно Ваша ОС не поддерживается.')
	print('Завершение работы...')
	exit()

print('''---
[3/3] Создаём папки для работы...
---''')
system('mkdir cached')
system('mkdir verify')
system('mkdir mysites')

# TODO
#print('Максимальный размер для кэшированных файлов. (в гигабайтах)')
#print('Укажите 0 для отключения ограничения.')
#max = input('>> ')
# Записываем в конфиг
#config['max'] = max
#write(config)

print('''
---
Установка завершена!

Чтобы подключится к jetwork выполните: python main.py
---''')
