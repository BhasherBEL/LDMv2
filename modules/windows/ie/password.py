# coding: utf-8

try:
	import winreg
	import hashlib
	import win32crypt
except ImportError:
	pass

from modules.windows.windows_module import WindowsModule
from internal import sorted_data


class WindowsIEPassword(WindowsModule):
	def __init__(self):
		WindowsModule.__init__(
			self,
			name='WindowsIEPassword',
			version='0.0.1',
			file=__file__,
			dependencies=['winreg', 'hashlib', 'win32crypt'],
		)
		self.hashed_links = []
		self.enable = False

	def execute(self) -> bool:
		if not super().execute():
			return False

		with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Internet Explorer\\IntelliForms\\Storage2') as hkey:
			key_data = winreg.QueryInfoKey(hkey)

			passwords = []

			for i in range(key_data[1]):
				password_data = winreg.EnumValue(hkey, i)
				if password_data:
					for history in self.hashed_history():
						#print(history[1], password_data[0][:40].lower(), history[2])
						if history[1] == password_data[0][:40].lower():
							passwords.append(self.decrypt(password_data[1], history[0]))
							break

			print(passwords)

		return True

	def hashed_history(self):
		if self.hashed_links:
			return self.hashed_links

		for link in sorted_data.LINKS:
			try:
				link_val = (link.link + '\0').encode('UTF-16LE')
				self.hashed_links.append([link_val, hashlib.sha1(link_val).hexdigest().lower(), link.link])
			except Exception:
				print(link.link + ' can\'t be hashed')

		return self.hashed_links

	def decrypt(self, password_data, history):
			pass