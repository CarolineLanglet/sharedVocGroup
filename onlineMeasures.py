import os 
import re
import statistics

filesPath = "../results/resultDialign1speakerGroup/"
lexiconsPath = "../results/shLexiconGlobal/"
convAnalysis = {}
lexiconsInfo = {}
for file in os.listdir(filesPath) : 
	fileNameData = file.split(".")
	if fileNameData[1] == "txt" :
		dataGroup = fileNameData[0].split("-")
		group = dataGroup[0]
		speakerFocus = dataGroup[1][0]
		dialog = open(filesPath + file, "r")
		i = 0 
		lines = dialog.readlines()
		for i in range(0, len(lines)): 
			line = lines[i]
			if len(line) > 1: 
				line = line.rstrip()
				firstChar = line[0]+line[1]
				#### analysis of dialogue part 1 
				#### get the nb of token per speech turns
				if firstChar == "A|" or firstChar == "B|":
					
					line = re.sub(r'\[', '', line)
					line = re.sub(r'\]', '', line)
					line = re.sub(r'_', '', line)
					infos = re.search('[AB]\|(\d+)\:',line)
					
					idSpeechT = infos.group(1)

					lineData = line.split("|")
					speakerOfSP = lineData[0]
					if speakerOfSP == "A" :
						speaker = speakerFocus
					else : 
						speaker = "X"
					speech = lineData[1]
					speechData = speech.split(" ")
					nbTokens = len(speechData) - 1

					if group in convAnalysis : 
						if idSpeechT in convAnalysis[group] : 
							if convAnalysis[group][idSpeechT]["speaker"] == "X" and speaker != "X" : 
								convAnalysis[group][idSpeechT]["speaker"] = speaker

						else : 

							convAnalysis[group][idSpeechT] = {}
							convAnalysis[group][idSpeechT]["speaker"] = speaker
							convAnalysis[group][idSpeechT]["nbTokens"] = nbTokens
							convAnalysis[group][idSpeechT]["speech"] = speech

					else : 
						convAnalysis[group] = {}
						convAnalysis[group][idSpeechT] = {}
						convAnalysis[group][idSpeechT]["speaker"] = speaker
						convAnalysis[group][idSpeechT]["nbTokens"] = nbTokens
						convAnalysis[group][idSpeechT]["speech"] = speech
				
				### Analyse dialogue Part II		

				if firstChar == "Tu" : 
					idMatch = re.search('Turn ID=(\d+)',line)
					idTurn = idMatch.group(1)
					freePatternsLine = lines[i+1]
					constrainPatternsLine = lines[i+2]
					freePatternsLine = re.sub(r', Pattern', '##Pattern', freePatternsLine)
					freePatternsLine = re.sub(r'Free: Pattern', '##Pattern', freePatternsLine)
					freePatternsLine = re.sub(r'\t+', '', freePatternsLine)
					freePatterns = freePatternsLine.split('##Pattern=')

					constrainPatternsLine = re.sub(r', Pattern', '##Pattern', constrainPatternsLine)
					constrainPatternsLine = re.sub(r'Constrained: Pattern', '##Pattern', constrainPatternsLine)
					constrainPatternsLine = re.sub(r'\t', '', constrainPatternsLine)
					constraintPatterns = constrainPatternsLine.split('##Pattern=')
					
					
					for fPattern in freePatterns:
						if group in convAnalysis : 
							if idTurn in convAnalysis[group] : 
								if "freePatterns" in convAnalysis[group][idTurn] :
									if fPattern not in convAnalysis[group][idTurn]["freePatterns"] :
										convAnalysis[group][idTurn]["freePatterns"].append(fPattern)
								else : 
									convAnalysis[group][idTurn]["freePatterns"] = []
									convAnalysis[group][idTurn]["freePatterns"].append(fPattern)
					
					for cPattern in constraintPatterns:
						if group in convAnalysis : 
							if idTurn in convAnalysis[group] : 
								if "constrainedPatterns" in convAnalysis[group][idTurn] :
									if cPattern not in convAnalysis[group][idTurn]["constrainedPatterns"] : 
										convAnalysis[group][idTurn]["constrainedPatterns"].append(cPattern)
								else : 
									convAnalysis[group][idTurn]["constrainedPatterns"] = []
									convAnalysis[group][idTurn]["constrainedPatterns"].append(cPattern)
								
			

