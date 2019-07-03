#!/usr/local/bin/python
# coding: utf-8

from modules.linux.chrome import cookie

modules = [
		cookie.ChromeCookie,
	]


def execute():
	for module in modules:
		module()
