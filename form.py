import json
from helps import *
from mapsEnums import *

# keeps track of how many nameless grids we've had so far
gridCount = 0
# holds all control_names that need to be 
# added in Genify for this form
names2add = []

class Element: # basic attributes common to all elements
	def __init__(self, obj):
		self.displayName = obj["displayName"]
		self.show = obj["show"]
		# everything is section/container/question/formTool
		self.formBlock = formBlockMap[obj["type"]]

		# everything has a control_name
		# so we'll set it here
		global gridCount
		if self.formBlock == FormBlock.grid:
			self.control_name = f"grid_{gridCount}"
			gridCount += 1
		else: 
			self.control_name = to_control_name(obj["Label"])
			print(self.control_name)
			if self.formBlock == FormBlock.field:
				global names2add
				names2add.append(self.control_name)

# this defines a single field
class Field(Element):
	def __init__(self, obj):
		super().__init__(obj)
		self.type = questionTypeMap[obj["QuestionType"]]
		match self.type:
			case FieldType.text:
				self = Text

# sets up a single grid
class Grid(Element):
	def __init__(self, obj):
		super().__init__(obj)
		self.open = obj["open"]
		self.readonly = obj["readonly"]
		self.numColumns = len(obj["columns"])
		self.colWidth = (int) (12 / self.numColumns)
		self.fields = []
		for col in obj["columns"]:
			# stuff is always 1 layer deeper here
			for item in col["items"]:
				self.fields.append(Field(item))

# this should basically set up a section 
# of the form, mainly just the attributes
class Section(Element):
	def __init__(self, obj):
		super().__init__(obj)
		self.readonly = obj["readonly"]
		self.open = obj["open"]
		self.label = obj["Label"]
		self.grids = []
		for grid in obj["contents"]:
			self.grids.append(Grid(grid))


		

class Form:
	def __init__(self):
		self.title = input("Enter the name of the form you want to translate: ")
		self.json = json.load(open("examples/newHire.json"))
		self.sections = []
		for section in self.json:
			self.sections.append(Section(section))

		
