from common import loadJson, ConstString, addToMap, dumpJson
from datetime import datetime
from shutil import copyfile
import os

# sort by speaker

soundFolderRoot = r'F:\Game\p5r_cpk\SOUND\EVENT'
soundMapName = 'soundMap-2023-04-12-01-21-06'
soundMapJson = loadJson(soundMapName)
outPutFolder = r"E:\Temp\p5r_sound_event-20230411\P5R_sound_classfied"

soundMapSpeaker = {}


for folder in soundMapJson:
  for adxName in soundMapJson[folder]:
    data = soundMapJson[folder][adxName]
    if(len(data) == 0):
      continue
    else:
      newAdxName = "{}-{}".format(folder, adxName)
      if(type(data) == list):
        data = data[0]
      speaker = data[ConstString.msgSpeaker.value]
      speaker = speaker.replace("?", "")
      speaker = speaker.replace(" ", "_")
      if(speaker == ' '):
        # TODO
        speaker = "主角"
      # TODO 屎山显灵

      # copy file
      dstPath = os.path.join(outPutFolder, speaker, newAdxName)
      os.makedirs(os.path.dirname(dstPath), exist_ok=True)
      try:
        if(os.path.exists(dstPath)):
          # print("{} exists".format(dstPath))
          continue
        copyfile(os.path.join(soundFolderRoot, folder, 'awb', adxName), dstPath)
        soundMapSpeaker = addToMap([speaker, newAdxName], soundMapSpeaker, data[ConstString.msgText.value])
      except Exception as e:
        print(e)
        print("copy {},{} to  {} fail".format(folder, adxName, dstPath))

dumpJson(soundMapName.replace('soundMap', 'soundMapSpeaker'), soundMapSpeaker)
print("DONE")
