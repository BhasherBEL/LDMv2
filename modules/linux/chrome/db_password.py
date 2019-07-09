# coding: utf-8

try:
	import os
	import sqlite3
	from urllib import parse
except ImportError:
	pass

from modules.linux.chrome.chrome_module import ChromeModule


class LinuxChromeDbPassword(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='LinuxChromeDbPassword',
			version='0.1.1',
			file=__file__,
			dependencies=['os', 'sqlite3', 'urllib.parse'],
		)

	def can(self):
		return super().can()

	def has(self):
		return super().has()

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():
			download_path = profile + '/Login Data'
			if os.path.isfile(download_path):
				self.log(profile.split('/')[-1] + ':')
				connection = sqlite3.connect(download_path)
				cursor = connection.cursor()

				self.cursor_get_and_log(cursor, 'origin_url,username_value,password_value,date_created',
										'logins WHERE blacklisted_by_user = 0', decrypt_ids=[0],
										decrypt_algo=self.parse_hostname, spe=os.path.split(profile)[1])

				self.cursor_get_and_log(cursor, 'origin_url,date_created',
										'logins WHERE blacklisted_by_user = 1', decrypt_ids=[0],
										decrypt_algo=self.parse_hostname, spe=os.path.split(profile)[1])
		return True

	@staticmethod
	def parse_hostname(origin):
		hostname_split = parse.urlsplit(origin)
		return parse.urlunsplit((hostname_split.scheme, hostname_split.netloc, "", "", ""))