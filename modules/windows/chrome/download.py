# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule


class WindowsChromeDownload(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='WindowsChromeDownload',
			version='0.1.0',
			file=__file__,
			dependencies=['os', 'sqlite3'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():
			download_path = profile + '/History'
			if os.path.isfile(download_path):
				self.log(profile.split('/')[-1] + ':')
				connection = sqlite3.connect(download_path)
				cursor = connection.cursor()
				self.cursor_get_and_log(cursor, 'target_path,tab_url,total_bytes,start_time', 'downloads')

		return True
