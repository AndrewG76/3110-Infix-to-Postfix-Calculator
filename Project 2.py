#Gravino, Andrew
#CS3110, Project 2
#5-4-22

#evaluate floating point expreessions whose operands and values are floating-point numbers
#essentially just adding to project 1 by adding *, /, +, -, parentheses, and white space

import sys

def main(): #we're gonna be taking in a string expression from the user, 
    rawListOfEverything = []
    stringListOfEverything = []

    userInput = input("Please enter an expression: ")
    
    userInput = userInput.replace(" ", "") #we will first and remove the whitespaces since they mean literally nothing
    userInput = userInput.replace("E", "e") #clarity sake for making code easier later
    
    floatList = expressionSplitter(userInput) #first stage, break the expression into pieces
    
    convertedList = floatListConversion(floatList) #second stage, run project 1 on all the expressions
    
    for item in convertedList: #third stage, convert them all to strings
        rawListOfEverything.append(item)
    for item in rawListOfEverything:
        stringListOfEverything.append(str(item))
    
    finalString = "".join(stringListOfEverything) #fourth stage, join all the strings into one giant string
    
    return finalString
    
    
def floatListConversion(passedList):
    rawListOfItems = []
    convertedListOfItems = []
    itemIndex = 0
    
    for item in passedList:
        rawListOfItems.append(item)
    
    for item in rawListOfItems:
        if item != "+" and item != "-" and item != "*" and item != "/" and item != "(" and item != ")":
            convertedListOfItems.append(floatStringProcessing(item))
        else:
            convertedListOfItems.append(item)
        itemIndex += 1
            
    return convertedListOfItems

def expressionSplitter(passedString):
    uneditedCharacterList = []
    startIndex = 0
    endIndex = 0
    currentIndex = 0 #this will be the index of character in passedString
    characterIndex = 0 #this will be the index within each floating point value 
    listOfFloatsAndOperands = []
    operandFound = ""
    floatingPointValueConstruction = []
    floatingPointValue = ""
    
    for character in passedString:
        uneditedCharacterList.append(character)
    
    for character in uneditedCharacterList: #we check the first character, characterIndex is 0 | we check the second character, characterIndex is 1          
        if (character == "+" or character == "-" or character == "*" or character == "/" or character == "(" or character == ")"):
            #if we notice an operand, then we want to apppend to the list of floats the floating point value before it
            if uneditedCharacterList[currentIndex - 1] == "e": #if we notice the letter e before the stuff though, we just skip this time
                endIndex += 1
            else:
                operandFound = character
                endIndex = currentIndex #currentIndex only increments after finishing this iteration so when we do this, currentIndex is currently the index before the item we are looking at
                for i in range(startIndex, endIndex):
                    floatingPointValueConstruction.append(uneditedCharacterList[i]) #we start off with an empty construction list
                    #let's say we have 123.4+5.6
                    #it appends 1, then 2, then 3, then ., then 4
                floatingPointValue = "".join(floatingPointValueConstruction)
                listOfFloatsAndOperands.append(floatingPointValue)
                listOfFloatsAndOperands.append(operandFound)
                floatingPointValueConstruction = [] #then when we're done, we clear it out again and wait for it append 5, then append ., and then append 6
            
                startIndex = endIndex + 1
            
        currentIndex += 1
        characterIndex += 1
        
    for i in range(startIndex, len(uneditedCharacterList) - 1): #this makes sure to print out the last floating point value
        floatingPointValueConstruction.append(uneditedCharacterList[i])
    floatingPointValue = "".join(floatingPointValueConstruction)
    listOfFloatsAndOperands.append(floatingPointValue)
    
    listOfFloatsAndOperands = list(filter(("").__ne__,listOfFloatsAndOperands))
    
    return listOfFloatsAndOperands
            

