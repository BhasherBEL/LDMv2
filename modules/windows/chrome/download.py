# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule
from internal import data_type


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

			self.cursor_getV2(
				path=profile + '/History',
				items=[
					[data_type.File, ('target_path', 'total_bytes')],
					[data_type.Link, 'tab_url'],
					[data_type.Time, 'start_time'],
				],
				db='downloads',
				spe=os.path.split(profile)[1],
			)

		return True
