from formRepr.formBlocks import *
from formRepr.fields import *
class Visitor:
  def visitForm(self, form: Form) -> str:
    raise Exception("Abstract method 'visitForm'")
  def visitSection(self, section: Section) -> str:
    raise Exception("Abstract method 'visitSection'")
  def visitGrid(self, grid: Grid) -> str:
    raise Exception("Abstract method 'visitGrid'")
  def visitPlace(self, place: Place) -> str:
    raise Exception("Abstract method 'visitPlace'")
  def visitText(self, text: Text) -> str:
    raise Exception("Abstract method 'visitText'")
  def visitArea(self, area: Area) -> str:
    raise Exception("Abstract method 'visitArea'")
  def visitRichText(self, richText: RichText) -> str:
    raise Exception("Abstract method 'visitRichText'")
  def visitNumeric(self, numeric: Numeric) -> str:
    raise Exception("Abstract method 'visitNumeric'")
  def visitCurrency(self, currency: Currency) -> str:
    raise Exception("Abstract method 'visitCurrency'")
  def visitEmail(self, email: Email) -> str:
    raise Exception("Abstract method 'visitEmail'")
  def visitPhone(self, phone: Phone) -> str:
    raise Exception("Abstract method 'visitPhone'")
  def visitLink(self, link: Link) -> str:
    raise Exception("Abstract method 'visitLink'")
  def visitDatadrop(self, datadrop: Datadrop) -> str:
    raise Exception("Abstract method 'visitDatadrop'")
  def visitDate(self, date: Date) -> str:
    raise Exception("Abstract method 'visitDate'")
  def visitRadio(self, radio: Radio) -> str:
    raise Exception("Abstract method 'visitRadio'")
  def visitYesNo(self, yesno: YesNo) -> str:
    raise Exception("Abstract method 'visitYesNo'")
  def visitCheckBox(self, checkBox: CheckBox) -> str:
    raise Exception("Abstract method 'visitCheckBox'")
  def visitDropDown(self, dropDown: DropDown) -> str:
    raise Exception("Abstract method 'visitDropDown'")
  def visitFile(self, file: File) -> str:
    raise Exception("Abstract method 'visitFile'")
  def visitSecret(self, secret: Secret) -> str:
    raise Exception("Abstract method 'visitSecret'")
  def visitSignature(self, signature: Signature) -> str:
    raise Exception("Abstract method 'visitSignature'")
  def visitFTDImage(self, image: StaticText) -> str:
    raise Exception("Abstract method 'visitFTDImage'")
  def visitStaticText(self, staticText: StaticText) -> str:
    raise Exception("Abstract method 'visitStaticText'")
  def visitLine(self, line: Line) -> str:
    raise Exception("Abstract method 'visitLine'")
  def visitSpace(self, space: Space) -> str:
    raise Exception("Abstract method 'visitSpace'")