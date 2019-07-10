# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.windows.chromium.chromium_module import ChromiumModule
from internal import data_type
from api.windows import format


class WindowsChromiumHistory(ChromiumModule):
	def __init__(self):
		ChromiumModule.__init__(
			self,
			name='WindowsChromiumHistory',
			version='0.1.2',
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
