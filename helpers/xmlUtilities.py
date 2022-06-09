# functions to help generate XForm's XML
def tag(type, attrStr="\b", attrDict={}, innerText="", close=False, selfClosing=False):
	# here we piece together the xml tag using the 
	# type and a few optional attributes
	src = f"<{type} {attrStr}"
	for attr, val in attrDict.items():
		src += f" {attr}=\"{val}\""
	src += "/>\n" if selfClosing else ">\n"
	# this is just for quick inner text inserts 
	# and subsequent closes
	if not selfClosing and innerText != "":
		src += f"{innerText}\n"
		if close:
			src += closing(type)
	return src


def closing(type):
	return f"</{type}>\n"
