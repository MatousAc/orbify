# functions to help generate XForm's XML
def tag(type: str, attrStr="", attrDict={}, innerText="", 
	close=False, selfClosing=False, mt=0, mb=0) -> str:
	# here we piece together the xml tag using the 
	# type and a few optional attributes
	nls = ""
	for i in range(mt): nls += "\n"
	src = f"{nls}<{type}"
	nls = ""
	for i in range(mb): nls += "\n"
	
	if attrStr != "": src +=  f" {attrStr}"
	for attr, val in attrDict.items():
		src += f" {attr}=\"{val}\""
	if selfClosing: src += "/"
	src += ">"
	if innerText == "": return src + nls

	# the rest is just for quick inner 
	# text inserts and subsequent closes
	nl = "" if len(innerText) < 30 else "\n"
	if not selfClosing and innerText != "":
		src += f"{nl}{innerText}"
		if close:
			src += closing(type)
	return src + nls


def closing(type: str) -> str:
	return f"</{type}>\n"
