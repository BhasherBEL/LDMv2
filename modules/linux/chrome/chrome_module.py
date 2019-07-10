#!/usr/local/bin/python
# coding: utf-8

try:
	import os
	import json
except ImportError:
	pass

from modules.linux.linux_module import LinuxModule


CHROME_LINUX_NAMES = ['google-chromium', 'google-chromium-beta', 'google-chromium-unstable', 'chromium']
PROFILES = []
PROFILES_CHECK = False


class ChromeModule(LinuxModule):

	def __init__(self, name, version, file, dependencies):
		LinuxModule.__init__(
			self,
			name=name,
			version=version,
			file=file,
			dependencies=dependencies+['os', 'json'] if dependencies else ['os', 'json'],
		)

	def can(self):
		return super().can()

	def has(self):
		return super().has() and self.get_profiles()

	def execute(self) -> bool:
		return super().execute()

	def get_profiles(self) -> list:
		global PROFILES_CHECK, CHROME_LINUX_NAMES, PROFILES

		if PROFILES_CHECK:
			return PROFILES
		else:
			PROFILES_CHECK = True
			configs = []
			for name in CHROME_LINUX_NAMES:
				if os.environ.get('XDG_CONFIG_HOME') is not None and os.path.isdir(os.environ.get('XDG_CONFIG_HOME') + '/' + name):
					configs.append(os.environ.get('XDG_CONFIG_HOME') + '/' + name)

				elif os.environ.get('CHROME_CONFIG_HOME') is not None and os.path.isdir(os.environ.get('CHROME_CONFIG_HOME') + '/' + name):
					configs.append(os.environ.get('CHROME_CONFIG_HOME') + '/' + name)

				elif os.path.isdir(os.environ.get('HOME') + '/.config/' + name):
					configs.append(os.environ.get('HOME') + '/.config/' + name)

				elif os.path.isdir('~/.config/' + name):
					configs.append('~/.config/' + name)

			for config in configs:
				profiles_name = []
				if os.path.isfile(config + '/Local State'):
					with open(config + '/Local State') as file:
						local_state_json = json.load(file)

					if local_state_json and 'profile' in local_state_json and 'info_cache' in local_state_json['profile']:
							profiles_name += local_state_json['profile']['info_cache'].keys()
				else:
					profiles_name.append('Default')

				for name in profiles_name:
					path = config + '/' + name
					if os.path.isdir(path):
						PROFILES.append(path)
		return PROFILES
