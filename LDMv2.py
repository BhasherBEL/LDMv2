# coding: utf-8

import argparse
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from internal import config
from modules import modlist
from api import platforms, user

user_data = {
	'username': user.get_username(),
	'platform': platforms.Platform(),
	'other_users': [otuser for otuser in user.get_accessible_users() if otuser != user.get_username()],
}


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbosity', help='change output verbosity', type=int, choices=[0, 1, 2])
	parser.add_argument('-l', '--logtype', help='change log type', type=int, choices=[0, 1, 2])
	parser.add_argument('-o', '--output', help='change output dir', type=str)
	parser.add_argument('-e', '--execute', nargs='*', help='set modules to execute')
	args = parser.parse_args()
	if args.verbosity:
		config.VERBOSE_LEVEL = args.verbosity
	if args.logtype:
		config.LOG_TYPE = args.logtype
	if args.output:
		config.LOG_DIR = args.output
	if args.execute:
		for mod in modlist.modules:
			if mod.enable:
				mod.enable = False
				for exec_module in args.execute:
					if exec_module in mod.name:
						mod.enable = True
						break


def print_logo():
	print('#########################################')
	print('#                 LDMv2                 #')
	print('#               by Bhasher              #')
	print('#########################################')
	print(' ')
	print(
		'User:',
		user_data['username'].capitalize()
	)
	print(
		'Os:',
		user_data['platform'].system,
		user_data['platform'].dist_name,
		user_data['platform'].dist_version,
		user_data['platform'].machine
	)
	print(
		'Other users:',
		', '.join(user_data['other_users']) if len(user_data['other_users']) > 0 else 'None'
	)
	print(
		str(len([True for module in modlist.modules if module.enable])) + '/' + str(len(modlist.modules)),
		'modules loaded')
	print(' ')


if __name__ == '__main__':
	st = time.time()
	main()
	print_logo()
	modlist.execute()
	print(' ')
	print('Total execution time:', str(round(time.time()-st, 2)) + 's')
