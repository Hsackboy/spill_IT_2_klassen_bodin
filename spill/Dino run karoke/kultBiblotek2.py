def betterInput(variableType:str,inputText:str,errorText="",listLength =1,forventet=[]):
    """Tar inn input og stopper brukeren fra å skrive inn feil datatype

    Args:
        variableType (str): "str","float" eller "int"
        inputText (str): Tekst som står når man spør om innput
        errorText (str, optional): error tekst hvis bruker ikke skriver rett datatype. Defaults to "".
        listLength (int, optional): Lager liste hvis den blir endret fra en. Defaults to 1.

    Returns:
        "liste","str","float" eller "int": returnere iputverdier
    """
    
    willBreakAtEnd = False
    if listLength!=1:
        willBreakAtEnd=True
    if forventet==[]:
        willBreakAtEnd=True
    returnValue=""
    while ((returnValue in forventet) ==False):
        returnValue=""
        if listLength>1:
            returnValue = []
        
        if variableType=="str":
            if listLength==1:
                returnValue=input(inputText)
            else:
                for i in range(listLength):
                    returnValue.append(input(inputText))
        
        if variableType=="int":
            if listLength==1:
                while True:
                    returnValue = input(inputText)
                    if str.isdigit(returnValue):
                        returnValue = int(returnValue)
                        break
                    elif errorText!="":
                        print(errorText)
            else:
                for i in range(listLength):
                    while True:
                        inVal = input(inputText)
                        if str.isdigit(inVal):
                            returnValue.append(int(inVal))
                            break
                        elif errorText!="":
                            print(errorText)
        
        if variableType=="float":
            if listLength==1:
                while True:
                    returnValue = input(inputText)
                    try:
                        returnValue = float(returnValue)
                        break
                    except:
                        if  errorText!="":
                            print(errorText)
                        else:
                            pass
            else:
                for i in range(listLength):
                    while True:
                        inVal = input(inputText)
                        try:
                            inVal = float(inVal)
                            returnValue.append(inVal)
                            break
                        except:
                            if  errorText!="":
                                print(errorText)
                            else:
                                pass
        if willBreakAtEnd:
            break
        if ((returnValue in forventet) ==False):
            print("oops oops, verdien(",returnValue,") var ikke en del av forventet verdiene: ",forventet)
    return returnValue

def print1DList(listIn):
    for i in range(len(listIn)):
        print(i,":",listIn[i])

def print2DList(listIn:list,plass:int)-> None:
    """Tar inn en 2d liste og skriver den ut

    Args:
        listIn (list): liste som skal skrives ut
        plass (int): bestemmer hvor mye plass elementene skal ha i listen ved utskrift
    """
    
    rowNum =-1
    collumAmmount,rowAmount =0,0
    x ="x"
    for rows in listIn:
        if len(rows)>collumAmmount:
            collumAmmount=len(rows)
        rowAmount+=1
    spaceNeeded = len(str(rowAmount))
    print(f"{x:>{spaceNeeded}}",end="")
    for i in range(collumAmmount):
        print(f"{i:>{plass}}",end="")
    print("")
    kolonner=""
    for rows in listIn:
        rowNum+=1
        print(f"{rowNum:>{spaceNeeded}}"  ,end="")
        for value in rows:
            print(f"{value:>{plass}}",end="")
        print("")
    print("")