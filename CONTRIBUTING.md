__LDMv2 Contributig__
==
:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to LDMv2 project on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

### Styleguides

If you are writing new code in a programming language, please follow the writing rules of the language.

In Python, [PEP8](https://www.python.org/dev/peps/pep-0008/) details the writing rules.

### Comments and docstrings

If your code is hard to understand and you can't simplify it, it's better to explain through comments how it works, in order to simplify the reading of the code by others.

It is also best to add docstrings to your functions and classes to explain what they do. Be careful, docstrings also follow writing rules (see above). In addition, they should not explain how the code works, but what it does, and as precisely as possible, to make it easier to read again.

### New module

If you are writing one or more modules, classify them in folders according to the software they are intended for. Keep in mind that the same folder structure is used to generate output files. Any module must inherit directly or indirectly from `internal.module` and be called in the file `modules.modlist`, otherwise it will not work. 

Many general functions are written in existing meta-classes. If you design several modules for the same target, do not hesitate to write a meta-module grouping the common points between the different modules. 

Don't forget to specify the dependencies you use in the place provided for. Note that not everyone has all the dependencies, so you have to import them via the following system:
```python
try:
  import your_import
except ImportError:
  pass
```

A module, whatever it is, must follow this structure:

```python
class ModuleName(MetaModule):
	def __init__(self):
		MetaModule.__init__(
			self,
			name='ModuleName',
			version='0.0.1',
			file=__file__,
			dependencies=['depencence'],
		)
```

For the version, the first number is the number of "big version". Normally it only increments when the logic is completely redesigned. The second number is the number of the version, incremented when a new feature is added. Finally, the last number is the under version. Each time a change is made, it increments. Whether it is a bug fix, a new writing,...

Each module inherits three functions from internal.module:
- `can`

This function is executed before importing the modules, and returns a boolean if the modules should be imported or not. For example, he will check the OS. It returns a successful boolean.

- `has`

This function is performed after the modules have been loaded. It will check that the module must be loaded, but taking into account the imports. For example, it will check the existing of the necessary files. It returns a successful boolean.

- `execute`

This function is the logical core of the module. It is she who will look for the information in the files, in the databases, and will send all this to be logged. It returns a successful boolean.

If one of its functions is not used in a module or meta-module, then it should not be specified. But if it is used, it is first necessary to check if the higher levels have returned a "success". By exemple for the `can` function:

```python
def can(self) -> bool:
  if not super().can():
    return False
```

__Changelog__
--

__LDMv2 2.1 : Windows update__
  - Cookies, passwords, history, downloads and saved data for Chromium Windows
  - Cookies, history, downloads and saved data for Firefox
  - New log system
  - New README file with markdown
  - New Contributing file with markdown

__LDMv2 2.0 : Initial update__
  - Cookies, passwords, history and downloads for Chrome Linux
  - Module system
  - Log system with console and files
  - Readme
