from api import requirement


class ApiModule:
	def __init__(self, dependencies: list):
		self.dependencies = dependencies
		self.enable = True
		if not requirement.are_presents(dependencies):
			self.enable = False

	def __repr__(self):
		return str({key: self.__dict__[key] for key in self.__dict__ if key not in ['dependencies', 'enable']})
