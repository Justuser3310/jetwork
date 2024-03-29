import streamlit as st
import streamlit.components.v1 as components

from os import walk
from time import sleep
from db import *

# Получаем порт со входа
from sys import argv
our_port = argv[1]


st.title('jetwork')

ph = st.empty()

while True:
	# Боковая панель
	with ph.container():
		# Столбцы для элементов
		sidebar, space, main = st.columns([60, 10, 90])


	with sidebar:
		st.success(f"Ваш порт: {our_port}")

		conf = read()
		if 'ports' in conf:
			ports = conf['ports']
			for i in ports:
				st.warning(f"{i}")

	with main:
		# Получаем все сайты
		sites = next(walk('cached/'), (None, None, []))[1]

		for i in sites:
			addr = f"http://127.0.0.1:8000/{i}"
			st.info(f"[{i}]({addr})")

	sleep(3)
	ph.empty()
	st.rerun()
