# coding: utf-8

try:
	import os
	import sqlite3
except ImportError:
	pass

from modules.windows.firefox.firefox_module import FirefoxModule
from internal import data_type


class WindowsFirefoxSavedData(FirefoxModule):
	def __init__(self):
		FirefoxModule.__init__(
			self,
			name='WindowsFirefoxSavedData',
			version='0.1.0',
			file=__file__,
			dependencies=['os', 'sqlite3'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():
			download_path = profile + '/formhistory.sqlite'
			if os.path.isfile(download_path):
				connection = sqlite3.connect(download_path)
				cursor = connection.cursor()

				self.cursor_get_and_log(cursor, 'fieldname, value', 'moz_formhistory', spe=os.path.split(profile)[1])

			self.cursor_getV2(
				path=os.path.join(profile, 'formhistory.sqlite'),
				items=[
					[data_type.Text, 'fieldname'],
					[data_type.Text, 'value'],
				],
				db='moz_formhistory',
				header=['name', 'value'],
				spe=os.path.split(profile)[1],
			)

		return True
