import argparse 
import re

# fail2 completed

def mapObjectKeys(text):
    dictionary = {}
    keysValuePairs = map(lambda s: s.strip(), text.split(","))


    return list(keysValuePairs)
    

def mapArrayItems(text):
    array = []
    stringItems = map(lambda s: s.strip(), text.split(","))

    for item in stringItems:
        if item == "":
            raise SyntaxError("Extra comma")
        

        array.append(item)

    return array
    

def lookForObject(text):
    index = 0
    numOpennedObjects = 0
    isThereAnObject = False
    openningChar = None 
    closingChar = None 
    openningIndex = None
    closingIndex = None

    while index < len(text):
        char = text[index]

        if char in ["{", "["] and not( openningChar and closingChar):
            openningChar =  char 
            openningIndex = index
            closingChar =  {'{':'}','[':']'}[openningChar]


        if openningChar and  char == openningChar:
            numOpennedObjects += 1
            isThereAnObject = True
        elif closingChar and char == closingChar:
            numOpennedObjects -= 1

        if isThereAnObject and numOpennedObjects == 0:
            closingIndex = index
            break

        index+=1

    if numOpennedObjects > 0 or not isThereAnObject:
        raise SyntaxError("There is no valid object or array")

    return {'{': mapObjectKeys, '[': mapArrayItems}[openningChar](text[openningIndex+1:closingIndex])


def converJsonTextToDictionary(text):

        

    return lookForObject(text)


def main():
    parser = argparse.ArgumentParser(prog="json parser", description="A json parser");
    parser.add_argument("fileName");


    try: 
        jsonFile =  open(parser.parse_args().fileName, "r")
    except:
        print("The given file is not in this directory or does not exist")
        return

    data = converJsonTextToDictionary(jsonFile.read())


    print("Parsed dictionary:", data, sep="\n")


    jsonFile.close()


if __name__ == '__main__':
    main()