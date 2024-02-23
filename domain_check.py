from re import compile, sub

def domain_ok(domain):
	domains = ["jet"]

	if domain.count(".") == 1:
		if domain.split(".")[1] in domains:
			# ../some => some
			# Защита от проверки папок выше, чем нужно и др.
			regex = compile('[^a-zA-Zа-яА-ЯЁё.]')
			c_domain = regex.sub('', domain)
			if domain == c_domain:
				return domain

	return False
