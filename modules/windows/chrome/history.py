# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule


class WindowsChromeHistory(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='WindowsChromeHistory',
			version='0.1.0',
			file=__file__,
			dependencies=['os', 'sqlite3'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():
			history_path = profile + '/History'
			if os.path.isfile(history_path):
				connection = sqlite3.connect(history_path)
				cursor = connection.cursor()
				self.cursor_get_and_log(cursor, 'url,title,visit_count,last_visit_time', 'urls', spe=os.path.split(profile)[1])

		return True
