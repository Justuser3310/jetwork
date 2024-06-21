from os import system
from threading import Thread
from time import sleep

from status import *
from db import read

global http_out ; http_out = None
def proxy_http(port):
	global http_out
	os = read()['os']
	if os == 'Linux':
		http_out = system(f'./bore local 8000 --to bore.pub --port {port}')
	elif os == 'Windows' or os == 'Android':
		http_out = system(f'bore local 8000 --to bore.pub --port {port}')

global serv_out ; serv_out = None
def proxy_serv(port):
	global serv_out
	os = read()['os']
	if os == 'Linux':
		http_out = system(f'./bore local 8001 --to bore.pub --port {port}')
	elif os == 'Windows' or os == 'Android':
	  http_out = system(f'bore local 8001 --to bore.pub --port {port}')


def watch_http(port):
	run = Thread(target=proxy_http, args=(port,))
	run.start()

	global http_out
	st = status_check()
	while st:
		# Если команда вышла
		if http_out or not run.is_alive():
			run.join(1)
			http_out = None
			run = Thread(target=proxy_http, args=(port,))
			run.start()
		st = status_check()
		sleep(1)

def watch_serv(port):
	run = Thread(target=proxy_serv, args=(port,))
	run.start()

	global serv_out
	st = status_check()
	while st:
		if serv_out or not run.is_alive():
			run.join(1)
			serv_out = None
			run = Thread(target=proxy_serv, args=(port,))
			run.start()
			st = status_check()
		sleep(1)
