import json
from helps import *
from maps import *

gridCount = 0

class Element: # basic attributes common to all elements
	def __init__(self, obj):
		self.displayName = obj["displayName"]
		self.show = obj["show"]
		# section/container/question
		self.level = obj["type"].replace("_Type", "").lower
		# everything has a control_name
		# so we'll set it here
		if self.type == "Container_Type":
			self.control_name = f"grid_{gridCount}"
			gridCount += 1
		else: 
			self.control_name = snake_case(obj["Label"])

# this defines a single field
class Field(Element):
	def __init__(self, obj):
		super().__init__(obj)
		self.type = questionTypeMap[obj["QuestionType"]]


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
			for item in col:
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
		self.title = input("Enter the name of the form you want to generate: ")
		self.json = json.load(open("examples/newHire.json"))
		self.sections = []
		for section in self.json:
			self.sections.append(Section(section))

		
