servInstBodyAttrs = {
  "xmlns:xxbl": "http://orbeon.org/oxf/xml/xbl",
  "xmlns:fbf": "java:org.orbeon.oxf.fb.FormBuilderXPathApi"
}

servInstAttrs = {
  "class": "fr-service",
  "xxf:exclude-result-prefixes": "#all"
}

servSubmitAttrs = {
  "class": "fr-service",
  "method": "get",
  "serialization": "none",
  "mediatype": ""
}

resURL = "{xxf:property('ftd.url')}/ftdproxyrs"

actGenAttrs = {
  "event": "xforms-value-changed xforms-enabled",
  "if": "true()"
}

actResItemAttrs = {
  "class": "fr-itemset-action"
}