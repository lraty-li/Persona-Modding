import json
import difflib

### pair up eng and zh hans names
lines = []
with open("./names.txt", encoding="utf8") as file:
  lines = file.read().splitlines()
ENGNames = lines[:255]
CHSNames = lines[255:]
namePiars = dict(zip(ENGNames, CHSNames))
with open("name_pair-game.json","w", encoding='utf8') as file:
  file.write(json.dumps(namePiars,ensure_ascii=False))
print("done")

### re generate p4 demon-data.json, insert zhHansName property
'''
suspiciousPair = {}
newDemonData = {}
demonDataFileName = "golden-party-data.json"
namePairFile = "name_pair.json"
with open(demonDataFileName, 'r+', encoding="utf8") as file:
  with open(namePairFile, 'r', encoding="utf8") as namefile:
    orginData = json.loads(file.read())
    newDemonData = orginData
    namePairs = json.loads(namefile.read())

    gameEngNames = set(namePairs.keys())
    for i in orginData.keys():
      try:
        newDemonData[i]['zhHansName'] = namePairs[difflib.get_close_matches(i, gameEngNames, 1, cutoff=0.8)[0]]
      except Exception as e:
        suspiciousPair[i] = difflib.get_close_matches(i, gameEngNames, 10, cutoff=0.5)
with open("new-"+demonDataFileName , "w") as file:
  file.write(json.dumps(newDemonData))
# print(suspiciousPair)
'''

### generate i18n json for website using ngx-translate(website use "Yomotsu-Ikusa" but game has "Ikusa")
'''
suspiciousPair = {}
dataFileNames = ["golden-party-data.json","golden-demon-data.json","party-data.json","demon-data.json"]
namePairFile = "name_pair-game.json"

namePairWebsite = {}
with open(namePairFile, 'r', encoding="utf8") as namefile:
  namePairs = json.loads(namefile.read())
  for demonDataFileName in dataFileNames:
    with open(demonDataFileName, 'r+', encoding="utf8") as file:
        orginData = json.loads(file.read())
        gameEngNames = set(namePairs.keys())
        for i in orginData.keys():
          try:
            namePairWebsite[i] = namePairs[difflib.get_close_matches(i, gameEngNames, 1, cutoff=0.8)[0]]
          except Exception as e:
            suspiciousPair[i] = difflib.get_close_matches(i, gameEngNames, 10, cutoff=0.5)
with open("name_pair-website.json", "w") as file:
  file.write(json.dumps(namePairWebsite))
print(suspiciousPair)

'''
