import os 
import sys 

# finner mappen som filene ligger i
folderPath = os.path.dirname(os.path.abspath(sys.argv[0])) 
heiFilPath = r"/data/hei.txt"

innhold = ""
with open(folderPath+heiFilPath, encoding="utf-8") as fil:
    innhold = fil.read()
    print(innhold)
    
