from common import loadJson, dumpJson
zhSpkSndMap = loadJson('E:\Temp\p5r_sound_event-20230411\soundMapSpeaker-2023-04-12-01-21-06')

jpSpkSndMap = loadJson('E:\Temp\p5r_sound_event-20230411\soundMapSpeaker-jp-2023-04-11-15-25-34')

def getOneAndRevs(mMap):
  revMap = {}
  for spk in mMap:
    texts = mMap[spk]
    if(len(texts) > 0):
      oneFileName = list(texts.keys())[0]
      revMap[oneFileName] = spk
      continue
  return revMap

zhMap = getOneAndRevs(zhSpkSndMap)
jpMap = getOneAndRevs(jpSpkSndMap)

speakerMapZhJp = {}
speakerMapJpZh = {}

for i in zhMap:
  speakerMapZhJp[zhMap[i]] = jpMap[i]
  speakerMapJpZh[jpMap[i]] = zhMap[i]

dumpJson('speakerMapZhJp', speakerMapZhJp)
dumpJson('speakerMapJpZh', speakerMapJpZh)

print('DONE')
