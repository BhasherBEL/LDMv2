# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule
from internal import data_type
from api.windows import format


class WindowsChromeHistory(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='WindowsChromeHistory',
			version='0.1.1',
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
					[data_type.Link, ('url', 'title')],
					[data_type.Text, 'visit_count'],
					[data_type.Time, 'last_visit_time', format.chrome_time],
				],
				db='urls',
				spe=os.path.split(profile)[1],
			)

		return True
