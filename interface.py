from dash import Dash, dcc, html, Input, Output, callback
app = Dash(__name__, title='Jetwork', update_title=None)

from db import *
from os import walk

app.layout = html.Div([ html.Div([

html.Div([], id='our_port', className='our_port'),
html.Div([], id='servers', className='servers'),
html.Div([], id='sites', className='sites'),
#dcc.Input(className='search', type='search', list=[1,2,3]),
dcc.Dropdown(options=[], id='search', placeholder='Поиск...'),

dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)

], className='main')], className='content')



# Обновление нашего порта (зачем?)
@callback(Output('our_port', 'children'),
					Input('interval-component', 'n_intervals'))
def update_our_port(n):
	return f"Ваш порт: {read()['our_port']}"

# Обновление доступных узлов
@callback(Output('servers', 'children'),
          Input('interval-component', 'n_intervals'))
def update_servers(n):
	res = []
	for i in read()['ports']:
		res.append(html.Div([i], className='serv_elem'))
	return res

# Обновление доступных сайтов
@callback(Output('sites', 'children'),
					Input('interval-component', 'n_intervals'),
					Input('search', 'value'))
def update_sites(n, s_val):
	# Если есть элемент в поиске
	if s_val:
		return html.Div([ dcc.Link(children=i, href=f'http://0.0.0.0:8000/{s_val}',
		target='_blank') ], className='sites_elem')

	res = []
	for i in next(walk('cached/'), (None, None, []))[1]:
		res.append(html.Div([ dcc.Link(children=i, href=f'http://0.0.0.0:8000/{i}',
													target='_blank') ], className='sites_elem'))
	return res

# Обновление доступных сайтов в поиске
@callback(Output('search', 'options'),
          Input('interval-component', 'n_intervals'))
def update_search(n):
	res = []
	for i in next(walk('cached/'), (None, None, []))[1]:
		res.append(i)
	return res

#app.run(debug=True, port = 5555)
app.run(debug=False, port = 5555)
