from visitors.visitor import Visitor
from helpers.xmlUtilities import tag, closing
from helpers.resources import srcFormTextAttrs, hintTag, sourceLine
from formRepr.formBlocks import *
from formRepr.fields import *

class Sourcer(Visitor):
	def visitForm(self, form: Form) -> str:
		src = ""
		for section in form.sections:
			src += section.accept(self)
		return src

	def labelHelp(self, section: Section): # helper
		l = tag("label", innerText=section.label, close=True)
		h = " " + tag("help", selfClosing=True)
		return tag(section.control_name, innerText=l+h, close=True)
	
	def visitSection(self, section: Section) -> str:
		src = self.labelHelp(section)
		for grid in section.grids:
			src += grid.accept(self)
		return src

	def visitGrid(self, grid: Grid) -> str:
		src = ""
		for place in grid.places:
			src += place.accept(self)
		return src

	def visitPlace(self, place: Place) -> str:
		return place.field.accept(self)

	def labelHint(self, field): # helper
		l = tag("label", innerText=field.label, close=True)
		return tag(field.control_name, 
			innerText=f"{l} {hintTag}", close=True)

	def visitText(self, text: Text) -> str:
		return self.labelHint(text)

	def visitArea(self, area: Area) -> str:
		return self.labelHint(area)

	def visitRichText(self, richText: RichText) -> str:
		return self.labelHint(richText)

	def visitNumeric(self, numeric: Numeric) -> str:
		return self.labelHint(numeric)

	def visitCurrency(self, currency: Currency) -> str:
		return self.labelHint(currency)

	def visitEmail(self, email: Email) -> str:
		return self.labelHint(email)
		
	def visitPhone(self, phone: Phone) -> str:
		return self.labelHint(phone)
	
	def visitLink(self, link: Link) -> str:
		return self.labelHint(link)

	def visitDatadrop(self, datadrop: Datadrop) -> str:
		return self.labelHint(datadrop)

	def visitDate(self, date: Date) -> str:
		return self.labelHint(date)

	def itemResources(self, field, needHint = False):
		src = tag(field.control_name)
		src += tag("label", innerText=field.label, close=True)
		src += f" {hintTag}\n"
		for label, value in field.choices.items():
			inner = tag("label", innerText=label, close=True)
			inner += f"{hintTag}\n" if needHint else ""
			inner += tag("value", innerText=value, close=True)
			src += tag("item", innerText=inner, close=True)
		src += closing(field.control_name)
		return src

	def visitRadio(self, radio: Radio) -> str:
		return self.itemResources(radio)

	def visitYesNo(self, yesno: YesNo) -> str:
		return self.labelHint(yesno)

	def visitCheckBox(self, checkBox: CheckBox) -> str:
		return self.itemResources(checkBox, needHint=True)

	def visitDropDown(self, dropDown: DropDown) -> str:
		return self.itemResources(dropDown)

	def visitFileAttach(self, fileAttach: FileAttach) -> str:
		return self.labelHint(fileAttach)

	def visitSecret(self, secret: Secret) -> str:
		return self.labelHint(secret)

	def visitSignature(self, signature: Signature) -> str:
		return self.labelHint(signature)

	def visitFTDImage(self, FTDImage: FTDImage) -> str:
		return tag(FTDImage.control_name, close=True,
      innerText=tag("label", selfClosing=True))

	def visitStaticText(self, staticText: StaticText) -> str:
		src = tag("text", attrStr=srcFormTextAttrs,
			innerText=staticText.text, close=True)
		return tag(staticText.control_name,
			innerText=src, close=True)

	def visitLine(self, line: Line) -> str:
		src = tag("text", attrStr=srcFormTextAttrs,
			innerText=sourceLine, close=True)
		return tag(line.control_name,
			innerText=src, close=True)

	def visitSpace(self, space: Space) -> str:
		return ""
