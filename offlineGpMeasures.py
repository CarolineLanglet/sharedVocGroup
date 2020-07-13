import os 

lexiconsPath = "../results/shLexiconGlobal/"


lexiconAnalysis = {}
for file in os.listdir(lexiconsPath) : 
	lexiconNameData = file.split(".")
	group = lexiconNameData[0]
	lexiconFile = open(lexiconsPath+file, "r")
	els = 0
	if file != ".DS_Store": 
		for line in lexiconFile.readlines():
			lineData = line.split(";")
			if lineData[0] == "Surface Form":
				els = els 
			else : 
				els = els + 1

		lexiconAnalysis[group] = {}
		lexiconAnalysis[group]["els"] = els


syntheseDial = open("../results/dial-synthesis1speakerVsGr.csv","r")
for l in syntheseDial.readlines():
	lData = l.split("\t")
	if lData[0] != "ID" : 
		fileName = lData[0]
		fileNameData = fileName.split("-")
		groupName = fileNameData[0]
		nbTokens = lData[2]
		nbUtterances = lData[1]
		if "nbTokens" not in lexiconAnalysis[groupName]: 
			lexiconAnalysis[groupName]["nbTokens"] = nbTokens

		if "nbUtterances" not in lexiconAnalysis[groupName]: 
			lexiconAnalysis[groupName]["nbUtterances"] = nbUtterances

output = open("../results/synthesisGlobalAllConv.csv","w")
output.write("group;nbUtterances;nbTokens;expresion Lexique Size (els);expression variety"+"\n")
for group, data in lexiconAnalysis.items() : 
	ev = float(data["els"])/float(data["nbTokens"])
	output.write(group + ";" + str(data["nbUtterances"]) +";"+ str(data["nbTokens"]) +";"+ str(data["els"]) +";"+ str(ev)+"\n")





