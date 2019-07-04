# coding: utf-8

import sys
import importlib
import os
import time

from internal import platforms, config

CURRENT_TIME = time.strftime('%Y%m%d-%H%M%S')


class Module:
	platform = platforms.Platform()
	PYTHON_VERSION = [sys.version_info.major, sys.version_info.minor, sys.version_info.micro]

	def __init__(self, name: str, version: str, file: str, dependencies: list = None):

		print('-------------------- ' + name + ' ' + version + ' --------------------')
		self.version = version
		self.name = name
		self.dependencies = dependencies
		self.file = file
		self.logfile = os.path.abspath(file).replace(
			os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
			os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + config.LOG_DIR + '/' + CURRENT_TIME,
		).replace('.py', '.txt')
		if self.can():
			dep_error = False
			if dependencies:
				for el in dependencies:
					try:
						importlib.import_module(el)
					except ImportError as e:
						print(e)
						dep_error = True
						self.dependenciesnot(el)
			if not dep_error:
				if self.has():
					if not self.execute():
						self.executenot()
				else:
					self.hasnot()

		else:
			self.cannot()

		if config.LOG_TYPE == 1:
			print('done')
		print('-'*(43+len(name)+len(version)))

	def can(self) -> bool:
		"""
			The "can" function checks whether the module can be called. It is based on the OS, the python version, and other generic data.
			:return boolean depend on module can be called.
		"""
		return self.PYTHON_VERSION[0] == 3

	def has(self) -> bool:
		"""
			The "has" function checks whether the data required for the module is present. For example, it will check the existence of the program or file concerned.
			:return boolean depend on data required is present.
		"""
		return True

	def execute(self) -> bool:
		"""
			The "execute" function contains the core of the module. She will execute the module.
			:return boolean depend on success
		"""
		return True

	def cannot(self):
		self.log('Cannot load ' + self.name + ' module.', 2)

	def hasnot(self):
		self.log('Cannot execute ' + self.name + ' module.', 2)

	def dependenciesnot(self, name):
		self.log('Cannot execute ' + self.name + ' module. \'' + name + '\' cannot be imported.', 1)

	def executenot(self, text=None, verbose=1):
		if text:
			self.log(text, verbose=verbose)
		else:
			self.log('Module ' + self.name + ' could not be correctly executed.', verbose=verbose)

	def log(self, text, verbose=1):
		if verbose <= config.VERBOSE_LEVEL:
			if config.LOG_TYPE == 0 or config.LOG_TYPE == 2:
				print(text)
			if config.LOG_TYPE == 1 or config.LOG_TYPE == 2:
				if not os.path.isdir(os.path.dirname(self.logfile)):
					os.makedirs(os.path.dirname(self.logfile))

				with open(self.logfile, 'a') as file:
					file.write(text + '\n')
