from formRepr.fields import *
from helpers.helps import *
from formRepr.mapsEnums import *
# holds all control_names that need to be 
# added in Genify for this form
fieldControls = []

def trackNames(field):
  if field.formBlock == FormBlock.field:
    global fieldControls
    fieldControls.append(field.control_name)

class Place():
  def __init__(self, grid, item):
    field = None # create an instance of the field
    match questionTypeMap[item["QuestionType"]]:
      case FieldType.text:
        if isPhone(item):				field = Phone(item)
        else:										field = Text(item)
      case FieldType.area:			field = Area(item)
      case FieldType.richText:	field = RichText(item)
      case FieldType.numeric:
        if item["format"]["currency"]["useCurrency"]:
                                field = Currency(item)
        else: 									field = Numeric(item)
      case FieldType.email: 		field = Email(item)
      case FieldType.link: 			field = Link(item)
      case FieldType.datadrop:	field = Datadrop(item)
      case FieldType.date: 			field = Date(item)
      case FieldType.radio: 		
        if isYesNo(item["Choices"]):
                                field = YesNo(item)
        else: 									field = Radio(item)
      case FieldType.checkbox:
        if isYesNo(item["Choices"]):
                                field = YesNo(item)
        else: 									field = CheckBox(item)
      case FieldType.dropdown: 	
        if (item["dbSettings"]["useDB"]):
                                field = Datadrop(item)
        else: 									field = DropDown(item)
      case FieldType.file:      field = File(item)
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
    self.h = grid.curH
    self.w = grid.curW
    if field.fieldType == FieldType.ftdImage:
      self.w = grid.curW // 2
    self.x = grid.curX
    self.y = grid.curY
  
  def accept(self, visitor):
    return visitor.visitPlace(self)


# sets up a single grid
class Grid(Element):
  def __init__(self, obj):
    super().__init__(obj)
    self.open = obj["open"]
    # getting grid measurements
    numDivisions = 12
    self.numColumns = len(obj["columns"])
    self.numRows = 0
    for col in obj["columns"]:
      numRows = len(col["items"])
      if numRows > self.numRows:
        self.numRows = numRows
    # where we are in the grid right now
    self.curW = (int) (numDivisions / self.numColumns)
    self.curH = 1
    self.curX = 1
    self.places = []
    for col in obj["columns"]:
      self.curY = 0
      for item in col["items"]:
        self.curY += 1 # move one row farther down
        self.places.append(Place(self, item))
      # here we insert blank spaces wherever there aren't enough
      # fields to fill up the total number of rows
      numSpaces = self.numRows - self.curY
      while numSpaces > 0:
        self.curY += 1
        # add space
        self.places.append(Place(self, spaceItem()))
        numSpaces -= 1
      self.curX += self.curW # move one column farther over
  
  def accept(self, visitor):
    return visitor.visitGrid(self)

# this should basically set up a section 
# of the form, mainly just the attributes
class Section(Element):
  def __init__(self, obj):
    super().__init__(obj)
    self.open = obj["open"]
    self.grids = []
    for grid in obj["contents"]:
      self.grids.append(Grid(grid))
  
  def accept(self, visitor):
    return visitor.visitSection(self)


class Form:
  def __init__(self, title, json):
    self.title = title
    self.control_name = to_control_name(self.title)
    self.json = json
    self.sections = []
    for section in self.json:
      self.sections.append(Section(section))
  
  def accept(self, visitor):
    return visitor.visitForm(self)


