#!/usr/local/bin/python
# coding: utf-8

from internal.module import Module


class LinuxModule(Module):

	def __init__(self, name, version, file, dependencies):
		Module.__init__(
			self,
			name=name,
			version=version,
			file=file,
			dependencies=dependencies,
		)

	def can(self):
		return super().can() and self.platform.system.lower() == 'linux'

	def has(self):
		return super().has()

	def execute(self):
		return super().execute()
