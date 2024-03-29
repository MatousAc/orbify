from enum import Enum, auto

class FieldType(Enum): # defining all the different field types
  text, area,	richText, numeric, date = auto(), auto(), auto(), auto(), auto()
  email, phone, link, datadrop = auto(), auto(), auto(), auto()
  radio, checkbox, dropdown, file = auto(), auto(), auto(), auto()
  secret, signature, currency, yesno = auto(), auto(), auto(), auto()
  ftdImage, staticText, space, line = auto(), auto(), auto(), auto() # form tools


questionTypeMap = {
  # real fields
  "ShortText": FieldType.text,
  "SearchBox": FieldType.text,
  "LongText": FieldType.area,
  "RichText": FieldType.richText,
  "Number": FieldType.numeric,
  "EmailAddress": FieldType.email,
  "Hyperlink": FieldType.link,
  "Calendar": FieldType.date,
  "DbRadioButton": FieldType.radio,
  "DbCheckbox": FieldType.checkbox,
  "ContactSearch": FieldType.datadrop,
  "MultiContactSearch": FieldType.datadrop,
  "DbSelectList": FieldType.dropdown,
  "FileAttachment": FieldType.file,
  "MultiFileAttachment": FieldType.file,
  "Password": FieldType.secret,
  "Signature": FieldType.signature,
  # form tools
  "Image": FieldType.ftdImage,
  "FormText": FieldType.staticText,
  "HorizontalRule": FieldType.line,
  "BlankSpace": FieldType.space,
  "Grid": FieldType.space,
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