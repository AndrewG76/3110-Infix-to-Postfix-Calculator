#Gravino, Andrew
#CS3110, Project 1
#4-13-22

#read a user input as a string, 
#use an automaton to translate it into a floating point number 
#(without help from built-in or 3rd party functions), 
#or reject it saying it's not a decimal float number.

#Recognize any decimal floating point literals
#For simplicity, you can assume the input string’s length <=20, and within range 

import sys

def main():
    finalResult = stringProcessing()
    print(finalResult)


def stringProcessing():
    stringInput = input("Please enter your string: ")
    
    rawCharacterList = [] #holds the characters of the original input
    trueCharacterList = [] #holds the characters after it evaluates that a specified character is valid at each part
    powerArray = [] #holds the digits of powers to multiply by for each place in the string input
    suffixFlag = False #will be either "f", "F", "d", "D"
    eFlag = False #will be either "E" or "e"
    signFlag = False #will be either "+" or "-"
    decimalFlag = False #will be "."
    digitFlag = False #will be something from 0-9
    characterIndex = 0 #used as an easy way to iterate through the arrays
    finalValue = 0 #this will be p
    signType = None
    underscoreCounter = 0 #this is used as an offset to fix values like with e and suffixes
    eIndex = 0
    
    for character in stringInput:
        rawCharacterList.append(character)
        
######This segment of the code is dedicated to verifying if the string is valid and populating a new list used for computing a floating value if the conditions are met
    for character in rawCharacterList:
        if digitCheck(character) == True: #we check to see if it is a digit
            if suffixFlag != True: #you can have a digit after everything except the suffix
                trueCharacterList.append(character) #we add it like no problem
                digitFlag = True
                characterIndex += 1
            else:
                print("String Input Rejected.")
                sys.exit()
        if underscoreCheck(character) == True:
            underscoreCounter += 1
            #you can have an underscore after only digits and more underscores
            #we're not appending anything though
            if decimalCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an underscore after a decimal
                print("String Input Rejected.")
                sys.exit()
            if suffixCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an underscore after a suffix
                print("String Input Rejected.")
                sys.exit()
            if signCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an underscore after a sign
                print("String Input Rejected.")
                sys.exit()
            if eCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an underscore after an e
                print("String Input Rejected.")
                sys.exit()
            if underscoreCheck(rawCharacterList[len(rawCharacterList) - 1]) == True: #you cant have an underscore be the last character
                print("String Input Rejected.")
                sys.exit()
            else:
                pass
        if decimalCheck(character) == True: #we check to see if it is a decimal
            if decimalFlag == True: #if we see that there was already a decimal, we reject the string
                print("String Input Rejected.")
                sys.exit()
            if suffixFlag == True: #you cannot have a decimal after the suffix
                print("String Input Rejected.")   
            else:
                decimalFlag = True #if there wasn't a decimal already, we now set the decimal flag to on or True
                trueCharacterList.append(character)
                characterIndex += 1
        if eCheck(character) == True: #we check to see if it is some kind of e
            if eFlag == True: #if e or E was detected prior, then we reject the string
                print("String Input Rejected.")
                sys.exit()
            if digitFlag != True: #there must be some digit first
                print("String Input Rejected.")
                sys.exit()
            if suffixFlag == True: #you cannot have an e after the suffix
                print("String Input Rejected.")
            if signCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an e after a sign
                print("String Input Rejected.")
                sys.exit()
            if digitCheck(rawCharacterList[len(trueCharacterList) + 1 - underscoreCounter]) != True and signCheck(rawCharacterList[len(trueCharacterList) + 1- underscoreCounter]) != True and decimalCheck(rawCharacterList[len(trueCharacterList) + 1 - underscoreCounter]) != True:
                print("String Input Rejected.")
                sys.exit()
            if underscoreCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an e after an underscore
                print("String Input Rejected.")
                sys.exit()
            if eCheck(rawCharacterList[len(rawCharacterList) - 1]) == True: #you cant have an e be the last character
                print("String Input Rejected.")
                sys.exit()
            else:
                trueCharacterList.append("e")
                eFlag = True
                characterIndex += 1
        if signCheck(character) == True: #we check to see if there is some kind of sign character of + or -
            if signFlag == True: #you cannot have a sign if there is already some other sign
                print("String Input Rejected.")
                sys.exit()
            if digitFlag != True: #there must be some digit first
                print("String Input Rejected.")
                sys.exit()
            if digitCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a sign after a digit, only after E
                print("String Input Rejected.")
                sys.exit()
            if suffixFlag == True: #you cannot have a sign after the suffix
                print("String Input Rejected.")
                sys.exit()
            if decimalCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a sign after a decimal
                print("String Input Rejected.")
                sys.exit()
            if digitCheck(rawCharacterList[len(trueCharacterList) + 1]) != True and decimalCheck(rawCharacterList[len(trueCharacterList) + 1]) != True:
                print("String Input Rejected.")
                sys.exit()
            if signCheck(rawCharacterList[len(rawCharacterList) - 1]) == True: #you cant have a sign be the last character
                print("String Input Rejected.")
                sys.exit()
            if underscoreCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a sign after an underscore
                print("String Input Rejected.")
                sys.exit()
            if eCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #for positive and negative signs after E, we want to look at the last character provided in the trueCharacterList is an "e" or "E"
                trueCharacterList.append(character) #if the last character was "e" or "E", then you are allowed to include the plus or negative sign
                signFlag = True #turn the sign flag on to indciate a sign has been used already
                signType = positiveOrNegativeAssign(character)
                characterIndex += 1
            else:
                print("String Input Rejected.")
                sys.exit()
        if suffixCheck(character) == True: #we check to see if there is some kind of suffix character of f, F, d, or D
            if suffixFlag == True: #you cannot have a suffix after the suffix
                print("String Input Rejected.")
                sys.exit()
            if digitFlag != True: #there must be some digit first
                print("String Input Rejected.")
                sys.exit()
            if signCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a suffix after a sign
                print("String Input Rejected.")
                sys.exit()
            if eCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a suffix after e
                print("String Input Rejected.")
                sys.exit()
            if underscoreCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an suffix after an underscore
                print("String Input Rejected.")
                sys.exit()
            if characterIndex == (len(rawCharacterList) - 1) - underscoreCounter:
                suffixFlag = True #we will indicate that this SHOULD be the end but if something else comes in, the suffixFlag is a backup measure to reject the string
            else:
                print("String Input Rejected.")
                sys.exit()
        if digitCheck(character) != True and decimalCheck(character) != True and eCheck(character) != True and signCheck(character) != True and suffixCheck(character) != True and underscoreCheck(character) != True:
            print("String Input Rejected.")
            sys.exit()
            
    if decimalFlag == False and suffixFlag == True: #if there is no decimal but the letter f or d is spotted at the end, we convert that integer into a float and make the input valid by placing a decimal
        if eFlag == True: #on the offchance the person is writing maybe 1e-9d, that is valid and our fix doesn't work
            eIndex = trueCharacterList.index("e")
            #we would put the decimal right before where e is 
            #it converts maybe 1e1f into 1.e1f which is also valid and helps with calculations
            trueCharacterList.insert(eIndex, ".")
        else:
            trueCharacterList.append(".") 
            
        decimalFlag = True
            
            
    
