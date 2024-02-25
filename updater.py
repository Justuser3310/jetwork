# Здесь ищём порты и обновляем все сайты

from time import sleep
from db import *
from network import *

def update_demon(serv_port):
	while True:
		ports = port_check(serv_port)

		conf = read()
		conf["ports"] = ports
		write(conf)

		sleep(8)
