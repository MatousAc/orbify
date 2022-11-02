from visitors.visitor import Visitor
from helpers.xmlUtilities import tag, closing
from helpers.resources import bindLinkAttrs, bindPhoneAttrs
from formRepr.formBlocks import *
from formRepr.fields import *

class Binder(Visitor):
  xf = "xf:bind"

  def commonAttrs(self, block):
    attrs = {
      "id":			f"{block.control_name}-bind",
      "ref":		block.control_name,
      "name":		block.control_name,
      "readonly":	f'{"true" if block.readonly else "false"}()'
    }
    if not block.visible: # implicitly visible
      attrs["relevant"] = 'false()'
    if block.formBlock == FormBlock.field:
      req = block.validation["required"]
      attrs["required"] = f'{"true" if req else "false"}()'
    return attrs

  def visitForm(self, form: Form) -> str:
    src = ""
    for section in form.sections:
      src += section.accept(self)
    return src

  def visitSection(self, section: Section) -> str:
    src = tag(self.xf, attrDict=self.commonAttrs(section))
    for grid in section.grids:
      src += grid.accept(self)
    src += closing(self.xf)
    return src

  def visitGrid(self, grid: Grid) -> str:
    src = tag(self.xf, attrDict=self.commonAttrs(grid))
    for place in grid.places:
      src += place.accept(self)
    src += closing(self.xf)
    return src

  def visitPlace(self, place: Place) -> str:
    return place.field.accept(self)

  def visitText(self, text: Text) -> str:
    attrs = self.commonAttrs(text)
    attrs["xxf:whitespace"] = "trim"
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitArea(self, area: Area) -> str:
    attrs = self.commonAttrs(area)
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitRichText(self, richText: RichText) -> str:
    return tag(self.xf, attrDict=self.commonAttrs(richText),
      selfClosing=True)

  def visitNumeric(self, numeric: Numeric) -> str:
    attrs = self.commonAttrs(numeric)
    attrs["type"] = "xf:decimal"
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitCurrency(self, currency: Currency) -> str:
    attrs = self.commonAttrs(currency)
    attrs["type"] = "xf:decimal"
    attrs["constraint"] = f"xxf:fraction-digits({currency.precision})"
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitEmail(self, email: Email) -> str:
    attrs = self.commonAttrs(email)
    attrs["type"] = "xf:email"
    attrs["xxf:whitespace"] = "trim"
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitPhone(self, phone: Phone) -> str:
    attrs = self.commonAttrs(phone) | bindPhoneAttrs
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitLink(self, Link: Link) -> str:
    attrs = self.commonAttrs(Link) | bindLinkAttrs
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitDatadrop(self, datadrop: Datadrop) -> str:
    attrs = self.commonAttrs(datadrop)
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitDate(self, date: Date) -> str:
    attrs = self.commonAttrs(date)
    attrs["type"] = "xf:date"
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitRadio(self, radio: Radio) -> str:
    return tag(self.xf, attrDict=self.commonAttrs(radio),
      selfClosing=True)

  def visitYesNo(self, yesno: YesNo) -> str:
    attrs = self.commonAttrs(yesno)
    attrs["type"] = "xf:boolean"
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitCheckBox(self, checkBox: CheckBox) -> str:
    return tag(self.xf, attrDict=self.commonAttrs(checkBox),
      selfClosing=True)

  def visitDropDown(self, dropDown: DropDown) -> str:
    return tag(self.xf, attrDict=self.commonAttrs(dropDown), 
      selfClosing=True)

  def visitFile(self, file: File) -> str:
    attrs = self.commonAttrs(file)
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitSecret(self, secret: Secret) -> str:
    return tag(self.xf, attrDict=self.commonAttrs(secret), 
      selfClosing=True)

  def visitSignature(self, signature: Signature) -> str:
    attrs = self.commonAttrs(signature)
    attrs["type"] = "xf:anyURI"
    return tag(self.xf, attrDict=attrs, selfClosing=True)

  def visitFTDImage(self, FTDImage: FTDImage) -> str:
    attrs = self.commonAttrs(FTDImage)
    attrs["type"] = "xf:anyURI"
    return tag(self.xf, attrDict=attrs, selfClosing=True)
  
  def visitStaticText(self, staticText: StaticText) -> str:
    return tag(self.xf, attrDict=self.commonAttrs(staticText), 
      selfClosing=True)
  
  def visitLine(self, line: Line) -> str:
    return tag(self.xf, attrDict=self.commonAttrs(line), 
      selfClosing=True)

  def visitSpace(self, space: Space) -> str:
    return "" # space not represented
