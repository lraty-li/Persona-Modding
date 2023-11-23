from common import loadJson,dumpJson
import os

msgMap = loadJson('./msgMap.json')
soundMap = {}

wavsRoot = r'./cache'

wavs = os.listdir(wavsRoot)
wavs = [i for i in wavs if(i.endswith('.wav'))]

for wav in wavs:
  vpNum = int(wav.split('_')[-1].replace('.wav',''))-1
  if(vpNum == 0):
    continue
  try:
    text = msgMap[wav[0:3]][wav[3:6]][str(vpNum)]
  except KeyError as e:
    text = ''
  soundMap[wav] = text

dumpJson('./soundMap.json', soundMap)
print('DONE')
