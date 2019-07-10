from internal import data_type

EMAILS = []
PASSWORDS = []
USERNAMES = []
NAMES = []
IPS = []
PHONES_NUMBERS = []
CREDITS_CARDS = []
LINKS = []
ADDRESS = []
TIMES = []
FILES = []
OTHERS = []


def find(obj):
	global EMAILS, IPS, PHONES_NUMBERS, LINKS
	EMAILS += [data_type.Email(e) for e in data_type.Email.find(obj) if e not in EMAILS]
	IPS += [data_type.Ip(e) for e in data_type.Ip.find(obj) if e not in IPS]
	PHONES_NUMBERS += [data_type.PhoneNumber(e[0], e[1]) for e in data_type.PhoneNumber.find(obj) if e not in PHONES_NUMBERS]
	LINKS += [data_type.Link(e) for e in data_type.Link.find(obj) if e not in LINKS]


def print_stat():
	print(len(EMAILS), 'emails found')
	print(len(PASSWORDS), 'passwords found')
	print(len(USERNAMES), 'usernames found')
	print(len(NAMES), 'names found')
	print(len(IPS), 'ips found')
	print(len(PHONES_NUMBERS), 'phones numbers found')
	print(len(CREDITS_CARDS), 'credits cards found')
	print(len(LINKS), 'links found')
	print(len(ADDRESS), 'addresses found')
	print(len(TIMES), 'dates found')
	print(len(FILES), 'files found')
	print(len(OTHERS), 'unknown data found')
