import argparse 
import re
from enum import Enum

# fail10 completed
def mapString(text):
    # if match := re.fullmatch('".+"',text, re.DOTALL):
    #     return match.group()[1:-1]
    text = text.strip()
    newString = ''
    index = 1
    while index < len(text):
        char = text[index]

        newString += char
        if char == '"' and not text[index-1] == "\\" :
            break
        
        index +=1 

    if not (text[0] == '"' and newString[-1] == '"' ):
        raise SyntaxError(f'There is no valid string >{text}<')
    
    return newString[0:-1]

def mapValue(text):
    return []

def mapObjectItems(text):
    dictionary = {}
    keyValuePairs = map(lambda s: s.strip(), text.split(","))
    
    for keyValue in keyValuePairs:
        try:
            key, value = keyValue.split(":")
        except:
            raise SyntaxError("Invalid key value pair")
        
        dictionary[mapString(key)] = value
        
        

    return dictionary
    

def mapArrayItems(text):
    array = []
    stringItems = map(lambda s: s.strip(), text.split(","))

    for item in stringItems:
        if item == "":
            raise SyntaxError(f"Extra comma [{text}]")
        
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

    if len(text[index+1:].strip()) > 0:
        raise SyntaxError(f"Unknown token in object mapping > {text[index+1:]} <")

    if numOpennedObjects > 0 or not isThereAnObject:
        raise SyntaxError("There is no valid object or array")

    return {'{': mapObjectItems, '[': mapArrayItems}[openningChar](text[openningIndex+1:closingIndex])


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


    print("Parsed json File:", data, sep="\n")


    jsonFile.close()


if __name__ == '__main__':
    main()