from formRepr.formBlocks import *
from helpers.resources import *
from helpers.xmlUtilities import *
from visitors.binder import Binder
from visitors.namer import Namer
from visitors.sourcer import Sourcer
from visitors.viewer import Viewer
import pyperclip


def genMeta(form: Form) -> str:
	src = (
		tag("application-name", innerText="ftd", close=True) +
		tag("form-name", innerText=form.control_name, close=True) +
		tag("title", attrStr=enlang, innerText=form.title, close=True) +
		tag("description", attrStr=enlang, selfClosing=True) +
		tag("created-with-version", innerText=version, close=True) +
		tag("updated-with-version", innerText=version, close=True)
	)
	return tag("metadata", innerText=src, close=True)
	

def genModel(form: Form) -> str:
	# opening
	src = tag("xh:head")
	src += tag("xh:title", innerText=form.title, close=True)
	src += tag("xf:model", attrStr=modelAttrs)
	
	# laying out the data
	dataMapper = Namer()
	src += tag("xf:instance", attrStr=modelDataMapAttrs,
		innerText=form.accept(dataMapper), close=True)
	
	# binding data to names
	binder = Binder()
	src += tag("xf:bind", attrStr=modelBindAttrs,
		innerText=form.accept(binder), close=True)
	
	# throw in the metadata and attachment tags
	src += tag("xf:instance", attrStr=modelMetaAttrs,
		innerText=genMeta(form), close=True)
	src += tag("xf:instance", attrStr=modelAttachAttrs,
		innerText=tag("attachments", selfClosing=True), close=True)
	
	# lay out the forms resources
	sourcer = Sourcer()
	resource = tag("resource", attrStr=enlang,
		innerText=form.accept(sourcer), close=True)
	resources = tag("resources", innerText=resource, close=True)
	src += tag("xf:instance", attrStr=modelResourcesAttrs,
		innerText=resources, close=True)

	# closing
	src += closing("xf:model") + closing("xh:head")
	return src


def genView(form: Form) -> str:
	viewer = Viewer()
	src = tag("fr:body", attrStr=viewFrBody,
		innerText=form.accept(viewer), close=True)
	src = tag("fr:view", innerText=src, close=True)
	src = tag("xh:body", innerText=src, close=True)
	return src


def gen_xhtml(form: Form) -> str:
	src = tag("xh:html", htmlAttrs)
	src += genModel(form)
	src += genView(form)
	src += closing("xh:html")
	return src


if __name__ == "__main__":
	form = Form()
	src = gen_xhtml(form)
	pyperclip.copy(src)