def floatStringProcessing(passedString): #this function will be used on every single floating point value in the list
    stringInput = passedString
    
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
                print("String Input Rejected.a")
                sys.exit()
        if underscoreCheck(character) == True:
            underscoreCounter += 1
            #you can have an underscore after only digits and more underscores
            #we're not appending anything though
            if decimalCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an underscore after a decimal
                print("String Input Rejected.b")
                sys.exit()
            if suffixCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an underscore after a suffix
                print("String Input Rejected.c")
                sys.exit()
            if signCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an underscore after a sign
                print("String Input Rejected.d")
                sys.exit()
            if eCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an underscore after an e
                print("String Input Rejected.e")
                sys.exit()
            if underscoreCheck(rawCharacterList[len(rawCharacterList) - 1]) == True: #you cant have an underscore be the last character
                print("String Input Rejected.f")
                sys.exit()
            else:
                pass
        if decimalCheck(character) == True: #we check to see if it is a decimal
            if decimalFlag == True: #if we see that there was already a decimal, we reject the string
                print("String Input Rejected.g")
                sys.exit()
            if suffixFlag == True: #you cannot have a decimal after the suffix
                print("String Input Rejected.h")   
            else:
                decimalFlag = True #if there wasn't a decimal already, we now set the decimal flag to on or True
                trueCharacterList.append(character)
                characterIndex += 1
        if eCheck(character) == True: #we check to see if it is some kind of e
            if eFlag == True: #if e or E was detected prior, then we reject the string
                print("String Input Rejected.i")
                sys.exit()
            if digitFlag != True: #there must be some digit first
                print("String Input Rejected.j")
                sys.exit()
            if suffixFlag == True: #you cannot have an e after the suffix
                print("String Input Rejected.k")
            if signCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an e after a sign
                print("String Input Rejected.l")
                sys.exit()
            if digitCheck(rawCharacterList[len(trueCharacterList) + 1 - underscoreCounter]) != True and signCheck(rawCharacterList[len(trueCharacterList) + 1- underscoreCounter]) != True and decimalCheck(rawCharacterList[len(trueCharacterList) + 1 - underscoreCounter]) != True:
                print("String Input Rejected.m")
                sys.exit()
            if underscoreCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an e after an underscore
                print("String Input Rejected.n")
                sys.exit()
            if eCheck(rawCharacterList[len(rawCharacterList) - 1]) == True: #you cant have an e be the last character
                print("String Input Rejected.o")
                sys.exit()
            else:
                trueCharacterList.append("e")
                eFlag = True
                characterIndex += 1
        if signCheck(character) == True: #we check to see if there is some kind of sign character of + or -
            if signFlag == True: #you cannot have a sign if there is already some other sign
                print("String Input Rejected.p")
                sys.exit()
            if digitFlag != True: #there must be some digit first
                print("String Input Rejected.q")
                sys.exit()
            if digitCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a sign after a digit, only after E
                print("String Input Rejected.r")
                sys.exit()
            if suffixFlag == True: #you cannot have a sign after the suffix
                print("String Input Rejected.s")
                sys.exit()
            if decimalCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a sign after a decimal
                print("String Input Rejected.t")
                sys.exit()
            if digitCheck(rawCharacterList[len(trueCharacterList) + 1]) != True and decimalCheck(rawCharacterList[len(trueCharacterList) + 1]) != True:
                print("String Input Rejected.u")
                sys.exit()
            if signCheck(rawCharacterList[len(rawCharacterList) - 1]) == True: #you cant have a sign be the last character
                print("String Input Rejected.v")
                sys.exit()
            if underscoreCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a sign after an underscore
                print("String Input Rejected.w")
                sys.exit()
            if eCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #for positive and negative signs after E, we want to look at the last character provided in the trueCharacterList is an "e" or "E"
                trueCharacterList.append(character) #if the last character was "e" or "E", then you are allowed to include the plus or negative sign
                signFlag = True #turn the sign flag on to indciate a sign has been used already
                signType = positiveOrNegativeAssign(character)
                characterIndex += 1
            else:
                print("String Input Rejected.x")
                sys.exit()
        if suffixCheck(character) == True: #we check to see if there is some kind of suffix character of f, F, d, or D
            if suffixFlag == True: #you cannot have a suffix after the suffix
                print("String Input Rejected.y")
                sys.exit()
            if digitFlag != True: #there must be some digit first
                print("String Input Rejected.z")
                sys.exit()
            if signCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a suffix after a sign
                print("String Input Rejected.1")
                sys.exit()
            if eCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have a suffix after e
                print("String Input Rejected.2")
                sys.exit()
            if underscoreCheck(trueCharacterList[len(trueCharacterList) - 1]) == True: #you cannot have an suffix after an underscore
                print("String Input Rejected.3")
                sys.exit()
            if characterIndex == (len(rawCharacterList) - 1) - underscoreCounter:
                suffixFlag = True #we will indicate that this SHOULD be the end but if something else comes in, the suffixFlag is a backup measure to reject the string
            else:
                print("String Input Rejected.4")
                sys.exit()
        if digitCheck(character) != True and decimalCheck(character) != True and eCheck(character) != True and signCheck(character) != True and suffixCheck(character) != True and underscoreCheck(character) != True:
            print("String Input Rejected.5")
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
        print("String Input Rejected.6")
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
    
