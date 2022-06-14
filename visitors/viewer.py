from random import choices
from visitors.visitor import Visitor
from helpers.xmlUtilities import tag
from formRepr.formBlocks import *
from formRepr.fields import *
from helpers.resources import *

class Viewer(Visitor):
	def ref(self, block, resource):
		return f' ref="$form-resources/{block.control_name}/{resource}"'

	def idBind(self, block) -> str:
		id = f"{block.control_name}-"
		match block.formBlock:
			case FormBlock.section: 	id += "section"
			case FormBlock.grid: 	id += "grid"
			case FormBlock.field: 	id += "control"
			case FormBlock.formTool: 	id += "control"
		bind = f"{block.control_name}-bind"
		return f"id=\"{id}\" bind=\"{bind}\""

	def basicTag(self, block, t): # t = tag
		return tag(f"xf:{t}", attrStr=self.ref(block, t),
			selfClosing=True)

	def basicAlert(self):
		return '<xf:alert ref="$fr-resources/detail/labels/alert"/>\n'

	def basic3(self, block):
		return (self.basicTag(block, "label") +
			self.basicTag(block, "hint") +
			self.basicAlert())

	def itemset(self, block):
		src = tag("xf:label", attrStr="ref=\"label\"", selfClosing=True)
		src += tag("xf:value", attrStr="ref=\"value\"", selfClosing=True)
		src += tag("xf:hint", attrStr="ref=\"hint\"", selfClosing=True)
		return tag("xf:itemset", attrStr=self.ref(block, "item"),
			innerText=src, close=True)

	def visitForm(self, form: Form) -> str:
		src = ""
		for section in form.sections:
			src += section.accept(self)
		return src

	def visitSection(self, section: Section) -> str:
		src = self.basicTag(section, "label")
		for grid in section.grids:
			src += grid.accept(self)
		return tag("fr:section", attrStr=self.idBind(section),
			innerText=src, close=True)

	def visitGrid(self, grid: Grid) -> str:
		src = ""
		for place in grid.places:
			src += place.accept(self)
		return tag("fr:grid", attrStr=self.idBind(grid),
			innerText=src, close=True)

	# this is finally where the "place" block is useful!
	def visitPlace(self, p: Place) -> str: # p=place
		placement = f'x="{p.x}" y="{p.y}" w="{p.w}" h="{p.h}"'
		return tag("fr:c", attrStr=placement,
			innerText=p.field.accept(self), close=True)

	def visitText(self, text: Text) -> str:
		src = self.basic3(text)
		return tag("xf:input", attrStr=self.idBind(text),
			innerText=src, close=True)

	def visitRichText(self, richText: RichText) -> str:
		src = self.basic3(richText)
		return tag("fr:tinymce", attrDict=viewRichText,
			attrStr=self.idBind(richText), innerText=src, close=True)

	def visitNumeric(self, numeric: Numeric) -> str:
		src = self.basic3(numeric)
		return tag("fr:number", attrDict=viewNumeric,
			attrStr=self.idBind(numeric), innerText=src, close=True)

	def visitCurrency(self, currency: Currency) -> str:
		src = self.basic3(currency)
		attrs = viewCurrency.copy()
		attrs["prefix"] = currency.prefix
		attrs["digits-after-decimal"] = currency.precision
		return tag("fr:currency", attrDict=attrs,
			attrStr=self.idBind(currency), innerText=src, close=True)

	def visitEmail(self, email: Email) -> str:
		src = self.basic3(email)
		return tag("xf:input", attrStr=self.idBind(email),
			innerText=src, close=True)

	def visitDate(self, date: Date) -> str:
		src = self.basic3(date)
		return tag("fr:date", attrDict=viewDate,
			attrStr=self.idBind(date), innerText=src, close=True)

	def visitRadio(self, radio: Radio) -> str:
		src = self.basic3(radio)
		src += self.itemset(radio)
		return tag("xf:select1", attrDict=viewRadio,
			attrStr=self.idBind(radio), innerText=src, close=True)

	def visitYesNo(self, yesno: YesNo) -> str:
		src = self.basic3(yesno)
		return tag("fr:yesno-input", attrDict=viewYesNo,
			attrStr=self.idBind(yesno), innerText=src, close=True)

	def visitCheckBox(self, checkBox: CheckBox) -> str:
		src = self.basic3(checkBox)
		src += self.itemset(checkBox)
		return tag("xf:select", attrDict=viewCheckBox,
			attrStr=self.idBind(checkBox), innerText=src, close=True)

	def visitDropDown(self, dropDown: DropDown) -> str:
		src = self.basic3(dropDown)
		src += self.itemset(dropDown)
		# default to searchable list if there are many choices
		isSearch = len(dropDown.choices) > 3
		attrs = {
			"appearance": "search" if isSearch else "dropdown"
		}
		return tag("xf:select1", attrDict=attrs,
			attrStr=self.idBind(dropDown), innerText=src, close=True)

	def visitFileAttach(self, fileAttach: FileAttach) -> str:
		src = self.basic3(fileAttach)
		return tag("fr:attachment", attrDict=viewAttach,
			attrStr=self.idBind(fileAttach), innerText=src, close=True)

	def visitSecret(self, secret: Secret) -> str:
		src = self.basic3(secret)
		return tag("xf:secret", attrStr=self.idBind(secret),
		innerText=src, close=True)

	def visitSignature(self, signature: Signature) -> str:
		src = self.basic3(signature)
		return tag("fr:handwritten-signature", attrDict=viewSignature,
			attrStr=self.idBind(signature), innerText=src, close=True)

	def visitFTDImage(self, FTDImage: FTDImage) -> str:
		src = (self.basicTag(FTDImage, "label") +
      self.basicAlert())
		return tag("fr:image", attrDict=viewImage,
      attrStr=self.idBind(FTDImage),
      innerText=src, close=True)
		
	def visitStaticText(self, staticText: StaticText) -> str:
		media = 'mediatype="text/html"'
		text = tag("fr:text", selfClosing=True,
			attrStr=f'{self.ref(staticText, "text")} {media}')
		return tag("fr:explanation", attrDict=viewStaticText,
			attrStr=self.idBind(staticText), 
			innerText=text, close=True)

	def visitSpace(self, space: Space) -> str:
		return "" # space not represented
