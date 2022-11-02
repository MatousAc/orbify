# long predefined strings that are used in 
# generating the source code string 

# general
version = "2019.2.2.202003311635 PE"
enlang = 'xml:lang="en"'
hintTag = "<hint/>"

# first xml tag attributes
htmlAttrs = """xmlns:xh="http://www.w3.org/1999/xhtml" 
xmlns:xf="http://www.w3.org/2002/xforms"
xmlns:xs="http://www.w3.org/2001/XMLSchema"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:ev="http://www.w3.org/2001/xml-events"
xmlns:xi="http://www.w3.org/2001/XInclude"
xmlns:xxi="http://orbeon.org/oxf/xml/xinclude"
xmlns:xxf="http://orbeon.org/oxf/xml/xforms"
xmlns:map="http://www.w3.org/2005/xpath-functions/map"
xmlns:array="http://www.w3.org/2005/xpath-functions/array"
xmlns:exf="http://www.exforms.org/exf/1-0"
xmlns:fr="http://orbeon.org/oxf/xml/form-runner"
xmlns:saxon="http://saxon.sf.net/"
xmlns:sql="http://orbeon.org/oxf/xml/sql"
xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:fb="http://orbeon.org/oxf/xml/form-builder"
fr:data-format-version="4.0.0\""""
# model outer tag attributes
modelAttrs = 'id="fr-form-model" xxf:expose-xpath-types="true" xxf:analysis.calculate="true"'
modelDataMapAttrs = 'id="fr-form-instance" xxf:exclude-result-prefixes="#all" xxf:index="id"'
modelBindAttrs = """id="fr-form-binds" ref="instance('fr-form-instance')" readonly="/form/is_form_readonly/text() = 'true'\""""
modelMetaAttrs = 'id="fr-form-metadata" xxf:readonly="true" xxf:exclude-result-prefixes="#all"'
modelAttachAttrs = 'id="fr-form-attachments" xxf:exclude-result-prefixes="#all"'
modelResourcesAttrs = 'xxf:readonly="true" id="fr-form-resources" xxf:exclude-result-prefixes="#all"'
ftdImgAttrs = {
  "filename": "FTD logo Full Color.jpg", 
  "mediatype": "image/jpeg"
}
ftdImgInner = "/fr/service/persistence/crud/orbeon/builder/data/f3b1932efed53c4d9345c74c8205ac6b8da5c91a/a7199ec5951beb7002622bd4456b1063208a8b42.bin"
# bind attributes
bindPhoneAttrs = {
  "xxf:whitespace": "trim",
	"constraint": ". = '' or matches(., '^\+?(\s*\(?\d\D?\s*){10,13}$')",
	"calculate": "if (string-length(replace(., '\D', '')) = 10)&#xA;then replace(replace(., '\D', ''),&#xA;        '(\d{3})(\d{3})(\d{4})', '($1) $2-$3')&#xA;else if (string-length(replace(., '\D', '')) = 11)&#xA;then replace(replace(., '\D', ''),&#xA;        '(\d{1})(\d{3})(\d{3})(\d{4})', '+$1 ($2) $3-$4')&#xA;else if (string-length(replace(., '\D', '')) = 12)&#xA;then replace(replace(., '\D', ''),&#xA;        '(\d{2})(\d{3})(\d{3})(\d{4})', '+$1 ($2) $3-$4')&#xA;else if (string-length(replace(., '\D', '')) = 13)&#xA;then replace(replace(., '\D', ''),&#xA;        '(\d{3})(\d{3})(\d{3})(\d{4})', '+$1 ($2) $3-$4')&#xA;else ."
}
bindLinkAttrs = {
	"xxf:whitespace": "trim",
	"constraint": ". = '' or matches(., '[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}')"
}

# resource attributes
srcFormTextAttrs = 'xmlns:xxbl="http://orbeon.org/oxf/xml/xbl" xmlns:xbl="http://www.w3.org/ns/xbl" xmlns:p="http://www.orbeon.com/oxf/pipeline"'
sourceLine = "&lt;hr/&gt;"
# view attributes
# generals
vfw = 'field-width="natural"'
xxbl = "http://orbeon.org/oxf/xml/xbl"
fbURL = "http://orbeon.org/oxf/xml/form-builder"
xblurl = {
	"xmlns": fbURL,
	"xmlns:xxbl": xxbl
}
# specifics
viewFrBody = 'xmlns:xbl="http://www.w3.org/ns/xbl" xmlns:p="http://www.orbeon.com/oxf/pipeline" xmlns:oxf="http://www.orbeon.com/oxf/processors"'
viewDate = {
	"xmlns:xxbl": xxbl,
	"xmlns:DateSupport": "java:org.orbeon.xbl.DateSupportJava",
	"field-width": "natural"
}

viewNumeric = {
	"xmlns": fbURL,
	"xmlns:xxbl": xxbl,
	"xmlns:NumberSupport": "java:org.orbeon.xbl.NumberSupportJava"
}

viewAttach = {
	"xmlns": fbURL,
	"xmlns:xxbl": xxbl,
	"class": "fr-attachment"
}

viewYesNo = viewSignature = xblurl

viewRadio = {
	"appearance": "full"
}

viewCheckBox = viewRadio

viewCurrency = {
	"xmlns": fbURL,
	"xmlns:xxbl": xxbl,
	"xmlns:NumberSupport": "java:org.orbeon.xbl.NumberSupportJava"
}

viewDatadrop = {
	"appearance": "dropdown"
}

viewRichText = {
	"xmlns:xxbl": xxbl,
	"xmlns:f": "http://orbeon.org/oxf/xml/formatting"
}

viewStaticText = {
	"xmlns:xxbl": xxbl
}

viewImage = {
	"xmlns": fbURL,
	"xmlns:xxbl": xxbl,
	"class": "fr-static-attachment"
}