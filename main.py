import argparse 
import re

specialWords = {
        "t":"true", 
        "f":"false",
        "n": "null"
    }
specialWordsCovertionTable = {
    "true": True, 
    "false": False,
    "null": None
}

def main():
    parser = argparse.ArgumentParser(prog="json parser", description="A json parser");
    parser.add_argument("fileName");


    try: 
        jsonFile =  open(parser.parse_args().fileName, "r")
    except:
        print("The given file is not in this directory or does not exist")
        return

    data = converTojsonFromText(jsonFile.read())


    print("Parsed dictionary:", data, sep="\n")


    jsonFile.close()

def lookForLastIndexOfString(rawText, startIndex):  
    index = startIndex + 1

    while index <= len(rawText)-1:
        char = rawText[index]
        index+=1

        if char == '"':
            return index
     
        

def lookForLastIndexOfNestableToken(rawText, startIndex):
    openningChar = rawText[startIndex]
    closingChar =  {'{':'}','[':']'}[openningChar]
    index = startIndex
    numOpennedChars = 0

    while index <= len(rawText)-1:
        char = rawText[index]
        if char == openningChar:
            numOpennedChars += 1
        elif char == closingChar:
            numOpennedChars -= 1
        
        index+=1

        if numOpennedChars == 0:
            return index

        

    
    raise SyntaxError("Invalid string closed character or it does not exist")

        
def extractTokens(rawText):
    tokens = []
    index = 0
    while index <= len(rawText)-1:
        char = rawText[index]
        
        if char in ['{', "["]:
            lastIndex = lookForLastIndexOfNestableToken(rawText, index)
            tokens.append(rawText[index:lastIndex])
            index = lastIndex
        elif char in ['"']:
            lastIndex = lookForLastIndexOfString(rawText, index)
            tokens.append(rawText[index:lastIndex])
            index = lastIndex - 1
        elif char in [":"]:
            tokens.append(char)
        elif char in specialWords.keys():
            specialWord = specialWords[char]
            stimatedEndIndex = index+len(specialWord)
            if not(specialWord == rawText[index:stimatedEndIndex]):
                raise SyntaxError(f"Invalid Special Word in char with index {index}")

            tokens.append(specialWord)
            index = stimatedEndIndex

        elif number := re.search(r"^-?\d+(\.\d+)?", rawText[index:]):
            stringNumber = number.group()
            tokens.append(stringNumber)
            index += len(stringNumber)

        index+=1


    return tokens

def mapDictionaryFromTokens(tokens):
    dictionary = {}
    index = 0
    lastIndex = len(tokens) - 1
    while index <= lastIndex:
        token = tokens[index]
        if token == ":":
            key = tokens[index - 1]
            value = tokens[index + 1]
            dictionary[parseType(key)] = parseType(value)

        index+=1 

    return dictionary

def parseType(text):
    if text[0] == '"' and text[len(text)-1] == '"':
        return text[1:-1]
    
    if text in specialWordsCovertionTable.keys():
        return specialWordsCovertionTable[text]
    
    if number := re.search(r"^-?\d+(\.\d+)?", text):
        number = number.group()
        return float(number)  if '.' in number  else int(number)

    if text[0] == "[" and text[len(text)-1] == ']':
        text = text[1:-1]
        arrayTokens = extractTokens(text)
        return list(map(lambda d: parseType(d), arrayTokens))

    if text[0] == "{" and text[len(text)-1] == '}':
        return converTojsonFromText(text)
         

    return text

def converTojsonFromText(rawText):
  
    return mapDictionaryFromTokens(extractTokens(rawText[1:-1]))
     



if __name__ == '__main__':
    main()