for lexiconFile in os.listdir(lexiconsPath):
	dataGroup = lexiconFile.split(".")
	conv = dataGroup[0]
	lexicon = open(lexiconsPath + lexiconFile, "r")
	if lexiconFile != ".DS_Store": 
		for l in lexicon.readlines():
			if len(l) > 1:
				l = l.rstrip()
				lData = l.split(";")
				surfaceForm = lData[0]
				size = lData[1]
				establishTurn = lData[2]
				spanning = lData[3]
				priming = lData[4]
				firstSpeaker = lData[5]
				turns = lData[6].split(",")

				if conv in lexiconsInfo : 
					lexiconsInfo[conv][surfaceForm] = {}
					lexiconsInfo[conv][surfaceForm]["size"] = size
					lexiconsInfo[conv][surfaceForm]["establishTurn"] = establishTurn
					lexiconsInfo[conv][surfaceForm]["spanning"] = spanning
					lexiconsInfo[conv][surfaceForm]["priming"] = priming
					lexiconsInfo[conv][surfaceForm]["firstSpeaker"] = firstSpeaker
					lexiconsInfo[conv][surfaceForm]["turns"] = turns

				else : 
					lexiconsInfo[conv] = {}
					lexiconsInfo[conv][surfaceForm] = {}
					lexiconsInfo[conv][surfaceForm]["size"] = size
					lexiconsInfo[conv][surfaceForm]["establishTurn"] = establishTurn
					lexiconsInfo[conv][surfaceForm]["spanning"] = spanning
					lexiconsInfo[conv][surfaceForm]["priming"] = priming
					lexiconsInfo[conv][surfaceForm]["firstSpeaker"] = firstSpeaker
					lexiconsInfo[conv][surfaceForm]["turns"] = turns



