import http.server
import socketserver
import urllib.request
import logging

from db import *
base_url = read()['base_url']

# Логирование
#logging.basicConfig(level=ic, format='%(asctime)s - %(message)s')
from icecream import ic
ic.disable() # Выключить отладку

class Proxy(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		ic(f"Request for: {self.path}")

		# 'js-check.jet/favicon.ico' -> '127.0.0.1:8000/favicon.ico'
		target = self.path
		domain = target[7:]
		domain = domain[:domain.find('/')]
		# Если статичный
		if read(f'cached/{domain}/config.json')['type'] == 'static':
			target = f'{base_url}/{target[7:]}' # http://127.0.0.1:8000 / js-check.jet
		# Если динамический
		elif read(f'cached/{domain}/config.json')['type'] == 'dynamic':
			port = read(f'cached/{domain}/config.json')['port']
			target = f'http://bore.del.pw:{port}/{target.replace(f"http://{domain}/", "")}'
		else:
			self.send_error(404, f"Site not found")
			return 0

		ic(f"Modded request: {target}")

		# Направление запроса по адресу
		try:
			with urllib.request.urlopen(target) as response:
				self.send_response(response.getcode())
				self.send_header("Content-type", response.headers.get_content_type())
				self.end_headers()
				self.wfile.write(response.read())
		except Exception as e:
			self.send_error(500, f"Error: {str(e)}")

	def do_POST(self):
		ic(f"Request for: {self.path}")

		if read(f'cached/{domain}/config.json')['type'] == 'static':
			target = f'{base_url}/{target[7:]}' # http://127.0.0.1:8000 / js-check.jet
		elif read(f'cached/{domain}/config.json')['type'] == 'dynamic':
			port = read(f'cached/{domain}/config.json')['port']
			target = f'http://bore.del.pw:{port}/{target.replace(f"http://{domain}/", "")}'
		else:
			self.send_error(404, f"Site not found")
			return 0

		ic(f"Modded request: {target}")

		# Направление запроса по адресу
		try:
			content_length = int(self.headers['Content-Length'])
			post_data = self.rfile.read(content_length)
			req = urllib.request.Request(self.path, data=post_data, method='POST')
			with urllib.request.urlopen(req) as response:
				self.send_response(response.getcode())
				self.send_header("Content-type", response.headers.get_content_type())
				self.end_headers()
				self.wfile.write(response.read())
		except Exception as e:
			self.send_error(500, f"Error: {str(e)}")

def web_proxy():
	PORT = 8080
	with socketserver.TCPServer(("", PORT), Proxy) as httpd:
		ic(f"Serving on port {PORT}")
		httpd.serve_forever()
