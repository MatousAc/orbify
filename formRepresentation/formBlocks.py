import json
from formRepresentation.fields import *
from helpers.helps import *
from formRepresentation.mapsEnums import *
# holds all control_names that need to be 
# added in Genify for this form
names2add = []

def trackNames(field):
	if field.formBlock == FormBlock.field:
		global names2add
		names2add.append(field.control_name)
		print(field.control_name)

class FieldHolder():
	def __init__(self, grid, item):
		field = None # create an instance of the field
		match questionTypeMap[item["QuestionType"]]:
			case FieldType.text: 			field = Text(item)
			case FieldType.richText:	field = RichText(item)
			case FieldType.numeric:
				if item["format"]["currency"]["useCurrency"]:
																field = Currency(item)
				else: 									field = Numeric(item)
			case FieldType.email: 		field = Email(item)
			case FieldType.date: 			field = Date(item)
			case FieldType.radio: 		
				if isYesNo(item["Choices"]):
																field = YesNo(item)
				else: 									field = Radio(item)
			case FieldType.checkbox: 	field = CheckBox(item)
			case FieldType.dropdown: 	field = DropDown(item)
			case FieldType.fileAttach:field = FileAttach(item)
			case FieldType.secret: 		field = Secret(item)
			case FieldType.signature: field = Signature(item)
			case FieldType.staticText:field = StaticText(item)
			case FieldType.space: 		field = Space(item)
		
		# we keep track of control_names here cause they 
		# could have changed in the constructors above
		trackNames(field)
		self.field = field
		self.h = grid.h
		self.w = grid.w
		self.x = grid.x
		self.y = grid.y
	
	def accept(self, visitor):
		visitor.visitFieldHolder(self)



# sets up a single grid
class Grid(Element):
	def __init__(self, obj):
		super().__init__(obj)
		self.open = obj["open"]
		self.readonly = obj["readonly"]
		# grid measurements
		numDivisions = 12
		self.numColumns = len(obj["columns"])
		self.w = (int) (numDivisions / self.numColumns)
		self.h = 1
		self.x = 1
		self.fields = []
		for col in obj["columns"]:
			self.y = 1
			for item in col["items"]:
				self.fields.append(FieldHolder(self, item))
				self.y += 1 # move one row farther down
			self.x += self.w # move one column farther over
	
	def accept(self, visitor):
		visitor.visitGrid(self)

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
	
	def accept(self, visitor):
		visitor.visitSection(self)


class Form:
	def __init__(self):
		self.title = input("Enter the name of the form you want to translate: ")
		self.control_name = to_control_name(self.title)
		print(self.control_name)
		self.json = json.load(open("examples/newHire.json"))
		self.sections = []
		for section in self.json:
			self.sections.append(Section(section))
	
	def accept(self, visitor):
		visitor.visitForm(self)


