def domain_ok(domain):
	domains = ["jet"]

	if domain.count(".") == 1:
		if domain.split(".")[1] in domains:
			return True

	return False
