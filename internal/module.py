# coding: utf-8

import sys
import os
import time
import math

try:
	import win32crypt
except ImportError:
	pass
try:
	import sqlite3
except ImportError:
	pass

from internal import config, sorted_data
from api import platforms, requirement, csv_to_html

CURRENT_TIME = time.strftime('%Y%m%d-%H%M%S')


class EmptyException(Exception):
	pass


class Module:
	platform = platforms.Platform()
	PYTHON_VERSION = [sys.version_info.major, sys.version_info.minor, sys.version_info.micro]
	enable = True

	def __init__(self, name: str, version: str, file: str, dependencies: list = None):
		self.version = version
		self.name = name
		self.dependencies = dependencies
		self.file = file
		self.logfile = os.path.abspath(file).replace(
			os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
			os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + config.LOG_DIR + '/' + CURRENT_TIME,
		).replace('.py', '')
		self.logs = {}

	def init(self):
		if self.enable:
			can = self.can()
			if can or config.VERBOSE_LEVEL == 2:
				self.log(('-'*(int(math.floor((60-len(self.name)-len(self.version))/2)))
							 + ' ' +
							self.name
							+ ' ' +
							self.version
							 + ' '
							+ '-'*(int(math.ceil((60-len(self.name)-len(self.version))/2)))
						  ), 1, write=False, forceprint=True)
			if can:
				dep_error = False
				if self.dependencies:
					if not requirement.are_presents(self.dependencies):
						dep_error = True
						self.dependenciesnot(self.dependencies)
				if not dep_error:
					if self.has():
						try:
							if not self.execute():
								self.executenot()
							else:
								if config.VERBOSE_LEVEL == 0:
									print(self.name) + ' executed'
								self.write(config.HTML)
						except (EmptyException if config.DEBUG else Exception) as e:
							self.log(type(e).__name__ + ': ' + str(e), verbose=1)
					else:
						self.hasnot()

			else:
				self.cannot()

			if can or config.VERBOSE_LEVEL == 2:
				self.log('-' * 63, write=False, forceprint=True)

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

	def cannot(self, write=False):
		self.log('Cannot load ' + self.name + ' module.', 2, write=write, forceprint=not write)

	def hasnot(self, write=False):
		self.log('Cannot execute ' + self.name + ' module.', 2, write=write, forceprint=not write)

	def dependenciesnot(self, name, write=False):
		self.log('Cannot execute ' + self.name + ' module. \'' + ', '.join(name) + '\' cannot be imported.', 1, write=write, forceprint=not write)

	def executenot(self, text=None, verbose=1, write=False):
		if text:
			self.log(text, verbose=verbose, write=write, forceprint=not write)
		else:
			self.log('Module ' + self.name + ' could not be correctly executed.', verbose=verbose, write=write, forceprint=not write)

	def cursor_getV2(self, path, items, db, request_sup='', header=None, *args, **kwargs):
		if os.path.isfile(path):
			connection = sqlite3.connect(path)
			cursor = connection.cursor()
			elements = ','.join([item[1] if type(item[1]) == str else ','.join(item[1]) for item in items])

			try:
				cursor.execute(
					'SELECT ' + elements + ' FROM ' + db + ' ' + request_sup)
			except (EmptyException if config.DEBUG else sqlite3.OperationalError):
				self.executenot(db + ' database is locked', 1)
				return False

			output = cursor.fetchall()
			sorted_output = self.sort_output(output, items)

			if not header:
				header = elements
			self.logV2(sorted_output, header, *args, **kwargs)

	def sort_output(self, output, items):
		sorted_output = []

		for out in output:
			res = []
			for i in range(0, len(out)):
				value = out[i]
				ii = 0
				vi = 0
				for item in items:
					vi += len(item[1]) if isinstance(item[1], list) or isinstance(item[1], tuple) else 1
					if i < vi:
						break
					ii += 1
				if len(items[ii]) == 3 or (len(items[ii]) == 4 and vi-len(items[ii][1]) in items[ii][3]):
					value = items[ii][2](value)
				res.append(value)
			sorted_res = []
			i = 0
			for item in items:
				if not isinstance(item[1], list) and not isinstance(item[1], tuple):
					item[1] = [item[1]]
				sorted_res.append(item[0](*res[i:i + len(item[1])]))
				i += len(item[1])
			sorted_output.append(sorted_res)
		return sorted_output

	def logV2(self, sorteds, header=None, verbose=1, spe=None, write=True, forceprint=False):
		"""
		Log text in a file or in the console
		:param sorteds: Table of table of sorted_value (basically generate by sort_output)
		:param header: header of log data
		:param verbose: The verbosity of the log data
		:param spe: The additional value in file name
		:param write: Define if data want to be write (force)
		:param forceprint: Define if the data want to be print although the internal.config.LOG_TYPE (force)
		:return: Nothing
		"""
		if verbose >= config.VERBOSE_LEVEL:
			if config.LOG_TYPE == 0 or config.LOG_TYPE == 2 or forceprint:
				if header:
					print(','.join(header) if isinstance(header, list) or isinstance(header, tuple) else str(header))
				print('\n'.join([','.join([str(ssub) for ssub in sub]) for sub in sorteds]))
			if (config.LOG_TYPE == 1 or config.LOG_TYPE == 2) and write:
				filepath:str = self.logfile + ('.' + spe if spe else '')
				if not filepath.endswith('.csv'):
					filepath += '.csv'
				if filepath not in self.logs:
					self.logs[filepath] = ''
				if header:
					self.logs[filepath] += (','.join(header) if isinstance(header, list) or isinstance(header, tuple) else str(header)) + '\n'
				self.logs[filepath] += '\n'.join([','.join([str(ssub) for ssub in sub]) for sub in sorteds]) + '\n'

	def cursor_get_and_log(self, cursor, elements, db_name, decrypt_ids=None, decrypt_algo=None, **other):
		try:
			cursor.execute(
				'SELECT ' + elements + ' FROM ' + db_name)
		except (EmptyException if config.DEBUG else sqlite3.OperationalError):
			self.executenot(db_name + ' database is locked', 1)
			return False

		self.standard_multiple_log(cursor.fetchall(), header=elements, decrypt_ids=decrypt_ids, decrypt_algo=decrypt_algo, **other)

	def standard_multiple_log(self, content, header=None, decrypt_ids=None, decrypt_algo=None, **other):
		if header and (content or config.VERBOSE_LEVEL == 2):
			self.log(header, **other)
		if not decrypt_algo and platforms.current_platform.system == 'Windows':
			decrypt_algo = lambda x: win32crypt.CryptUnprotectData(x, None, None, None, 0)[1].decode('utf-8')
		for el in content:
			res = ''
			for i in range(len(el)):
				if decrypt_ids and i in decrypt_ids:
					res += ',' + decrypt_algo(el[i])
				else:
					res += ',' + str(el[i])
			self.log(res[1:], **other)

	def log(self, text, verbose=1, spe=None, write=True, forceprint=False, sorted_value=None, end=True):
		"""
		Log text in a file or in the console
		:param text: The text to print or write
		:param verbose: The verbosity of the log data
		:param spe: The additional value in file name
		:param write: Define if data want to be write
		:param forceprint: Define if the data want to be print although the internal.config.LOG_TYPE.
		:param sorted_value: Define value with type
		:param end: Define if the data close the line
		:return: Nothing
		"""
		if verbose >= config.VERBOSE_LEVEL:
			if config.LOG_TYPE == 0 or config.LOG_TYPE == 2 or forceprint:
				print(str(text))
			if (config.LOG_TYPE == 1 or config.LOG_TYPE == 2) and write:
				filepath = self.logfile + ('.' + spe if spe else '') + '.csv'
				if filepath in self.logs:
					self.logs[filepath] += str(text) + ('\n' if end else '')
				else:
					self.logs[filepath] = str(text) + ('\n' if end else '')

	def write(self, html=False):
		if self.logs and not os.path.isdir(os.path.dirname(self.logfile)):
			os.makedirs(os.path.dirname(self.logfile))
		for key, value in self.logs.items():
			with open(key, 'a', encoding='utf-8') as file:
				file.write(value)
			if html:
				csv_to_html.convert(key)
