import importlib
from importlib import util


def is_present(module_name: str) -> bool:
	return util.find_spec(module_name) is not None


def are_presents(module_names: list) -> bool:
	return all([util.find_spec(module_name) for module_name in module_names])