#####This segment of the code is dedicated to combining all the characters together now to create a floating point value

#set the characterIndex to 0 here at first and we'll be using them again for the second part when it comes to calculating where is what
    characterIndex = 0 #used as an easy way to iterate through the arrays
    powerArray = [0]*len(trueCharacterList)
    powerIndex = 0
    ePower = 0

#if you notice the decimal anywhere in the list, then you take note of its index value and the absolute distance from the integer you're looking at it like "the power"
    if decimalFlag == True:
        powerIndex = trueCharacterList.index(".")
    elif decimalFlag == False and eFlag == True:
        pass
    else:
        print("String Input Rejected.v")
        sys.exit()
        
    if eFlag == True:
        eIndex = trueCharacterList.index("e")
        
#for example the trueCharacterList looks like: 1, 2, 3, ., 4, 5
#the corresponding powerArray would look like: 2, 1, 0, null, -1, -2
#you could use the digit checks again and if it's true, then you multiply the digit in trueCharacterList by 10 to the power of the value sitting in the corresponding index

    for character in trueCharacterList: #this is to first populate the powerArray before usage
        if characterIndex < powerIndex:
            powerArray[characterIndex] = powerIndex - characterIndex - 1
        if characterIndex > powerIndex:
            powerArray[characterIndex] = -(characterIndex - powerIndex)
        characterIndex += 1
        
    characterIndex = 0
    if eFlag == True:
        powerIndex = eIndex
        for character in trueCharacterList: #this second loop will overwrite the power array but only if it detected an e earlier
            if decimalFlag == True:
                if characterIndex > eIndex:
                    powerArray[characterIndex] = (((characterIndex - len(trueCharacterList)) + 1) * -1)
            if decimalFlag == False:
                if characterIndex < eIndex:
                    powerArray[characterIndex] = powerIndex - characterIndex - 1
                if characterIndex > eIndex:
                    powerArray[characterIndex] = (((characterIndex - len(trueCharacterList)) + 1) * -1)
            characterIndex += 1

    characterIndex = 0
    
    #DO NOT TOUCH THIS IT'S PERFECT
    
    if eFlag == True:
        for character in trueCharacterList:
            if trueCharacterList[characterIndex].isdigit() and characterIndex < eIndex:
                finalValue += int(trueCharacterList[characterIndex]) * pow(10, powerArray[characterIndex])
            if signType == False: #this means the signis negative
                if trueCharacterList[characterIndex].isdigit() and characterIndex > eIndex:
                    ePower -= int(trueCharacterList[characterIndex]) * pow(10, powerArray[characterIndex])
            else: #this is the condition where the sign is positve or there is no sign at all
                if trueCharacterList[characterIndex].isdigit() and characterIndex > eIndex:
                    ePower += int(trueCharacterList[characterIndex]) * pow(10, powerArray[characterIndex])
            characterIndex += 1
        finalValue *= pow(10, ePower)
    if eFlag == False:
        for character in trueCharacterList:
            if trueCharacterList[characterIndex].isdigit():
                finalValue += int(trueCharacterList[characterIndex]) * pow(10, powerArray[characterIndex])
            characterIndex += 1
            
    #for character in trueCharacterList
    
    finalValue = float(finalValue) #there is no double in python so we will only ever be handling floating-point literals regardless of symbols used like f or d
    
    print(powerArray)
    print(rawCharacterList)
    print(trueCharacterList)
    
    return finalValue 

