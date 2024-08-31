import argparse 
import re

class Parser:
    openAndClosedRelationship = {
        "{": "}",
        '"': '"',
        "[" : "]"
    }

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
    numbers = ["0","1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "e", "E", "-", "^", "/"]
    plainText = "afsd"
    symbolTable = []
    tokens = []
    parsedDictionary = {}

    def __init__(self, plainText) -> None:
        self.plainText = plainText.strip()
        if not ( self.plainText[0] == "{" and self.plainText[len(self.plainText) - 1] == "}"):
            raise SyntaxError("There is not valid json in this file")
        
        self.plainText = self.plainText[1:-1]

        

    def __str__(self) -> str:
        return f"ParserObjectPlainText: {self.plainText}"
    
    def parse(self) -> dict:
       
        self.tokens = self.mapTokens(self.plainText)
        self.mapKeyValueItems()

        return self.parsedDictionary
    
    def lookForClosedCharacterIndex(self,text, startIndex ) -> int:
        openChar = text[startIndex]
        closedTarget = self.openAndClosedRelationship[openChar]
        numOpenedChars = 0

        index = startIndex
        while index != len(text)-1:
            
            char = text[index]
            if char == openChar:
                numOpenedChars += 1
            if char == closedTarget:
               
                numOpenedChars -= 1
            
            if numOpenedChars == 0:
                return index + 1
            
            index +=1 

        raise SyntaxError("Invalid closed character or it does not exist")
    
    def lookForStringClosedCharacterIndex(self, text, startIndex)->int:
        index = startIndex + 1
        while index != len(text)-1:
            char = text[index]
            
            if char == '"':
                return index
            index +=1 
            
        raise SyntaxError("Invalid string closed character or it does not exist")
    
    def lookForNumberAreaEndIndex(self,text, startIndex) -> int:
        for index in range(startIndex + 1, len(text)):
            char = text[index]
            if not char in self.numbers:
                return index
            
        raise SyntaxError("Invalid number character or there is a problem with the program")

    def parseType(self, value):
        if value[0] == '"' and value[len(value)-1] == '"':
            return value[1:-1]

        if value in self.specialWordsCovertionTable.keys():
            return self.specialWordsCovertionTable[value]
        
        if re.fullmatch(r"\d+", value):
            return int(value)
        
        if value[0] == "[" and value[len(value)-1] == ']':
            value = value[1:-1]
            arrayTokens = self.mapTokens(value)
            return list(map(lambda d: self.parseType(d), arrayTokens))
        
        if value[0] == "{" and value[len(value)-1] == '}':
            return Parser(value).parse()

        return value

    def mapKeyValueItems(self)-> None: 
        index = 0
        lastIndex = len(self.tokens)
        while index != lastIndex:
            token = self.tokens[index]
            if token == ":":
                key = self.tokens[index - 1]
                value = self.tokens[index + 1]
                self.parsedDictionary[self.parseType(key)] = self.parseType(value)

            index+=1 


        return 


    def mapTokens(self, text) -> None:
        index = 0
        lastIndex = len(text)-1
        tokens = []

        while index <= lastIndex:
            char = text[index]

            if char in ['{', "["]:
                endIndex = self.lookForClosedCharacterIndex(text, index)

                tokens.append(text[index:endIndex])

                index = endIndex
            elif char == '"':
                endIndex = self.lookForStringClosedCharacterIndex(text, index)
                
                tokens.append(text[index:endIndex+1])

                index = endIndex

            elif char in [ ":", ","]:
                tokens.append(char)
            elif char in self.specialWords.keys():
                specialWord = self.specialWords[char]
                stimatedEndIndex = index+len(specialWord)
                if not(specialWord == text[index:stimatedEndIndex]):
                    raise SyntaxError(f"Invalid Special Word in char with index {index}")

                tokens.append(specialWord)
                index = stimatedEndIndex-1
            elif char in self.numbers:
                endIndex = self.lookForNumberAreaEndIndex(text, index)
            
                tokens.append(text[index:endIndex])

                index = endIndex

            index += 1

      
        return tokens

        
        


def main():
    parser = argparse.ArgumentParser(prog="json parser", description="A json parser");
    parser.add_argument("fileName");


    try: 
        jsonFile =  open(parser.parse_args().fileName, "r")
    except:
        print("The given file is not in this directory or does not exist")
        return

    data = Parser(jsonFile.read()).parse()

    print("Parsed dictionary:", data, sep="\n")


    jsonFile.close()



  
     



if __name__ == '__main__':
    main()