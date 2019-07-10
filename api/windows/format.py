try:
	import win32crypt
	import datetime
except ImportError:
	pass


def win32decrypt(x):
	return win32crypt.CryptUnprotectData(x, None, None, None, 0)[1].decode('utf-8')


def chrome_time(x):
	try:
		return (datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=x)).timestamp()
	except TypeError:
		return 0


def firefox_time(x):
	try:
		return (datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=x)).timestamp()
	except TypeError:
		return 0
