from re import compile, sub
domains = ['jet', 'mirror', 'org', 'info', 'news', 'me']

def domain_ok(domain):
	global domains
	if domain.count('.') == 1:
		if domain.split('.')[1] in domains:
			# ../some => some
			# Защита от проверки папок выше, чем нужно и др.
			regex = compile('[^a-z0-9.-]')
			c_domain = regex.sub('', domain)
			if domain == c_domain:
				return domain

	return False

def domain_list():
	global domains
	out = ''
	for i in domains:
		out += f'{i}, '
	out = out[:-2]
	return out
