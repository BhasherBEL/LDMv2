from api import requirement


class ApiModule:
	def __init__(self, dependencies: list):
		self.dependencies = dependencies
		self.enabled = True
		if not requirement.are_presents(dependencies):
			self.enabled = False

	def __str__(self):
		return str({key: self.__dict__[key] for key in self.__dict__ if key not in ['dependencies', 'enable']})

	def __repr__(self):
		return self.__str__()
