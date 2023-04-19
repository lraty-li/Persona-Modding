from common import loadJson, dumpJson
import re
soundMapName = "E:\Code\Git\Persona-Modding\classify_sound_file\soundMap-2023-04-14-13-11-02.json"
soundMap = loadJson(soundMapName)

speakerIdMap = {}

for adxFolderRoot in soundMap:
  for adxName in soundMap[adxFolderRoot]:
    if not (len(soundMap[adxFolderRoot][adxName]) == 0):
      result = re.search(r"e[0-9]+_[0-9]+_[0-9]+(_(\w)+)?.adx", adxName)
      if(result != None):
        speakerid = result.string.split('_')[2].replace('.adx', '')
        speakerIdMap[speakerid] = soundMap[adxFolderRoot][adxName]['speaker']


dumpJson('speaker_id.json', speakerIdMap)

print("DONE")
