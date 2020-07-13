import os 
import re
lexiconsPath = "../results/resultDialign1speakerGroup/"

sharedVoc = {}
for file in os.listdir(lexiconsPath) : 
	fileNameData = file.split(".")

	if fileNameData[1] == "csv" :
		dataGroup = fileNameData[0].split("-")
		# dataGroup2 = dataGroup[0].split("-")
		segment = dataGroup[0]
		# print(file, segment)
		lexiconFile = open(lexiconsPath + file, "r")
		for line in lexiconFile.readlines():
			line = line.rstrip()
			lineData = line.split('\t')
			if len(lineData) > 1 : 
				surfaceForm = lineData[2]
				surfaceForm = re.sub(" [\.;,]","",surfaceForm)
				surfaceForm = re.sub("[\.;,] ","",surfaceForm)
				surfaceForm = re.sub("\'"," \'",surfaceForm)

				estabTurn = lineData[3]
				spanning = lineData[4]
				priming = lineData[5]
				size = len(surfaceForm.split(" "))
				if lineData[6] == "A":
					firstSpeaker = dataGroup[1][0]
				else : 
					firstSpeaker = dataGroup[1][1]	
				turns = lineData[7].split(",")

				if segment in sharedVoc :
					if surfaceForm in sharedVoc[segment]:
						for t in turns : 
							if sharedVoc[segment][surfaceForm]["firstSpeaker"] == "X" and firstSpeaker != "X":
								sharedVoc[segment][surfaceForm]["firstSpeaker"] = firstSpeaker
							if t not in sharedVoc[segment][surfaceForm]["turns"]: 
								sharedVoc[segment][surfaceForm]["turns"].append(t)
					


					else : 
						sharedVoc[segment][surfaceForm] = {}
						sharedVoc[segment][surfaceForm]["size"] = size
						sharedVoc[segment][surfaceForm]["estabTurn"] = estabTurn
						sharedVoc[segment][surfaceForm]["spanning"] = spanning
						sharedVoc[segment][surfaceForm]["priming"] = priming
						sharedVoc[segment][surfaceForm]["firstSpeaker"] = firstSpeaker
						sharedVoc[segment][surfaceForm]["turns"] = []
						for t in turns : 
							if t not in sharedVoc[segment][surfaceForm]["turns"]: 
								sharedVoc[segment][surfaceForm]["turns"].append(t)


				else :
					sharedVoc[segment] = {}
					sharedVoc[segment][surfaceForm] = {}
					sharedVoc[segment][surfaceForm]["size"] = size
					sharedVoc[segment][surfaceForm]["estabTurn"] = estabTurn
					sharedVoc[segment][surfaceForm]["spanning"] = spanning
					sharedVoc[segment][surfaceForm]["priming"] = priming
					sharedVoc[segment][surfaceForm]["firstSpeaker"] = firstSpeaker
					sharedVoc[segment][surfaceForm]["turns"] = []
					for t in turns : 
						if t not in sharedVoc[segment][surfaceForm]["turns"]: 
							sharedVoc[segment][surfaceForm]["turns"].append(t)


for segment, formData in sharedVoc.items():
	output = open("../results/shLexiconGlobal/"+segment+".csv", "w")
	for expr, values in formData.items():
		output.write(expr + ";" + str(values['size'])+";"+values['estabTurn']+";"+values['spanning']+";"+values['priming']+";"+values['firstSpeaker']+";")
		for t in values['turns']: 
			output.write(t+",")

		output.write("\n")






