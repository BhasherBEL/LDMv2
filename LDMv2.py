# coding: utf-8

import argparse

from modules import modlist
from internal import config


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbosity', help='change output verbosity', type=int, choices=[0, 1, 2])
	parser.add_argument('-l', '--logtype', help='change log type', type=int, choices=[0, 1, 2])
	parser.add_argument('-o', '--output', help='change output dir', type=str)
	args = parser.parse_args()
	if args.verbosity:
		config.VERBOSE_LEVEL = args.verbosity
	if args.logtype:
		config.LOG_TYPE = args.logtype
	if args.output:
		config.LOG_DIR = args.output
	modlist.execute()


if __name__ == '__main__':
	main()
