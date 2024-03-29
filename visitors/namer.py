from visitors.visitor import Visitor
from helpers.xmlUtilities import tag, closing
from formRepr.formBlocks import *
from formRepr.fields import *
from helpers.resources import ftdImgAttrs, ftdImgInner

class Namer(Visitor):
  def visitForm(self, form: Form) -> str:
    src = tag("form")
    for section in form.sections:
      src += section.accept(self)
    src += closing("form")
    return src

  def visitSection(self, section: Section) -> str:
    src = tag(section.control_name)
    for grid in section.grids:
      src += grid.accept(self)
    src += closing(section.control_name)
    return src

  def visitGrid(self, grid: Grid) -> str:
    src = tag(grid.control_name)
    for place in grid.places:
      src += place.accept(self)
    src += closing(grid.control_name)
    return src

  def visitPlace(self, place: Place) -> str:
    return place.field.accept(self)

  # everything else gets a self-closing tag
  def visitText(self, text: Text) -> str:
    return tag(text.control_name, selfClosing=True)

  def visitArea(self, area: Area) -> str:
    return tag(area.control_name, selfClosing=True)

  def visitRichText(self, richText: RichText) -> str:
    return tag(richText.control_name, selfClosing=True)

  def visitNumeric(self, numeric: Numeric) -> str:
    return tag(numeric.control_name, selfClosing=True)

  def visitCurrency(self, currency: Currency) -> str:
    return tag(currency.control_name, selfClosing=True)

  def visitEmail(self, email: Email) -> str:
    return tag(email.control_name, selfClosing=True)

  def visitPhone(self, phone: Phone) -> str:
    return tag(phone.control_name, selfClosing=True)

  def visitLink(self, link: Link) -> str:
    return tag(link.control_name, selfClosing=True)

  def visitDatadrop(self, datadrop: Datadrop) -> str:
    return tag(datadrop.control_name, selfClosing=True)

  def visitDate(self, date: Date) -> str:
    return tag(date.control_name, selfClosing=True)

  def visitRadio(self, radio: Radio) -> str:
    return tag(radio.control_name, selfClosing=True)

  def visitYesNo(self, yesno: YesNo) -> str:
    return tag(yesno.control_name, selfClosing=True)

  def visitCheckBox(self, checkBox: CheckBox) -> str:
    return tag(checkBox.control_name, selfClosing=True)

  def visitDropDown(self, dropDown: DropDown) -> str:
    return tag(dropDown.control_name, selfClosing=True)

  def visitFile(self, file: File) -> str:
    return tag(file.control_name, selfClosing=True)

  def visitSecret(self, secret: Secret) -> str:
    return tag(secret.control_name, selfClosing=True)

  def visitSignature(self, signature: Signature) -> str:
    return tag(signature.control_name, selfClosing=True)

  def visitFTDImage(self, FTDImage: FTDImage) -> str:
    return tag(FTDImage.control_name, attrDict=ftdImgAttrs,
      innerText=ftdImgInner, close=True)

  def visitStaticText(self, staticText: StaticText) -> str:
    return tag(staticText.control_name, selfClosing=True)

  def visitLine(self, line: Line) -> str:
    return tag(line.control_name, selfClosing=True)
 
  def visitSpace(self, space: Space) -> str:
    return "" # spaces aren't included in the data mapping
