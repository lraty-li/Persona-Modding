from common import loadJson, addToMap, dumpJson
from shutil import copyfile
import os

# sort by speaker

soundFolderRoot = r'./cache'
soundMapName = 'soundMap.json'
soundMapJson = loadJson(soundMapName)
outPutFolder = r"./classfied"

soundMapSpeaker = {}


for wav in soundMapJson:
  if (len(soundMapJson[wav]) == 0):
    continue
  text = soundMapJson[wav]['text']
  speaker = soundMapJson[wav]['speaker']
  if (len(text) == 0):
    continue
  else:
    if (type(text) == list):
      text = text[0]

    speaker = speaker.replace("?", "")
    speaker = speaker.replace(" ", "_")
    if (speaker == ''):
      speaker = "_"

    # copy file
    dstPath = os.path.join(outPutFolder, speaker, wav)
    os.makedirs(os.path.dirname(dstPath), exist_ok=True)
    try:
      if (os.path.exists(dstPath)):
        print("{} exists, bypass".format(dstPath))
        continue
      copyfile(os.path.join(soundFolderRoot, wav), dstPath)

      soundMapSpeaker = addToMap([speaker, wav], soundMapSpeaker, text)
    except Exception as e:
      print(e)
      print("copy {},{} to  {} fail".format(folder, adxName, dstPath))

dumpJson(soundMapName.replace('soundMap', 'soundMapSpeaker'), soundMapSpeaker)
print("DONE")
