try:
	import re
	import phonenumbers
	import datetime
except ImportError:
	pass

from api.api_module import ApiModule
from internal import sorted_data


class Email(ApiModule):
	def __init__(self, email):
		ApiModule.__init__(self, dependencies=['re'])
		self.email = email
		sorted_data.EMAILS.append(self)

	@staticmethod
	def find(string):
		return re.findall(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b', string)

	def __str__(self):
		return str(self.email)


class Password(ApiModule):
	def __init__(self, password):
		ApiModule.__init__(self, dependencies=[])
		self.password = password
		sorted_data.PASSWORDS.append(self)

	def __str__(self):
		return str(self.password)


class Username(ApiModule):
	def __init__(self, username):
		ApiModule.__init__(self, dependencies=[])
		self.username = username
		sorted_data.USERNAMES.append(self)

	def __str__(self):
		return str(self.username)


class Name(ApiModule):
	def __init__(self, first_name, last_name=None):
		ApiModule.__init__(self, dependencies=[])
		self.first_name = first_name
		self.last_name = last_name
		sorted_data.NAMES.append(self)

	def __str__(self):
		return str(self.first_name) + (',' + self.last_name if self.last_name else '')


class Ip(ApiModule):
	def __init__(self, ip):
		ApiModule.__init__(self, dependencies=[])
		self.ip = ip
		sorted_data.IPS.append(self)

	@staticmethod
	def find(string):
		return [str(v) for v in ['.'.join(s) for s in re.findall(r'\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b', string)] if bool(v) and all([int(s) <= 255 for s in v.split('.')])]

	def __str__(self):
		return str(self.ip)


class PhoneNumber(ApiModule):
	def __init__(self, phone_number):
		ApiModule.__init__(self, dependencies=['re', 'phonenumbers'])
		self.phone_number = phone_number
		sorted_data.PHONES_NUMBERS.append(self)

	@staticmethod
	def find(string):
		return [(match.number.country_code, match.number.national_number) for match in phonenumbers.PhoneNumberMatcher(string, 'EU')]

	def __str__(self):
		return str(self.phone_number)


class CreditCard(ApiModule):
	def __init__(self, number, name=None, expiration=None):
		ApiModule.__init__(self, dependencies=[])
		self.name = name
		self.number = number
		self.expiration = expiration
		sorted_data.CREDITS_CARDS.append(self)

	def __str__(self):
		return str(self.number) + (',' + self.name if self.name else '') + (',' + self.expiration if self.expiration else '')


class Link(ApiModule):
	def __init__(self, link, title=None):
		ApiModule.__init__(self, dependencies=['rer'])
		self.link = link
		self.title = title
		sorted_data.LINKS.append(self)

	@staticmethod
	def find(string):
		return re.findall(r'\bhttp[s]?://(?:[a-zA-Z]|[0-9]|[$\-/_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\b', string)

	def __str__(self):
		return str(self.link) + (',' + str(self.title) if str(self.title) else '')


class Address(ApiModule):
	def __init__(self, address, zipcode=None, country=None):
		ApiModule.__init__(self, dependencies=[])
		self.address = address
		self.zipcode = zipcode
		self.country = country
		sorted_data.ADDRESS.append(self)

	def __str__(self):
		return str(self.address) + (',' + str(self.zipcode) if self.zipcode else '') + (',' + str(self.country) if self.country else '')


class Time(ApiModule):
	def __init__(self, timestamp):
		ApiModule.__init__(self, dependencies=['datetime'])
		self.timestamp = timestamp
		self.date = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp)
		sorted_data.TIMES.append(self)

	def __str__(self):
		return str(self.date)


class File(ApiModule):
	def __init__(self, url, size=None):
		ApiModule.__init__(self, dependencies=[])
		self.url = url
		self.size = size
		sorted_data.FILES.append(self)

	def __str__(self):
		return str(self.url) + (',' + self._strsize() if self.size else '')

	def _strsize(self) -> str:
		size = self.size
		for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
			if abs(size) < 1024.0:
				return "%3.1f%s" % (size, unit)
			size /= 1024.0
		return "%.1f%s" % (size, 'YiB')


class Text(ApiModule):
	def __init__(self, content):
		ApiModule.__init__(self, dependencies=[])
		self.content = str(content)

	def __str__(self):
		return self.content
