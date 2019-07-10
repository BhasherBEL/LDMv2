try:
	import sqlite3
	import os
except ImportError:
	pass

from modules.windows.firefox.firefox_module import FirefoxModule
from internal import data_type
from api.windows import format


class WindowsFirefoxHistory(FirefoxModule):
	def __init__(self):
		FirefoxModule.__init__(
			self,
			name='WindowsFirefoxHistory',
			version='0.1.0',
			file=__file__,
			dependencies=['sqlite3', 'os'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():

			self.cursor_getV2(
				path=os.path.join(profile, 'places.sqlite'),
				items=[
					[data_type.Link, ('url', 'title')],
					[data_type.Time, 'last_visit_date', format.firefox_time],
				],
				db='moz_historyvisits',
				request_sup='natural join moz_places',
				spe=os.path.split(profile)[1],
			)

		return True

