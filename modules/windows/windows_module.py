#!/usr/local/bin/python
# coding: utf-8

from internal.module import Module
from api.windows import users


class WindowsModule(Module):

	def __init__(self, name, version, file, dependencies):
		Module.__init__(
			self,
			name=name,
			version=version,
			file=file,
			dependencies=dependencies + ['win32net', 'win32netcon'],
		)

	def can(self):
		return super().can() and self.platform.system.lower() == 'windows'

	def get_users(self):
		return users.get_accessible_users()

	def get_users_path(self) -> list:
		return ['C:\\Users\\' + user for user in self.get_users()]

	def get_users_path_to(self, path: str) -> list:
		return [path.replace('{user}', user) for user in self.get_users()]
