from visitors.visitor import Visitor
from helpers.xmlUtilities import tag, closing
from formRepr.formBlocks import *
from formRepr.fields import *

class Binder(Visitor):
	xf = "xf:bind"

	def idRefName(self, block):
		return {
			"id":		f"{block.control_name}-bind",
			"ref":	block.control_name,
			"name":	block.control_name
		}

	def visitForm(self, form: Form) -> str:
		src = ""
		for section in form.sections:
			src += section.accept(self)
		return src

	def visitSection(self, section: Section) -> str:
		src = tag(self.xf, attrDict=self.idRefName(section))
		for grid in section.grids:
			src += grid.accept(self)
		src += closing(self.xf)
		return src

	def visitGrid(self, grid: Grid) -> str:
		src = tag(self.xf, attrDict=self.idRefName(grid))
		for place in grid.places:
			src += place.accept(self)
		src += closing(self.xf)
		return src

	def visitPlace(self, place: Place) -> str:
		return place.field.accept(self)

	def visitText(self, text: Text) -> str:
		attrs = self.idRefName(text)
		attrs["xxf:whitespace"] = "trim"
		return tag(self.xf, attrDict=attrs, selfClosing=True)

	def visitRichText(self, richText: RichText) -> str:
		return tag(self.xf, attrDict=self.idRefName(richText),
			selfClosing=True)

	def visitNumeric(self, numeric: Numeric) -> str:
		attrs = self.idRefName(numeric)
		attrs["type"] = "xf:decimal"
		return tag(self.xf, attrDict=attrs, selfClosing=True)

	def visitCurrency(self, currency: Currency) -> str:
		attrs = self.idRefName(currency)
		attrs["type"] = "xf:decimal"
		attrs["constraint"] = f"xxf:fraction-digits({currency.precision})"
		return tag(self.xf, attrDict=attrs, selfClosing=True)

	def visitEmail(self, email: Email) -> str:
		attrs = self.idRefName(email)
		attrs["type"] = "xf:email"
		attrs["xxf:whitespace"] = "trim"
		return tag(self.xf, attrDict=attrs, selfClosing=True)

	def visitDate(self, date: Date) -> str:
		attrs = self.idRefName(date)
		attrs["type"] = "xf:date"
		return tag(self.xf, attrDict=attrs, selfClosing=True)

	def visitRadio(self, radio: Radio) -> str:
		return tag(self.xf, attrDict=self.idRefName(radio),
			selfClosing=True)

	def visitYesNo(self, yesno: YesNo) -> str:
		attrs = self.idRefName(yesno)
		attrs["type"] = "xf:boolean"
		return tag(self.xf, attrDict=attrs, selfClosing=True)

	def visitCheckBox(self, checkBox: CheckBox) -> str:
		return tag(self.xf, attrDict=self.idRefName(checkBox),
			selfClosing=True)

	def visitDropDown(self, dropDown: DropDown) -> str:
		return tag(self.xf, attrDict=self.idRefName(dropDown), 
			selfClosing=True)

	def visitFileAttach(self, fileAttach: FileAttach) -> str:
		attrs = self.idRefName(fileAttach)
		attrs["type"] = "xf:anyURI"
		return tag(self.xf, attrDict=attrs, selfClosing=True)

	def visitSecret(self, secret: Secret) -> str:
		return tag(self.xf, attrDict=self.idRefName(secret), 
			selfClosing=True)

	def visitSignature(self, signature: Signature) -> str:
		attrs = self.idRefName(signature)
		attrs["type"] = "xf:anyURI"
		return tag(self.xf, attrDict=attrs, selfClosing=True)

	def visitStaticText(self, staticText: StaticText) -> str:
		return tag(self.xf, attrDict=self.idRefName(staticText), 
			selfClosing=True)

	def visitSpace(self, space: Space) -> str:
		return "" # space not represented
