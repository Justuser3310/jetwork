import streamlit as st

st.title('jetwork')

# Получаем все сайты
from os import walk
sites = next(walk('cached/'), (None, None, []))[1]

for i in sites:
	addr = f"http://127.0.0.1:8000/{i}/index.html"
	f"[{i}]({addr})"
