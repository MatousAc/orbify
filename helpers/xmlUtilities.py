# functions to help generate XForm's XML
def tag(type: str, attrStr="", attrDict={}, 
	innerText="", close=False, selfClosing=False) -> str:
	# here we piece together the xml tag using the 
	# type and a few optional attributes
	src = f"<{type}"
	if attrStr != "": src +=  f" {attrStr}"
	for attr, val in attrDict.items():
		src += f" {attr}=\"{val}\""
	if selfClosing: src += "/"
	src += ">"
	if innerText == "": return src + "\n"

	# the rest is just for quick inner 
	# text inserts and subsequent closes
	nl = "" if len(innerText) < 30 else "\n"
	if not selfClosing and innerText != "":
		src += f"{nl}{innerText}{nl}"
		if close:
			src += closing(type)
	return src


def closing(type: str) -> str:
	return f"</{type}>\n"
