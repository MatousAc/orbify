import json
from pickle import FALSE
import pyperclip
from formRepr.fields import *
from helpers.helps import *
from formRepr.mapsEnums import *
# holds all control_names that need to be 
# added in Genify for this form
names2add = []

def trackNames(field):
	if field.formBlock == FormBlock.field:
		global names2add
		names2add.append(field.control_name)

class Place():
	def __init__(self, grid, item):
		field = None # create an instance of the field
		match questionTypeMap[item["QuestionType"]]:
			case FieldType.text:
				if isPhone(item):				field = Phone(item)
				else:										field = Text(item)
			case FieldType.richText:	field = RichText(item)
			case FieldType.numeric:
				if item["format"]["currency"]["useCurrency"]:
																field = Currency(item)
				else: 									field = Numeric(item)
			case FieldType.email: 		field = Email(item)
			case FieldType.link: 			field = Link(item)
			case FieldType.contact:		field = Contact(item)
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
			case FieldType.ftdImage: 		
				# unless its the logo, images become space
				if isFTDImage(item):		field = FTDImage(item)
				else: 									field = Space(item)
			case FieldType.staticText:field = StaticText(item)
			case FieldType.line:			field = Line(item)
			case FieldType.space: 		field = Space(item)
		
		# we keep track of control_names here cause they 
		# could have changed in the constructors above
		trackNames(field)
		self.field = field
		self.h = grid.h
		self.w = grid.w
		if field.fieldType == FieldType.ftdImage:
			self.w = grid.w // 2
		self.x = grid.x
		self.y = grid.y
	
	def accept(self, visitor):
		return visitor.visitPlace(self)


# sets up a single grid
class Grid(Element):
	def __init__(self, obj):
		super().__init__(obj)
		self.open = obj["open"]
		# grid measurements
		numDivisions = 12
		self.numColumns = len(obj["columns"])
		self.w = (int) (numDivisions / self.numColumns)
		self.h = 1
		self.x = 1
		self.places = []
		for col in obj["columns"]:
			self.y = 1
			for item in col["items"]:
				self.places.append(Place(self, item))
				self.y += 1 # move one row farther down
			self.x += self.w # move one column farther over
	
	def accept(self, visitor):
		return visitor.visitGrid(self)

# this should basically set up a section 
# of the form, mainly just the attributes
class Section(Element):
	def __init__(self, obj):
		super().__init__(obj)
		self.open = obj["open"]
		self.label = obj["Label"]
		self.grids = []
		for grid in obj["contents"]:
			self.grids.append(Grid(grid))
	
	def accept(self, visitor):
		return visitor.visitSection(self)


class Form:
	def __init__(self):
		self.title = input("Form Name: ")
		self.control_name = to_control_name(self.title)
		self.json = json.loads(pyperclip.paste())
		self.sections = []
		for section in self.json:
			self.sections.append(Section(section))
	
	def accept(self, visitor):
		return visitor.visitForm(self)


