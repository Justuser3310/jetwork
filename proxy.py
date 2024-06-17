from os import system, name
from threading import Thread
from time import sleep

global http_out ; http_out = None
def proxy_http(port):
	global http_out
	if name == "posix":
		http_out = system(f"./bore local 8000 --to bore.pub --port {port}")
	elif name == "nt":
		http_out = system(f"bore local 8000 --to bore.pub --port {port}")

global serv_out ; serv_out = None
def proxy_serv(port):
	global serv_out
	if name == "posix":
		http_out = system(f"./bore local 8001 --to bore.pub --port {port}")
	elif name == "nt":
	  http_out = system(f"bore local 8001 --to bore.pub --port {port}")


def watch_http(port):
	run = Thread(target=proxy_http, args=(port,))
	run.start()

	global http_out
	while True:
		# Если команда вышла
		if http_out or not run.is_alive():
			run.join(1)
			http_out = None
			run = Thread(target=proxy_http, args=(port,))
			run.start()
		sleep(1)

def watch_serv(port):
	run = Thread(target=proxy_serv, args=(port,))
	run.start()

	global serv_out
	while True:
		if serv_out or not run.is_alive():
			run.join(1)
			serv_out = None
			run = Thread(target=proxy_serv, args=(port,))
			run.start()
		sleep(1)
