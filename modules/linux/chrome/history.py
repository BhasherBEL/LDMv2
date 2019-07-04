# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.linux.chrome.chrome_module import ChromeModule


class LinuxChromeHistory(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='LinuxChromeHistory',
			version='0.1.0',
			file=__file__,
			dependencies=['os', 'sqlite3'],
		)

	def can(self):
		return super().can()

	def has(self):
		return super().has()

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():
			history_path = profile + '/History'
			if os.path.isfile(history_path):
				self.log(profile.split('/')[-1] + ':')
				connection = sqlite3.connect(history_path)
				cursor = connection.cursor()
				try:
					cursor.execute('SELECT url, title, visit_count, last_visit_time FROM urls')
				except sqlite3.OperationalError:
					self.executenot(history_path + ' database is locked', 1)
					return False

				self.log('url,title,visit_count,last_visit_time')
				for url, title, visit_count, last_visit_time in cursor.fetchall():
					self.log(url + ',' + title + ',' + str(visit_count) + ',' + str(last_visit_time))

		return True
