import json

def parseJSON():
    return json.load(open("examples/newHire.json"))


if __name__ == "__main__":
    form = parseJSON()
    print(form)