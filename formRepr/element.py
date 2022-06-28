import string
import random
from helpers.helps import *
from formRepr.mapsEnums import *

# keeps track of how many nameless grids we've had so far
fieldCount = 0
gridCount = 0
sectionCount = 0
# keeps track of all names to avoid conflicts
allControls = []

class Element: # basic attributes common to all elements
	def __init__(self, obj):
		self.displayName = obj["displayName"]
		self.show = obj["show"]
		# readonly
		self.readonly = False
		if "readonly" in list(obj.keys()):
			self.readonly = obj["readonly"]
		# everything is section/container/question/formTool
		self.formBlock = formBlockMap[obj["type"]]

		self.set_control_name(obj)
		# setting type for form fields
		if self.formBlock == FormBlock.field:
			self.fieldType = questionTypeMap[obj["QuestionType"]]
			self.validation = obj["validation"]
 
	def set_control_name(self, obj):
		global gridCount
		if self.formBlock == FormBlock.grid:
			self.control_name = f"grid_{gridCount}"
			gridCount += 1
		else:
			self.label = obj["Label"].strip().strip(":")
			self.control_name = to_control_name(self.label)
			self.label = self.label.replace("&", "&amp;")
		
		if self.formBlock == FormBlock.section:
			#default section name
			if self.control_name in ["section", ""]:
				global sectionCount
				self.control_name = f"section_{sectionCount}"
				sectionCount += 1
			# differentiate sections from form controls
			else:
				self.control_name = f"section_{self.control_name}"
		# missing field control name
		if (self.formBlock in [FormBlock.field, FormBlock.formTool] and 
			(self.label == "" or self.control_name == "")):
			global fieldCount
			self.label = f"Field {fieldCount}"
			self.control_name = f"field_{fieldCount}"
			fieldCount += 1
		self.preventConflicts()

	def preventConflicts(self):
		while self.control_name in allControls:
			letter = random.choice(string.ascii_lowercase)
			self.control_name += letter
			self.label += letter
		allControls.append(self.control_name)

	def accept(self, visitor):
		match self.fieldType:
			case FieldType.text: 			return visitor.visitText(self)
			case FieldType.richText:	return visitor.visitRichText(self)
			case FieldType.numeric:		return visitor.visitNumeric(self)
			case FieldType.currency:	return visitor.visitCurrency(self)
			case FieldType.email: 		return visitor.visitEmail(self)
			case FieldType.phone: 		return visitor.visitPhone(self)
			case FieldType.link:			return visitor.visitLink(self)
			case FieldType.contact: 	return visitor.visitContact(self)
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
			case FieldType.line:			return visitor.visitLine(self)
			case FieldType.space: 		return visitor.visitSpace(self)
