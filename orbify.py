from formRepresentation.formBlocks import *
from helpers.resources import *
from helpers.xmlUtilities import *


def genModel(form):
	# opening
	src = tag("xh:head")
	src += tag("xh:title", innerText=form.title, close=True)
	src += tag("xf:model", attrStr=modelAttrs)
	# laying out the data
	src += tag("xf:instance", attrStr=modelDataMapAttrs,
		innerText="form", close=True)
	# binding data to names
	src += tag("xf:bind", attrStr=modelBindAttrs)
	# throw in the metadata and attachment tags
	src += tag("xf:instance", attrStr=modelMetaAttrs)
	src += tag("xf:instance", attrStr=modelAttachAttrs)
	# lay out the forms resources
	src += tag("xf:instance", attrStr=modelResourcesAttrs)

	
	# closing
	src += closing("xf:model") + closing("xh:head")
	return src


def genView(form):
	return ""


def gen_xhtml(form):
	src = tag("xh:html", htmlAttrs)
	src += genModel(form)
	src += genView(form)
	src += closing("xh:html")
	return src


if __name__ == "__main__":
	form = Form()
	src = gen_xhtml(form)
	print(src)
