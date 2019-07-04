#!/usr/local/bin/python
# coding: utf-8

from modules.linux.chrome import cookie, history, download

modules = [
		cookie.ChromeCookie,
		history.ChromeHistory,
		download.ChromeDownload,
	]


def execute():
	for module in modules:
		module()
