try:
	import sqlite3
	import os
except ImportError:
	pass

from modules.windows.firefox.firefox_module import FirefoxModule
from internal import data_type


class WindowsFirefoxCookie(FirefoxModule):
	def __init__(self):
		FirefoxModule.__init__(
			self,
			name='WindowsFirefoxCookie',
			version='0.1.0',
			file=__file__,
			dependencies=['sqlite3', 'os'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():

			self.cursor_getV2(
				path=os.path.join(profile, 'cookies.sqlite'),
				items=[
					[data_type.Link, 'baseDomain'],
					[data_type.Text, 'name'],
					[data_type.Text, 'value'],
				],
				db='moz_cookies',
				header=['url', 'name', 'value'],
				spe=os.path.split(profile)[1],
			)

		return True

