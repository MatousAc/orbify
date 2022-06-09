class Visitor:
	def visitForm(self, form):
		raise Exception("Abstract method 'visitForm'")
	def visitSection(self, section):
		raise Exception("Abstract method 'visitSection'")
	def visitGrid(self, grid):
		raise Exception("Abstract method 'visitGrid'")
	def visitFieldHolder(self, fieldHolder):
		raise Exception("Abstract method 'visitFieldHolder'")
	def visitText(self, field):
		raise Exception("Abstract method 'visitText'")
	def visitRichText(self, field):
		raise Exception("Abstract method 'visitRichText'")
	def visitNumeric(self, field):
		raise Exception("Abstract method 'visitNumeric'")
	def visitCurrency(self, field):
		raise Exception("Abstract method 'visitCurrency'")
	def visitEmail(self, field):
		raise Exception("Abstract method 'visitEmail'")
	def visitDate(self, field):
		raise Exception("Abstract method 'visitDate'")
	def visitRadio(self, field):
		raise Exception("Abstract method 'visitRadio'")
	def visitYesNo(self, field):
		raise Exception("Abstract method 'visitYesNo'")
	def visitCheckBox(self, field):
		raise Exception("Abstract method 'visitCheckBox'")
	def visitDropDown(self, field):
		raise Exception("Abstract method 'visitDropDown'")
	def visitFileAttach(self, field):
		raise Exception("Abstract method 'visitFileAttach'")
	def visitSecret(self, field):
		raise Exception("Abstract method 'visitSecret'")
	def visitSignature(self, field):
		raise Exception("Abstract method 'visitSignature'")
	def visitStaticText(self, field):
		raise Exception("Abstract method 'visitStaticText'")
	def visitSpace(self, field):
		raise Exception("Abstract method 'visitSpace'")