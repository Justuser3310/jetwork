# name - директория и имя (path/name.key)
def key_gen(name):
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import serialization
	from cryptography.hazmat.primitives.asymmetric import rsa

	# Generate the public/private key pair.
	private_key = rsa.generate_private_key(
		public_exponent = 65537,
		key_size = 4096,
		backend = default_backend(),
	)

	# Save the private key to a file.
	with open(f'{name}.key', 'wb') as f:
		f.write(
			private_key.private_bytes(
				encoding=serialization.Encoding.PEM,
				format=serialization.PrivateFormat.TraditionalOpenSSL,
				encryption_algorithm=serialization.NoEncryption(),
			)
		)

	# Save the public key to a file.
	with open(f'{name}.pem', 'wb') as f:
		f.write(
			private_key.public_key().public_bytes(
			encoding = serialization.Encoding.PEM,
			format = serialization.PublicFormat.SubjectPublicKeyInfo,
			)
		)



def sign(file, priv_key, sig):
	import base64
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives import serialization
	from cryptography.hazmat.primitives.asymmetric import padding

	# Load the private key.
	with open(priv_key, 'rb') as key_file:
		private_key = serialization.load_pem_private_key(
			key_file.read(),
			password = None,
			backend = default_backend(),
		)

	# Load the contents of the file to be signed.
	with open(file, 'rb') as f:
		payload = f.read()

	# Sign the payload file.
	signature = base64.b64encode(
		private_key.sign(
			payload,
			padding.PSS(
				mgf = padding.MGF1(hashes.SHA256()),
				salt_length = padding.PSS.MAX_LENGTH,
			),
			hashes.SHA256(),
		)
	)

	with open(f'{sig}.sig', 'wb') as f:
	    f.write(signature)



def verify(file, pub_key, sig):
	import base64
	import cryptography.exceptions
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives.asymmetric import padding
	from cryptography.hazmat.primitives.serialization import load_pem_public_key

	# Load the public key.
	with open(pub_key, 'rb') as f:
		public_key = load_pem_public_key(f.read(), default_backend())

	# Load the payload contents and the signature.
	with open(file, 'rb') as f:
		payload_contents = f.read()
	with open(sig, 'rb') as f:
		signature = base64.b64decode(f.read())

	# Perform the verification.
	try:
		public_key.verify(
			signature,
			payload_contents,
			padding.PSS(
				mgf = padding.MGF1(hashes.SHA256()),
				salt_length = padding.PSS.MAX_LENGTH,
			),
			hashes.SHA256(),
		)
		return True
	except cryptography.exceptions.InvalidSignature as e:
		print('ERROR: Payload and/or signature files failed verification!')
		return False