dataTurn = {}
output = open("../results/heterorepetByTurns.csv", "w")
output.write("group;idT;speakerSP;nbTotalPatterns;nb_fPatternsInT;nb_cPatternsInT;derU;derU_c;derU_f;\n")
for group, data in convAnalysis.items():
	patterns = lexiconsInfo[group].keys()
	for idT, infos in data.items():
		speakerSP = infos["speaker"]
		nb_cPatternsInT = 0 #nb de constrained patterns dans le tour de parole
		nb_fPatternsInT = 0 # nb de free patterns dans le tour de parole
		nbTokenInTurn = infos["nbTokens"] # nb de tokens dans le tour de parole
		nbTokenIn_cPatterns = 0 # nb de token dedies aux contrained patterns dans le tour de parole
		nbTokenIn_fPatterns = 0 # nb de token dedies aux free patterns dans le tour de parole
		
		### get nb constrained patterns, and nb tokens in constr patterns 
		for cPattern in infos["constrainedPatterns"]:
			for p in patterns : 
				if cPattern == p: 
					if speakerSP != lexiconsInfo[group][cPattern]["firstSpeaker"]:
						nb_cPatternsInT = nb_cPatternsInT + 1
						cPatternData = cPattern.split(" ")
						nbTokenIn_cPatterns = nbTokenIn_cPatterns + len(cPatternData)
						

		### get nb free patterns, and nb tokens in free patterns 
		for fPattern in infos["freePatterns"]:
			for p in patterns : 
				if fPattern == p: 
					if speakerSP != lexiconsInfo[group][fPattern]["firstSpeaker"]:
						nb_fPatternsInT = nb_fPatternsInT + 1
						fPatternData = fPattern.split(" ")
						nbTokenIn_fPatterns =  nbTokenIn_fPatterns + len(fPatternData)

		###nombre de patterns detectes dans le tour de parole
		### nombre de tokens consacres aux heterorepetitions dans le tour de parole / nb token tour de parole (1. cible sur les free, 2. cible sur les constrained, 3. both together)
		nbTotalPatterns = nb_fPatternsInT + nb_cPatternsInT
		derU_c = nbTokenIn_cPatterns/nbTokenInTurn
		derU_f = nbTokenIn_fPatterns/nbTokenInTurn
		derU = nbTotalPatterns/nbTokenInTurn

		output.write(group + ";" + idT+ ";" + speakerSP+ ";"  + str(nbTotalPatterns) + ";"  + str(nb_fPatternsInT)+ ";"  + str(nb_cPatternsInT) + ";"  + str(derU) + ";"  + str(derU_c) + ";"  + str(derU_f) + ";"  + "\n")


		if group in dataTurn : 
			dataTurn[group][idT] = {}
			dataTurn[group][idT]["speaker"] = speakerSP
			dataTurn[group][idT]["nb_fPatternsInT"] = nb_fPatternsInT
			dataTurn[group][idT]["nb_cPatternsInT"] = nb_cPatternsInT
			dataTurn[group][idT]["nbTotalPatterns"] = nbTotalPatterns
			dataTurn[group][idT]["derU_c"] = derU_c
			dataTurn[group][idT]["derU_f"] = derU_f
			dataTurn[group][idT]["derU"] = derU

		else : 
			dataTurn[group] = {}
			dataTurn[group][idT] = {}
			dataTurn[group][idT]["speaker"] = speakerSP
			dataTurn[group][idT]["nb_fPatternsInT"] = nb_fPatternsInT
			dataTurn[group][idT]["nb_cPatternsInT"] = nb_cPatternsInT
			dataTurn[group][idT]["nbTotalPatterns"] = nbTotalPatterns
			dataTurn[group][idT]["derU_c"] = derU_c
			dataTurn[group][idT]["derU_f"] = derU_f
			dataTurn[group][idT]["derU"] = derU


dataSpeaker = {}
output2 = open("../results/resultsOnLine.csv","w")
output2.write("group"+";"+"meanCpatternsByTurn;meanFpatternsByTurn;meanPatternByTurn;meanDerU_c;meanDerU_f;meanDerU\n")

for group, values in dataTurn.items():
	nbTurnInConv = 0
	totalNbPatternsInConv = 0
	totalNb_fPatternsInConv = 0
	totalNb_cPatternsInConv = 0

	allDerU = []
	allDerU_f = []
	allDerU_c = []

	for idTurn, data in values.items():
		totalNb_fPatternsInConv = totalNb_fPatternsInConv + data["nb_fPatternsInT"]
		totalNb_cPatternsInConv = totalNb_cPatternsInConv + data["nb_cPatternsInT"]
		totalNbPatternsInConv = totalNbPatternsInConv + data["nbTotalPatterns"]
		allDerU_c.append(data["derU_c"])
		allDerU_f.append(data["derU_f"])
		allDerU.append(data["derU"])
		nbTurnInConv = nbTurnInConv + 1

	meanCpatternsByTurn = totalNb_cPatternsInConv / nbTurnInConv
	meanFpatternsByTurn = totalNb_fPatternsInConv / nbTurnInConv
	meanPatternByTurn = totalNbPatternsInConv/nbTurnInConv
	meanDerU_c = statistics.mean(allDerU_c)
	meanDerU_f = statistics.mean(allDerU_f)
	meanDerU = statistics.mean(allDerU)

	output2.write(group+";"+str(meanCpatternsByTurn)+";"+str(meanFpatternsByTurn)+";"+str(meanPatternByTurn)+";"+str(meanDerU_c)+";"+str(meanDerU_f)+";"+str(meanDerU)+"\n")

