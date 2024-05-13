import os 
import sys 
import kultBiblotek2 as kB
import subprocess

# Specify the command to start the other Python script




# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0]))  #path til der filen fins
folderPathSpill = folderPath+r"/spill"  # path til spill folder
spillListe = os.listdir(folderPathSpill) #liste over alle spill i folder










#spør bruker hvilket spill man skal kjøre
print("")
print("-"*20)
print("Her er en liste over filer:")
kB.print1DList(spillListe)

brukerInput = kB.betterInput(variableType="int",inputText=f"Hvilken fil vil du ha?(0-{len(spillListe)-1}): ",errorText="Dette var ikke et heltall",forventet=[i for i in range(len(spillListe))])
spillnavn =spillListe[brukerInput]




#generer path til spillet
spillPath = r"/spill"+"/"+spillnavn+"/"+spillnavn+".py"
print(folderPath+ spillPath)









## starter spillet
command = ['python', folderPath+spillPath]


# Use subprocess to start the other Python script
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the process to finish and get the return code
return_code = process.wait()

# Check if the process exited successfully
if return_code == 0:
    print("Script executed successfully.")
else:
    print(f"Error: Script exited with return code {return_code}.")