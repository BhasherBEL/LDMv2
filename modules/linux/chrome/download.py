# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.linux.chrome.chrome_module import ChromeModule


class ChromeDownload(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='ChromeDownload',
			version='0.1.1',
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
			download_path = profile + '/History'
			if os.path.isfile(download_path):
				self.log(profile.split('/')[-1] + ':')
				connection = sqlite3.connect(download_path)
				cursor = connection.cursor()
				try:
					cursor.execute('SELECT target_path, start_time, total_bytes, tab_url FROM downloads')
				except sqlite3.OperationalError:
					self.executenot(download_path + ' database is locked', 1)
					return False

				self.log('target_path,url,size,time')
				for target_path, start_time, total_bytes, tab_url in cursor.fetchall():
					self.log(target_path + ',' + tab_url + ',' + str(total_bytes) + ',' + str(start_time))

		return True
