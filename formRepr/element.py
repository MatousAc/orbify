from helpers.helps import *
from formRepr.mapsEnums import *

# keeps track of how many nameless grids we've had so far
gridCount = 0
sectionCount = 0
anonControlCount = 0

class Element: # basic attributes common to all elements
	def __init__(self, obj):
		self.displayName = obj["displayName"]
		self.show = obj["show"]
		# everything is section/container/question/formTool
		self.formBlock = formBlockMap[obj["type"]]

		# control_names
		global gridCount
		if self.formBlock == FormBlock.grid:
			self.control_name = f"grid_{gridCount}"
			gridCount += 1
		else: 
			self.label = obj["Label"]
			self.control_name = to_control_name(self.label)

		# change default section name
		if (self.formBlock == FormBlock.section 
			and self.control_name == "section"):
			global sectionCount
			self.control_name += f"_{sectionCount}"
			sectionCount += 1
		# setting type for form fields
		if self.formBlock == FormBlock.field:
			self.fieldType = questionTypeMap[obj["QuestionType"]]
			self.validation = obj["validation"]
		
		if self.fieldType == FieldType.ftdImage:
			self.handleFTDImage(obj)
	
	def handleFTDImage(self, obj):
		txt = obj["properties"]["imageFile"]["text"].lower()
		if "ftd logo" not in txt: 
			self.fieldType = FieldType.space
		
   

	def accept(self, visitor):
		match self.fieldType:
			case FieldType.text: 			return visitor.visitText(self)
			case FieldType.richText:	return visitor.visitRichText(self)
			case FieldType.numeric:		return visitor.visitNumeric(self)
			case FieldType.currency:	return visitor.visitCurrency(self)
			case FieldType.email: 		return visitor.visitEmail(self)
			case FieldType.date: 			return visitor.visitDate(self)
			case FieldType.radio: 		return visitor.visitRadio(self)
			case FieldType.yesno:			return visitor.visitYesNo(self)
			case FieldType.checkbox: 	return visitor.visitCheckBox(self)
			case FieldType.dropdown: 	return visitor.visitDropDown(self)
			case FieldType.fileAttach:return visitor.visitFileAttach(self)
			case FieldType.secret: 		return visitor.visitSecret(self)
			case FieldType.signature: return visitor.visitSignature(self)
			case FieldType.ftdImage:	return visitor.visitFTDImage(self)
			case FieldType.staticText:return visitor.visitStaticText(self)
			case FieldType.space: 		return visitor.visitSpace(self)
