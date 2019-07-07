import getpass

from api import platforms
from api.windows import users


def get_username():
    return getpass.getuser()


def get_accessible_users():
    if platforms.current_platform.system == 'Windows':
        return users.get_accessible_users()
    else:
        return [get_username()]
