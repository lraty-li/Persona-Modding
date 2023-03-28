from common import loadJson, ConstString, addToMap, dumpJson
from datetime import datetime
from shutil import copyfile
import os

# sort by speaker

soundFolderRoot = r'F:\Game\p5r_cpk\SOUND\EVENT'
soundMapJson = loadJson('./soundMap-jp.json')
outPutFolder = r"E:\Temp\P5R_sound_classfied"

soundMapSpeaker = {}


for folder in soundMapJson:
  for adxName in soundMapJson[folder]:
    data = soundMapJson[folder][adxName]
    if(len(data) == 0):
      continue
    else:
      newAdxName = "{}-{}".format(folder, adxName)
      if(type(data) == list):
        data= data[0]
      speaker = data[ConstString.msgSpeaker.value]
      speaker = speaker.replace("?", "")
      speaker = speaker.replace(" ", "_")
      if(speaker == ' '):
        # TODO 
        speaker = "主角"
      #TODO 屎山显灵
      if('_vgmt_acb_ext_E748_000-e748000_021_0006.adx' == newAdxName):
        print()
      soundMapSpeaker = addToMap([speaker, newAdxName], soundMapSpeaker, data[ConstString.msgText.value])
      # copy file
      dstPath = os.path.join(outPutFolder, speaker, newAdxName)
      os.makedirs(os.path.dirname(dstPath), exist_ok=True)
      try:
        if(os.path.exists(dstPath)):
          # print("{} exists".format(dstPath))
          continue
        #copyfile(os.path.join(soundFolderRoot, folder, 'awb', adxName), dstPath)
      except Exception as e:
        print("copy {},{} to  {} fail".format(folder, adxName, dstPath))

dumpJson("soundMapSpeaker-jp.json", soundMapSpeaker)
print("DONE")
