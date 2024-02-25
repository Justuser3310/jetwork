from os import system, name
#from threading import Thread
from multiprocessing import Process
from time import sleep

global http_out ; http_out = None
def proxy_http(port):
	global http_out
	if name == "posix":
		http_out = system(f"./bore local 8000 --to jetwork.404.mn --port {port}")
	elif name == "nt":
		http_out = system(f"bore local 8000 --to jetwork.404.mn --port {port}")

global serv_out ; serv_out = None
def proxy_serv(port):
	global serv_out
	if name == "posix":
		http_out = system(f"./bore local 8001 --to jetwork.404.mn --port {port}")
	elif name == "nt":
	  http_out = system(f"bore local 8001 --to jetwork.404.mn --port {port}")


def watch_http(port):
	run = Process(target=proxy_http, args=(port,))
	run.start()

	global http_out
	while True:
		# Если команда вышла
		if http_out:
			run.terminate()
			http_out = None
			run = Process(target=proxy_http, args=(port,))
			run.start()
		sleep(1)

def watch_serv(port):
	run = Process(target=proxy_serv, args=(port,))
	run.start()

	global serv_out
	while True:
		if serv_out:
			run.terminate()
			serv_out = None
			run = Process(target=proxy_serv, args=(port,))
			run.start()
		sleep(1)
