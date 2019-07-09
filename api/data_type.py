try:
	import re
	import phonenumbers
except ImportError:
	pass

from api.api_module import ApiModule


class Email(ApiModule):
	def __init__(self, email):
		ApiModule.__init__(self, dependencies=['re'])
		self.email = email

	@staticmethod
	def find(string):
		return re.findall(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b', string)


class Password(ApiModule):
	def __init__(self, password):
		ApiModule.__init__(self, dependencies=[])
		self.password = password


class Username(ApiModule):
	def __init__(self, username):
		ApiModule.__init__(self, dependencies=[])
		self.username = username


class Name(ApiModule):
	def __init__(self, first_name, last_name=None):
		ApiModule.__init__(self, dependencies=[])
		self.first_name = first_name
		self.last_name = last_name


class Ip(ApiModule):
	def __init__(self, ip):
		ApiModule.__init__(self, dependencies=[])
		self.ip = ip

	@staticmethod
	def find(string):
		return [str(v) for v in ['.'.join(s) for s in re.findall(r'\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b', string)] if bool(v) and all([int(s) <= 255 for s in v.split('.')])]


class PhoneNumber(ApiModule):
	def __init__(self, national_number, country_code):
		ApiModule.__init__(self, dependencies=['re', 'phonenumbers'])
		self.national_number = national_number
		self.country_code = country_code

	@staticmethod
	def find(string):
		return [(match.number.country_code, match.number.national_number) for match in phonenumbers.PhoneNumberMatcher(string, 'EU')]


class CreditCard(ApiModule):
	def __init__(self, number, name=None, expiration=None):
		ApiModule.__init__(self, dependencies=[])
		self.name = name
		self.number = number
		self.expiration = expiration


class Link(ApiModule):
	def __init__(self, link, title=None):
		ApiModule.__init__(self, dependencies=['rer'])
		self.link = link
		self.title = title

	@staticmethod
	def find(string):
		return re.findall(r'\bhttp[s]?://(?:[a-zA-Z]|[0-9]|[$\-/_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\b', string)


class Address(ApiModule):
	def __init__(self, address, zipcode=None, country=None):
		ApiModule.__init__(self, dependencies=[])
		self.address = address
		self.zipcode = zipcode
		self.country = country
