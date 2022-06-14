from enum import Enum, auto

class FieldType(Enum): # defining all the different field types
	text,	richText, numeric, email, date = auto(), auto(), auto(), auto(), auto()
	radio, checkbox, dropdown, fileAttach = auto(), auto(), auto(), auto()
	secret, signature, currency, yesno = auto(), auto(), auto(), auto()
	ftdImage, staticText, space = auto(), auto(), auto() # form tools
	

questionTypeMap = {
	# real fields
	"ShortText": FieldType.text,
	"LongText": FieldType.text,
	"SearchBox": FieldType.text,
	"ContactSearch": FieldType.text,
	"Hyperlink": FieldType.text, # eventually make link type?
	"RichText": FieldType.richText,
	"Number": FieldType.numeric,
	"EmailAddress": FieldType.email,
	"Calendar": FieldType.date,
	"DbRadioButton": FieldType.radio,
	"DbCheckbox": FieldType.checkbox,
	"DbSelectList": FieldType.dropdown,
	"FileAttachment": FieldType.fileAttach,
	"Password": FieldType.secret,
	"Signature": FieldType.signature,
	# form tools
	"Image": FieldType.ftdImage,
	"FormText": FieldType.staticText,
	"BlankSpace": FieldType.space,
}

# the different levels of form building blocks
class FormBlock(Enum):
	section, grid, field, formTool = auto(), auto(), auto(), auto()

formBlockMap = {
	"Section_Type": FormBlock.section,
	"Container_Type": FormBlock.grid,
	"Question_Type": FormBlock.field,
	"FormTool_Type": FormBlock.formTool
}