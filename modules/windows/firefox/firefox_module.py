# coding: utf-8

try:
	import os
	import json
	from configparser import RawConfigParser
except ImportError:
	pass

from modules.windows.windows_module import WindowsModule
from api import user


FIREFOX_WINDOWS_NAMES = [
	'Mozilla\\Firefox',
	'NETGATE Technologies\\BlackHawk',
	'8pecxstudios\\Cyberfox',
	'Comodo\\IceDragon',
	'K-Meleon',
	'Mozilla\\icecat',
]
PROFILES = []
PROFILES_CHECK = False


class FirefoxModule(WindowsModule):

	def __init__(self, name, version, file, dependencies):
		WindowsModule.__init__(
			self,
			name=name,
			version=version,
			file=file,
			dependencies=dependencies+['os', 'json'],
		)

	def has(self):
		return super().has() and self.get_profiles()

	def get_firefox_profiles(self, directory):
		"""
		List all profiles
		"""

		profile_list = []
		try:
			cp.read(os.path.join(directory, 'profiles.ini'))
			for section in cp.sections():
				if section.startswith('Profile') and cp.has_option(section, 'Path'):
					profile_path = None

					if cp.has_option(section, 'IsRelative'):
						if cp.get(section, 'IsRelative') == '1':
							profile_path = os.path.join(directory, cp.get(section, 'Path').strip())
						elif cp.get(section, 'IsRelative') == '0':
							profile_path = cp.get(section, 'Path').strip()

					else:  # No "IsRelative" in profiles.ini
						profile_path = os.path.join(directory, cp.get(section, 'Path').strip())

					if profile_path:
						profile_path.replace('/', '\\')
						profile_list.append(profile_path)

		except Exception as e:
			self.error(u'An error occurred while reading profiles.ini: {}'.format(e))

	def get_profiles(self) -> list:
		global PROFILES_CHECK, FIREFOX_WINDOWS_NAMES, PROFILES

		if PROFILES_CHECK:
			return PROFILES
		else:
			PROFILES_CHECK = True
			configs = []
			if os.environ.get('APPDATA'):
				appdatas = os.environ.get('APPDATA').replace(user.get_username(), '{user}')
			else:
				appdatas = 'C:\\Users\\{user}\\AppData\\Roaming'
			for appdata in self.get_users_path_to(appdatas):
				for name in FIREFOX_WINDOWS_NAMES:
					if os.path.isdir(appdata + '\\' + name):
						configs.append(appdata + '\\' + name)

			# https://github.com/AlessandroZ/LaZagne/blob/master/Windows/lazagne/softwares/browsers/mozilla.py#L74
			for config in configs:
				if os.path.isfile(config + '\\profiles.ini'):
					cp = RawConfigParser()
					cp.read(config + '\\profiles.ini')
					for section in cp.sections():
						if section.startswith('Profile') and cp.has_option(section, 'Path'):
							profile_path = None

							if cp.has_option(section, 'IsRelative'):
								if cp.get(section, 'IsRelative') == '1':
									profile_path = os.path.join(config, cp.get(section, 'Path').strip())
								elif cp.get(section, 'IsRelative') == '0':
									profile_path = cp.get(section, 'Path').strip()

							else:  # No "IsRelative" in profiles.ini
								profile_path = os.path.join(config, cp.get(section, 'Path').strip())

							if profile_path:
								profile_path.replace('/', '\\')
								if os.path.isdir(profile_path):
									PROFILES.append(profile_path)
		return PROFILES
