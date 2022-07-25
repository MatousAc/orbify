# makes a string into snake_case
def snake_case(s : str) -> str:
	return s.lower().replace(" ", "_")

# here are helper functions that automatically
# generate control names. names are alphanumeric
# with '_' between words. '-' is allowed too
def allowCharsControl(c : str) -> bool:
	return (c.isalnum() 
		or c == "_"
		or c == "-")

def to_control_name(s: str) -> str:
	# remove spaces, make lower, replace w/ '_'
	s = s.strip().lower().replace(" ", "_")
	# removes all but allowed characters
	s = ''.join(filter(allowCharsControl, s))
	# collapse weird cases of whitespace
	s = s.replace("_-", "_").replace("-_", "_")
	s = s.replace("__", "_").replace("__", "_")
	return s

def allowCharsDashcase(c : str) -> bool:
	return (c.isalnum() 
		or c == "_"
		or c == "-"
		or c == "/"
		or c == ";"
		or c == "&")

# does the same except with dashes (values)
def dashcase(s : str) -> str:
	s = s.strip().lower().replace(" ", "-")
	s = ''.join(filter(allowCharsDashcase, s))
	s = s.replace("--", "-").replace("--", "-")
	return s
# FIXME the above two are painfully similar

# this helper function determines whether 
# a given radio button can be a boolean data type
def isYesNo(choices: dict) -> bool:
	if len(choices) != 2: return False # duh
	labels = [ # get our labels
		choices[0]["Label"].lower(),
		choices[1]["Label"].lower()
	] # now match up either yes/no or true/false
	if ("yes" in labels and "no" in labels): return True
	if ("true" in labels and "false" in labels): return True
	return False # default

# determines if an image element is a generic FTD logo
def isFTDImage(item):
	txt = item["properties"]["imageFile"]["text"].lower()
	return "ftd logo" in txt

# determines if a text field should be a phone number field
def isPhone(item):
	lbl = item["Label"].lower().strip().strip(":")
	return (
		(lbl in ["phone", "phone #", "employee number",
           "employee #", "cell #"]) or
		("phone" in lbl and "area code" not in lbl) or
		("cell phone" in lbl) or
		("us phone" in lbl) or
		("home phone" in lbl) or
		("mobile phone" in lbl) or
		("work phone" in lbl) or
		("international phone" in lbl)
	)

# this function collapses a list of choice 
# dictionaries into a single choice dictionary
def choiceDict(choiceList: list) -> dict:
	choices = {}
	for choice in choiceList:
		l = str(choice["Label"]).replace("&", "&amp;")
		choices[l] = dashcase(l) # values are not just label
		# choices[l] = l # value of label is label (can't do this)
	return choices

# converts a string of numbers into a string of letters
def id2control(id: int) -> str:
	divisor = 26
	name = ""
	while id > 100:
		name += chr(id % divisor + 97)
		id //= 10
	return name

# removes formatting tags from text that would be
# misinterpreted as XML
# also downsizes headings
def staticTextScrub(text: str) -> str:
	text = text.replace("<", "&lt;").replace(">", "&gt;")
	# at this point we replace tabs with ' ' because this works 🤷‍♂️
	text = text.replace("&nbsp;", " ")
	text = text.replace("&ldquo;", "\"")
	text = text.replace("&rdquo;", "\"")
	text = text.replace("&lsquo;", "'")
	text = text.replace("&rsquo;", "'")
	text = text.replace("&hellip;", "...")
	# replace with doubled-up ampersand encoding:
	# one for ampersand preservation while copy-pasting, 
	# and one for ampersand representation in XML
	text = text.replace(" & ", " &amp;amp; ")
	# heading shrink
	text = text.replace("h5","h6").replace("h4","h5")
	text = text.replace("h3","h4").replace("h2","h3")
	text = text.replace("h1","h2")
	return text

def extractJSON(text: str) -> str:
	if text[0] == '[': return text
	startStr = "code  View JSON"
	start = text.find(startStr) + len(startStr)
	return text[start:]

def spaceItem():
  return {
    "QuestionType": "BlankSpace",
    "displayName": "",
    "Label": "",
    "show": True,
    "type": "FormTool_Type"
	}