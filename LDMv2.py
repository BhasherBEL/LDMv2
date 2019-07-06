# coding: utf-8

import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from internal import config
from modules import modlist


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbosity', help='change output verbosity', type=int, choices=[0, 1, 2])
	parser.add_argument('-l', '--logtype', help='change log type', type=int, choices=[0, 1, 2])
	parser.add_argument('-o', '--output', help='change output dir', type=str)
	parser.add_argument('-e', '--execute', nargs='*', help='set modules to execute', choices=[mod.name for mod in modlist.modules])
	args = parser.parse_args()
	if args.verbosity:
		config.VERBOSE_LEVEL = args.verbosity
	if args.logtype:
		config.LOG_TYPE = args.logtype
	if args.output:
		config.LOG_DIR = args.output
	if args.execute:
		for mod in modlist.modules:
			mod.enable = False
			for exec_module in args.execute:
				if mod.name == exec_module:
					mod.enable = True
					break
	modlist.execute()


if __name__ == '__main__':
	main()
