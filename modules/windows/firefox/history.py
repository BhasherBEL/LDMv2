try:
	import sqlite3
	import os
except ImportError:
	pass

from modules.windows.firefox.firefox_module import FirefoxModule


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
			history_path = os.path.join(profile, 'places.sqlite')
			if os.path.isfile(history_path):
				self.log(os.path.split(profile)[1] + ':')
				connection = sqlite3.connect(history_path)
				cursor = connection.cursor()

				try:
					cursor.execute('select last_visit_date, url, title from moz_historyvisits natural join moz_places')
				except sqlite3.OperationalError:
					self.executenot(history_path + ' database is locked', 1)
					return False

				self.standard_multiple_log(cursor.fetchall(), header='last_visit_time,url,title')
		return True

