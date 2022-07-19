from visitors.visitor import Visitor
from helpers.xmlUtilities import tag
from formRepr.formBlocks import *
from formRepr.fields import *
from helpers.actionServiceDefs import *

dropCount = {
	DropType.ftdUsers: 0,
	DropType.clients: 0
}

class Actor(Visitor):
	def servInst(self, name):
		body = tag("body", attrDict=servInstBodyAttrs,
      innerText="&lt;params/&gt;", close=True)
		return tag("xf:instance", attrDict=servInstAttrs, 
      attrStr=f'id="{name}-instance"', innerText=body, close=True)
	
	def servSubmit(self, name, resource):
		attrs = {
			"id": f"{name}-submission",
			"resource": resource,
		}
		attrs = attrs | servSubmitAttrs
		return tag("xf:submission", attrDict=attrs, selfClosing=True)
	
	def action(self, name, field, items, lbl, val):
		xfa = "xf:action"; xfv = "xf:var"
		# three tabs of settings to generate
		general = tag(xfa, attrDict=actGenAttrs, 
      attrStr=f'ev:observer="{field.control_name}-control"',
      innerText=tag("xf:send", attrStr=f'submission="{name}-submission"',
        selfClosing=True),
      close=True)
		
		reqAttrs = {
			"event": "xforms-submit",
			"ev:observer": f"{name}-submission"
		}
		reqVarAttrs = {
			"name": "request-instance-name",
   		"value": f"'{name}-instance'"
		}
		request = tag(xfa, attrDict=reqAttrs,
      innerText=tag(xfv, attrDict=reqVarAttrs, selfClosing=True) + 
      	tag(xfa, selfClosing=True), close=True)
		
		itemset = tag(xfa, attrDict=actResItemAttrs, innerText=(
			tag(xfv, attrStr=f'name="control-name" value="\'{field.control_name}\'"', selfClosing=True) +
			tag(xfv, attrStr=f'name="response-items" value="{items}"', selfClosing=True) +
			tag(xfv, attrStr=f'name="item-label" value="{lbl}"', selfClosing=True) +
			tag(xfv, attrStr=f'name="item-value" value="{val}"', selfClosing=True)
		), close=True)
		resAttrs = {
			"event": "xforms-submit-done",
   		"ev:observer": f"{name}-submission"
		}
		response = tag(xfa, attrDict=resAttrs, innerText=itemset, close=True)
		return tag(xfa, attrStr=f'id="{name}-binding"', 
			innerText=general + request + response, close=True)
	
	# datadrop search gets actions and services
	def visitDatadrop(self, datadrop: Datadrop) -> str:
		match datadrop.dropType:
			case DropType.ftdUsers:
				servName = "get-ftd-users"
				items ="/*/user"
				label ="name"
				value ="id"
				res = resURL + "/users/data.orbeon"
			case DropType.clients:
				servName = "get-clients"
				items ="/*/client"
				label ="name"
				value ="id"
				res = resURL + "/orbeon/clients"
			case DropType.none: return ''
		
		global dropCount
		if dropCount[datadrop.dropType]:
			servName += str(dropCount[datadrop.dropType])
		dropCount[datadrop.dropType] += 1
		src = self.servInst(servName)
		src += self.servSubmit(servName, res)
		src += self.action(servName, datadrop, items, label, value)
		return src
  
  # container fields only pass down and distribute the Actor
	def visitForm(self, form: Form) -> str:
		src = ""
		for section in form.sections:
			src += section.accept(self)
		return src

	def visitSection(self, section: Section) -> str:
		src = ""
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

	# most fields don't need any actions or services
	def visitText(self, text: Text) -> str:
		return ""

	def visitArea(self, area: Area) -> str:
		return ""

	def visitRichText(self, richText: RichText) -> str:
		return ""

	def visitNumeric(self, numeric: Numeric) -> str:
		return ""

	def visitCurrency(self, currency: Currency) -> str:
		return ""

	def visitEmail(self, email: Email) -> str:
		return ""

	def visitPhone(self, phone: Phone) -> str:
		return ""

	def visitLink(self, link: Link) -> str:
		return ""

	def visitDate(self, date: Date) -> str:
		return ""

	def visitRadio(self, radio: Radio) -> str:
		return ""

	def visitYesNo(self, yesno: YesNo) -> str:
		return ""

	def visitCheckBox(self, checkBox: CheckBox) -> str:
		return ""

	def visitDropDown(self, dropDown: DropDown) -> str:
		return ""

	def visitFileAttach(self, fileAttach: FileAttach) -> str:
		return ""

	def visitSecret(self, secret: Secret) -> str:
		return ""

	def visitSignature(self, signature: Signature) -> str:
		return ""

	def visitFTDImage(self, FTDImage: FTDImage) -> str:
		return ""

	def visitStaticText(self, staticText: StaticText) -> str:
		return ""

	def visitLine(self, line: Line) -> str:
		return ""
 
	def visitSpace(self, space: Space) -> str:
		return "" # spaces aren't included in the data mapping