#use a flag to determine when the powers are negative, some kind of thing to indicate like the decimalFlag
#if the decimal flag is true, then all powers found from the absolute distance difference become negative
#if there is no decimal, then you technically put the decimal at the end
#if there is an f or a d, then the decimal would be in that location technically if and only if there is no decimal beforehand
#if there is an e, then there is no associated power at the corresponding index location
#if there is a decimal before the e, then all is fine and dandy with the same system
#because we're doing the powers based on distance from the decimal, any time that we encounter the letter e, the powers of the values after e start reset and are not tied to anything before the e
#we want to basically do the decimal system again and place it at the end of the values after e
#because this is the case, we do distance from the decimal after e as the power once again
#and because we're gonna be setting a new "decimal" location, we have to turn the original decimalFlag off and turn it on at the end of the e values
#we then have the corresponding values in the powerArray only holding power values between the e and the new "decimal" location
#if there is NO decimal found before the e, the e's index will be used as the new "decimal location"
#for example, the trueCharacterList looks like: 1, 2, 3, e, 4, 5
#the corresponding powerArray would look like: 2, 1, 0, null or something, 1, 0
#trueCharacterList = [1, 2, 3, ., 4, 5, e, 6, 7]
#powerArray = [-2, -1, 0, null or something, -1, -2, null or something, 1, 0]
#but because we have to verify the power's own sign like positive or negative, we can use that digit's placement as the other spot to stop at too
#tCL = [1, 2, 3, ., 4, 5, e, +, 6, 7]
#pA = [-2, -1, 0, null, -1, -2, null, null, 1, 0]
#tCL = [1, 2, 3, ., 4, 5, e, 6, 7]
#pA = [-2, -1, 0, null, -1, -2, null, 1, 0]
#these 2 are supposed to be virtually identical is the main gist for if they include the plus sign or not after the e
#tCL = [1, 2, 3, ., 4, 5, e, -, 6, 7]
#pa = [-2. -1, 0, null, -1, -2, null, null, 1, 0]
#we verify if we need to use something's power if and only if it meets the requirement that it is a digit 


#####this section of the code just serves to check if the character we're looking at is a digit, a decimal, an e, a sign, or a suffix
def digitCheck(inputCharacter):
    if inputCharacter == "0" or inputCharacter == "1" or inputCharacter == "2" or inputCharacter == "3" or inputCharacter == "4" or inputCharacter == "5" or inputCharacter == "6" or inputCharacter == "7" or inputCharacter == "8" or inputCharacter == "9":
        return True
    
def underscoreCheck(inputCharacter):
    if inputCharacter == "_":
        return True
    
def decimalCheck(inputCharacter):
    if inputCharacter == ".":
        return True
    
def eCheck(inputCharacter):
    if inputCharacter == "e" or inputCharacter == "E":
        return True
    
def signCheck(inputCharacter):
    if inputCharacter == "+" or inputCharacter == "-":
        return True
    
def positiveOrNegativeAssign(inputCharacter):
    if inputCharacter == "+":
        return True
    if inputCharacter == "-":
        return False
    
def suffixCheck(inputCharacter):
    if inputCharacter == "f" or inputCharacter == "F" or inputCharacter == "d" or inputCharacter == "D":
        return True
    
main()