
from element import Element
from helps import *
from mapsEnums import FieldType

# all these classes define a single field
# most are all slightly different
class Text(Element):
	def __init__(self, item):
		super().__init__(item)
class RichText(Element):
	def __init__(self, item):
		super().__init__(item)
		self.tinymceOptions = item["tinymceOptions"]
class Numeric(Element):
	def __init__(self, item):
		super().__init__(item)
		self.precision = item["format"]["digitsAfterDecimal"]
class Currency(Element):
	def __init__(self, item):
		super().__init__(item)
		self.fieldType = FieldType.currency
		self.precision = item["format"]["digitsAfterDecimal"]
		# decide which type of currency we have
		self.prefix = '$'
		match item["format"]["currency"]["id"]:
			case "en-us": self.prefix = '$'
			case "en-gb": self.prefix = '£'
			case "de-de": self.prefix = '€'
			case "fr-fr": self.prefix = '€'
class Email(Element):
	def __init__(self, item):
		super().__init__(item)
class Date(Element):
	def __init__(self, item):
		super().__init__(item)
class Radio(Element):
	def __init__(self, item):
		super().__init__(item)
		# here I create a dictionary from
		# a list of dictionaries 
		self.choices = choiceDict(item["Choices"])
class YesNo(Element):
	def __init__(self, item):
		super().__init__(item)
		self.fieldType = FieldType.yesno
		# change control_name to is_control_name
		self.control_name = f"is_{self.control_name}"
class CheckBox(Element):
	def __init__(self, item):
		super().__init__(item)
		self.choices = choiceDict(item["Choices"])
class DropDown(Element):
	def __init__(self, item):
		super().__init__(item)
		self.choices = choiceDict(item["Choices"])
		self.multipleSelect = item["multiple"]
class FileAttach(Element):
	def __init__(self, item):
		super().__init__(item)
class Secret(Element):
	def __init__(self, item):
		super().__init__(item)
		self.confirm = item["ConfirmPassword"]
class Signature(Element):
	def __init__(self, item):
		super().__init__(item)
class StaticText(Element):
	def __init__(self, item):
		super().__init__(item)
		self.text = item["formtext"]
class Space(Element):
	def __init__(self, item):
		super().__init__(item)
