#
# Установка/проверка статуса завершения
#

import os

if not os.path.exists('status'):
	f = open('status', 'w')
	f.write('work')
	f.close()

def status_check():
	f = open('status', 'r')
	st = f.read()
	if st == 'work':
		return True
	else:
		return False

def status_set(st):
	f = open('status', 'w')
	if st == True:
		f.write('work')
	else:
		f.write('stop')
	f.close()
