# coding: utf-8

try:
	import subprocess
except ImportError:
	pass

from modules.windows.windows_module import WindowsModule


class WindowsWifi(WindowsModule):
	def __init__(self):
		WindowsModule.__init__(
			self,
			name='WindowsWifi',
			version='0.1.0',
			file=__file__,
			dependencies=['subprocess'],
		)

	def execute(self):
		if not super().execute():
			return False

		data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp1252').split('\n')
		profiles = [i.split(":")[1][1:-1] for i in data if "all user profile" in i.lower() or 'profil tous les utilisateurs' in i.lower()]
		if profiles:
			self.log('SSID,key')
		for i in profiles:
			results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(
				'cp1252').split('\n')
			results = [b.split(":")[1][1:-1] for b in results if "key content" in b.lower() or "contenu de la cl" in b.lower()]
			try:
				self.log(i + ',' + results[0])
			except IndexError:
				self.log(i + ',')

		return True


