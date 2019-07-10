try:
	import win32crypt
	import datetime
except ImportError:
	pass


def win32decrypt(x):
	"""
	Decrypt data with win32decrypt module
	"""
	return win32crypt.CryptUnprotectData(x, None, None, None, 0)[1].decode('utf-8')


def chrome_time(x):
	"""
	Convert chromium time to timestamp. Chrome uses the number of microseconds spent since January 1, 1601
	"""
	try:
		return (datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=x)).timestamp()
	except TypeError:
		return 0


def firefox_time(x):
	"""
	Convert firefox time to timestamp. Firefox uses the number of microseconds spent since January 1, 1970
	"""
	try:
		return (datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=x)).timestamp()
	except TypeError:
		return 0
