from helpers.helps import *
from formRepresentation.mapsEnums import *

# keeps track of how many nameless grids we've had so far
gridCount = 0

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

		# just setting type
		if self.formBlock in [FormBlock.field, FormBlock.formTool]:
			self.fieldType = questionTypeMap[obj["QuestionType"]]
		# setting general stuff for form fields
		if self.formBlock == FormBlock.field:
			self.validation = obj["validation"]
	
	# def accept(self, visitor):
	# 	raise Exception("Abstract accept. Should override.")

	def accept(self, visitor):
		match self.fieldType:
			case FieldType.text: 			visitor.visitText(self)
			case FieldType.richText:	visitor.visitRichText(self)
			case FieldType.numeric:		visitor.visitNumeric(self)
			case FieldType.currency:	visitor.visitCurrency(self)
			case FieldType.email: 		visitor.visitEmail(self)
			case FieldType.date: 			visitor.visitDate(self)
			case FieldType.radio: 		visitor.visitRadio(self)
			case FieldType.yesno:			visitor.visitYesNo(self)
			case FieldType.checkbox: 	visitor.visitCheckBox(self)
			case FieldType.dropdown: 	visitor.visitDropDown(self)
			case FieldType.fileAttach:visitor.visitFileAttach(self)
			case FieldType.secret: 		visitor.visitSecret(self)
			case FieldType.signature: visitor.visitSignature(self)
			case FieldType.staticText:visitor.visitStaticText(self)
			case FieldType.space: 		visitor.visitSpace(self)
