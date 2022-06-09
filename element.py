from helps import *
from mapsEnums import *

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
