try:
	import win32net
	import win32netcon
except ImportError:
	pass

try:
	import os
except ImportError:
	pass

from api import requirement


def get_users() -> list:
	if not requirement.are_presents(['win32net', 'win32netcon']):
		if requirement.is_present('os'):
			return [os.getusername()]
		else:
			return []
	filter = win32netcon.FILTER_NORMAL_ACCOUNT
	resume_handle = 0
	user_list = []
	while True:
		result = win32net.NetUserEnum(None, 0, filter, resume_handle)
		user_list += [user['name'] for user in result[0]]
		resume_handle = result[2]
		if not resume_handle:
			break
	user_list.sort()
	return user_list


def get_accessible_users() -> list:
	users = []
	for user in get_users():
		user_path = 'C:\\Users\\' + user
		if os.path.isdir(user_path) and os.access(user_path + '\\AppData', os.R_OK):
			users.append(user)
	return users
