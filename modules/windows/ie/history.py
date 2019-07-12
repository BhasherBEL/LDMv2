# coding: utf-8

try:
	import winreg
except ImportError:
	pass

from modules.windows.windows_module import WindowsModule
from internal import data_type


class WindowsIEHistory(WindowsModule):
	def __init__(self):
		WindowsModule.__init__(
			self,
			name='WindowsIEHistory',
			version='0.0.1',
			file=__file__,
			dependencies=['winreg'],
		)

	def execute(self) -> bool:
		if not super().execute():
			return False

		with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Internet Explorer\\TypedURLs') as hkey:
			key_data = winreg.QueryInfoKey(hkey)
			urls = [[data_type.Link(winreg.EnumValue(hkey, x)[1])] for x in range(0, key_data[1])]
			self.logV2(urls, header=['url'])

		return True
