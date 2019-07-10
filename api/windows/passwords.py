try:
	import win32crypt
except ImportError:
	pass


def win32decrypt(x):
	return win32crypt.CryptUnprotectData(x, None, None, None, 0)[1].decode('utf-8')
