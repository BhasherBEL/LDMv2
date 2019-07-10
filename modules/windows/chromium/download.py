# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.windows.chromium.chromium_module import ChromiumModule
from internal import data_type
from api.windows import format


class WindowsChromiumDownload(ChromiumModule):
	def __init__(self):
		ChromiumModule.__init__(
			self,
			name='WindowsChromiumDownload',
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
					[data_type.File, ('target_path', 'total_bytes')],
					[data_type.Link, 'tab_url'],
					[data_type.Time, 'start_time', format.chrome_time],
				],
				db='downloads',
				spe=os.path.split(profile)[1],
			)

		return True
