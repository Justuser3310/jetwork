import http.server
import socketserver
import urllib.request
import logging

from db import *
domain = read()['domain']

# Логирование
#logging.basicConfig(level=ic, format='%(asctime)s - %(message)s')
from icecream import ic
ic.disable() # Выключить отладку

class Proxy(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		# Log the requested domain
		ic(f"Request for: {self.path}")

		# 'js-check.jet/favicon.ico' -> '127.0.0.1:8000/favicon.ico'
		target = self.path
		# Если статичный
		if 'jet' in target:
			target = f'{domain}/{target[7:]}' # http://127.0.0.1:8000 / js-check.jet
			ic(f"Modded request: {target}")
		elif 'dyn' in target:
			addr = target[target.find('://')+3:]
			addr = addr[:addr.find('/')]
			port = read(f'cached/{addr}/config.json')['port']
			target = f'http://bore.del.pw:{port}/{target[target.find("dyn")+4:]}'
			ic(f"Modded request: {target}")

		# Forward the request to the actual server
		try:
			with urllib.request.urlopen(target) as response:
				self.send_response(response.getcode())
				self.send_header("Content-type", response.headers.get_content_type())
				self.end_headers()
				self.wfile.write(response.read())
		except Exception as e:
			self.send_error(500, f"Error: {str(e)}")

	def do_POST(self):
		# Log the requested domain
		ic(f"Request for: {self.path}")

		if 'jet' in target:
			target = f'{domain}/{target[7:]}' # http://127.0.0.1:8000 / js-check.jet
			ic(f"Modded request: {target}")
		else:
			pass

		# Forward the request to the actual server
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
