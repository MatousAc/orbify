def snake_case(s : str) -> str:
	return s.lower().replace(" ", "_")

def dashcase(s : str) -> str:
	return s.lower().replace(" ", "-")

# here are helper functions that automatically
# generate control names. names are alphanumeric
# with '_' between words. '-' is allowed too
def allowTheseChars(c : str) -> bool:
	return (c.isalnum() 
		or c == "_"
		or c == "-")

def to_control_name(s: str) -> str:
	# remove spaces, make lower, replace w/ '_'
	s = s.strip().lower().replace(" ", "_")
	# removes all but allowed characters
	s = ''.join(filter(allowTheseChars, s))
	return s