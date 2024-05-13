from kultBiblotek2 import *
import csv
import json

def lesJson(filbane,encoding="utf-8",skrivUt=False):
    val=""
    with open(filbane, encoding=encoding) as fil:
        val= json.load(fil)

    if skrivUt:
        data_formatert = json.dumps(val, indent=2)
        print(data_formatert)

    return val
def skrivTilNyFil(filbane, tekst,safe=True):
    if safe:
        try:
            with open(filbane, "a") as fil:
                tekst+"\n"
                fil.write(tekst)
            print("-"*20)
            print("advarsel, fil finnes allerde, safe er på. Skriver på filen")
            print("-"*20)
        except:
            with open(filbane, "w") as fil:
                fil.write(tekst)
    else:
        with open(filbane, "w") as fil:
            fil.write(tekst)
        


def endreFil(filbane, appendTekst):
    with open(filbane, "a") as fil:
        fil.write(appendTekst)


def lesHelFil(filbane, skrivUt=False, encoding="utf-8"):
    innhold = ""
    with open(filbane, encoding=encoding) as fil:
        innhold = fil.read()

    if skrivUt == False:
        return innhold
    print(innhold)


def lesLinjer(filbane, antallLinjer=0, skrivUt=False, encoding="utf-8", strip=True):
    innhold = []

    with open(filbane, encoding=encoding) as fil:
        # print(len(fil))
        count = 1
        for line in fil:
            if strip:
                innhold.append(line.rstrip())
            else:
                innhold.append(line)

            if count >= antallLinjer and antallLinjer != 0:
                break
            count += 1

    if skrivUt == False:
        return innhold
    for i in range(len(innhold)):
        print(i, ":", innhold[i])


def undersookFil(filbane):
    semikolonCount = 0
    kommaCount = 0

    print("-" * 20)
    print("velkommen til håkons undersøking av fil")
    print("")
    print("Fil:")
    print("-" * 20)
    lesLinjer(filbane, antallLinjer=4, skrivUt=True, strip=True)
    print("-" * 20)
    filSample = lesLinjer(filbane, antallLinjer=20, skrivUt=False, strip=True)
    for linje in filSample:
        if ";" in linje:
            semikolonCount += 1
        if "," in linje:
            kommaCount += 1

    kommaDiff = abs(1 - (kommaCount / len(filSample)))
    semikolonDiff = abs(1 - (semikolonCount / len(filSample)))
    prediktion = ""
    if kommaDiff > semikolonDiff:
        prediktion = ";"

    if kommaDiff < semikolonDiff:
        prediktion = ","

    if kommaDiff == semikolonDiff:
        prediktion = ""

    print("Analyserer")
    if prediktion == "":
        print("fant ikke deleren")
        prediktion = betterInput("str", "Hva er deleren? ", "dette er ikke en string")
    else:
        print("Jeg tror deleren er: ", prediktion)
        svar = betterInput(
            "str",
            "Er dette rett?(y/n)",
            "dette er ikke en string",
            forventet=["y", "n"],
        )
        if svar != "y":
            prediktion = betterInput(
                "str", "Hva er deleren? ", "dette er ikke en string"
            )
    startLinje = betterInput("int", "Hvor starter dataen? ", "dette er ikke en int")
    filSample = lesLinjer(filbane,startLinje+4,False)
    csv_read_sample = csv.reader(filSample,delimiter=prediktion)
    print("-" * 20)
    # print1DList(filSample[startLinje:-1])
    rowList =[]
    rowLength = 1
    
    for row in csv_read_sample:
        rowLength = len(row)
        rowList.append(row)
    print2DList(rowList, 10)
    print("-" * 20)
    kolonner=""
    
    
    if rowLength!=1:
        svar = betterInput(
        "int",
        "det er mer en rad. Hvor mange rader vil du ha? ",
        "int",
        )
    kolonner = betterInput(
        "int",
        "hvilke rader? ",
        "int",
        listLength=svar
        )
    
    
    varType = betterInput("str","Hvilken variabeltype er de forskjellige kolonnene (int,float,str): ","",len(kolonner),forventet=["int","float","str"])
        
    if len(varType)==1:
        varType=[varType]
    
    # for i in range(len(varType)):
    #     varType[i]=f"'{varType[i]}'"
    
    print("Bruk denne koden \n")
    
    print(f"filbane ='{filbane}' \noppdeler='{prediktion}'\nstartLinje={startLinje} \nkolonner={kolonner}\nvarType={varType} \nverdier=hentInformasjonCSV(filbane=filbane,oppdeler=oppdeler,startLinje=startLinje,kolonner=kolonner,varType=varType)")

def hentInformasjonCSV(filbane,oppdeler,varType,startLinje=0,kolonner=0,):
    verdier = []
    for i in range(len(kolonner)):
        verdier.append([])
    if kolonner == 0:
        kolonner =[0]
    linjer = lesLinjer(filbane)
    csv_fil = csv.reader(linjer[startLinje:-1],delimiter=oppdeler)
    for row in csv_fil:
        try:
            for i in range(len(kolonner)):
                if varType[i]=="float":
                    verdier[i].append(float(row[kolonner[i]].replace(",",".")))
                elif varType[i]=="str":
                    verdier[i].append(row[kolonner[i]])
                else:
                    verdier[i].append(int(row[kolonner[i]].replace(",",".")))
        except:
                verdier[i].append(0)
    return verdier
     
    
if __name__ == "__main__":
    print("Hei")
    # lesLinjer("./tekstfiler/MikkelRev.txt",antallLinjer=1,skrivUt=True,strip=False)
    # print(lesHelFil("./tekstfiler/MikkelRev.txt"))