########################################################
#After this segment is using an infix to postfix algorithm found online at https://codereview.stackexchange.com/questions/190101/expression-calculator-in-python
#Proper credit will be provided in the readme
########################################################
    
#Whenever is_number(x) exists, it is checking to see if x is a number, obviously.
def is_number(item):
    try:
        float(item)
        return True
    except ValueError:
        return False


def set_up_list(passedString):
    #First part gets string and deletes whitespace
    astring = passedString
    print(astring)
    astring = astring.replace(" ", "")
    #Next it will check if there are any unsupported characters in the string
    for item in astring:
        if item not in ["0", "1", "2", "3" , "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", ".", "(", ")"]:
            print ("Unsupported Character: " + item)
            sys.exit()
    #Then it creates the list and adds each individual character to the list
    a_list = []
    for item in astring:
        a_list.append(item)
    count = 0
    #Finally it combines individual numbers into actual numbers based on user input
    while count < len(a_list) - 1:
        if is_number(a_list[count]) and a_list[count + 1] == "(":
            print ("Program does not accept parentheses directly after number, must have operator in between.")
            sys.exit()
        if is_number(a_list[count]) and is_number(a_list[count + 1]):
            a_list[count] += a_list[count + 1]
            del a_list[count + 1]
        elif is_number(a_list[count]) and a_list[count + 1] == ".":
            try:
                x = a_list[count+2]
            except IndexError:
                print ("Your formatting is off somehow.")
                sys.exit()
            if is_number(a_list[count + 2]):
                a_list[count] += a_list[count + 1] + a_list[count + 2]
                del a_list[count + 2]
                del a_list[count + 1]
        else:
            count += 1
    return a_list


def perform_operation(n1, operand, n2):
    if operand == "+":
        return str(float(n1) + float(n2))
    elif operand == "-":
        return str(float(n1) - float(n2))
    elif operand == "*":
        return str(float(n1) * float(n2))
    elif operand == "/":
        try:
            n = str(float(n1) / float(n2))
            return n
        except ZeroDivisionError:
            print ("You tried to divide by 0.")
            print ("Just for that I am going to terminate myself")
            sys.exit()

#these next 5 lines are the only thing i changed about this code
stringToBeUsed = main() #fifth stage, perform the calculations
print("Your submitted expression was valid!")
print("Before proceeding with calculation, here is the converted equation:")

expression = set_up_list(stringToBeUsed)
emergency_count = 0
#Makes code shorter, short for parentheses
P = ["(", ")"]
#If the length of the list is 1, there is only 1 number, meaning an answer has been reached.
while len(expression) != 1:
    #If there are parentheses around a single list item, the list item is obviously just a number, eliminate parentheses
    #Will check to see if the first parentheses exists first so that it does not throw an index error
    count = 0
    while count < len(expression) - 1:
        if expression[count] == "(":
            if expression[count + 2] == ")":
                del expression[count + 2]
                del expression[count]
        count += 1
    #After that is done, it will multiply and divide what it can
    count = 0
    while count < len(expression) - 1:
        if expression[count] in ["*", "/"] and not (expression[count+1] in P or expression[count-1] in P):
            expression[count - 1] = perform_operation(expression[count - 1], expression[count], expression[count + 1])
            del expression[count + 1]
            del expression[count]
        count += 1
    #Then it will add and subtact what it can
    count = 0
    while count < len(expression) - 1:
        if expression[count] in ["+", "-"] and not (expression[count+1] in P or expression[count-1] in P):
            expression[count - 1] = perform_operation(expression[count - 1], expression[count], expression[count + 1])
            del expression[count + 1]
            del expression[count]
        count += 1
    #The steps will repeat until only one character is left. Operations that fail will be stopped by emergency count.
    emergency_count += 1
    if emergency_count >= 1000:
        print ("Operation was too long or was bugged")
        sys.exit()

print (float(expression[0]))
