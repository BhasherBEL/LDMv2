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
			history_path = profile + '/History'
			if os.path.isfile(history_path):
				connection = sqlite3.connect(history_path)
				cursor = connection.cursor()
				self.cursor_get_and_log(cursor, 'url,title,visit_count,last_visit_time', 'urls', spe=os.path.split(profile)[1])

		return True
