# coding: utf-8

# Source: https://github.com/easybuilders/easybuild/wiki/OS_flavor_name_version

import platform


class Platform:
	def __init__(self):
		if platform.system() and platform.dist() and platform.machine():
			self.system = platform.system()

			if self.system == 'SunOS':
				self.dist_name, __, self.dist_version, __, self.dist_version_name, __ = platform.uname()
			elif self.system == 'Darwin':
				self.dist_name = 'unknown'
				self.dist_version = platform.mac_ver()[0]
				self.dist_version_name = 'unknown'
			elif self.system == 'Windows':
				self.dist_version = platform.uname()[2]
			else:
				self.dist_name = platform.dist()[0]
				self.dist_version = platform.dist()[1]

				if self.dist_name == 'SuSE':
					self.dist_version_name = platform.uname()[1]
				else:
					self.dist_version_name = platform.dist()[2]

			if '64' in platform.machine():
				self.machine = 'x64'
			elif '86' in platform.machine():
				self.machine = 'x32'
			else:
				self.machine = 'unknown'
