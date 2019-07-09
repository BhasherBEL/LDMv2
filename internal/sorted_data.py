from api import data_type

EMAILS = []
PASSWORDS = []
USERNAMES = []
NAMES = []
IPS = []
PHONES_NUMBERS = []
CREDITS_CARDS = []
LINKS = []
ADDRESS = []
TOTAL = 0


def add(object):
	global EMAILS, PASSWORDS, USERNAMES, IPS, NAMES, PHONES_NUMBERS, CREDITS_CARDS, LINKS, ADDRESS, TOTAL
	TOTAL += 1
	if type(object) == data_type.Email:
		if object not in EMAILS:
			EMAILS.append(object)
	elif type(object) == data_type.Password:
		if object not in PASSWORDS:
			PASSWORDS.append(object)
	elif type(object) == data_type.Username:
		if object not in USERNAMES:
			USERNAMES.append(object)
	elif type(object) == data_type.Name:
		if object not in NAMES:
			NAMES.append(object)
	elif type(object) == data_type.Ip:
		if object not in IPS:
			IPS.append(object)
	elif type(object) == data_type.PhoneNumber:
		if object not in PHONES_NUMBERS:
			PHONES_NUMBERS.append(object)
	elif type(object) == data_type.CreditCard:
		if object not in CREDITS_CARDS:
			CREDITS_CARDS.append(object)
	elif type(object) == data_type.Link:
		if object not in LINKS:
			LINKS.append(object)
	elif type(object) == data_type.Address:
		if object not in ADDRESS:
			ADDRESS.append(object)
	elif type(object) == str:
		EMAILS += [data_type.Email(e) for e in data_type.Email.find(object) if e not in EMAILS]
		IPS += [data_type.Ip(e) for e in data_type.Ip.find(object) if e not in IPS]
		PHONES_NUMBERS += [data_type.PhoneNumber(e[0], e[1]) for e in data_type.PhoneNumber.find(object) if e not in PHONES_NUMBERS]
		LINKS += [data_type.Link(e) for e in data_type.Link.find(object) if e not in LINKS]


def print_stat():
	print(TOTAL, 'data found')
	print(len(EMAILS), 'emails found')
	print(len(PASSWORDS), 'passwords found')
	print(len(USERNAMES), 'usernames found')
	print(len(NAMES), 'names found')
	print(len(IPS), 'ips found')
	print(len(PHONES_NUMBERS), 'phones numbers found')
	print(len(CREDITS_CARDS), 'credits cards found')
	print(len(LINKS), 'links found')
	print(len(ADDRESS), 'addresses found')
