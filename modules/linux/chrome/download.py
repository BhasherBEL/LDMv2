# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.linux.chrome.chrome_module import ChromeModule


class LinuxChromeDownload(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='LinuxChromeDownload',
			version='0.1.2',
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
				self.cursor_get_and_log(cursor, 'target_path,tab_url,total_bytes,start_time', 'downloads', spe=os.path.split(profile)[1])

		return True
