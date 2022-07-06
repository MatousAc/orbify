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

GetFTDUsersRes = "https://165.227.16.142.nip.io:8443/ftdproxyrs/users/data.orbeon"

actGenAttrs = {
	"event": "xforms-value-changed xforms-enabled",
	"if": "true()"
}

actResItemAttrs = {
	"class": "fr-itemset-action"
}