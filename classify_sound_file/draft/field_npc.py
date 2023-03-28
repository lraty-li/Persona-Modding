from common import *
import os
import re

npcFolderRoot = r'F:\Game\p5r_cpk\FIELD\NPC'

files = [i for i in os.listdir(npcFolderRoot) if i.endswith('.BF')]

soundMpap = {}

for file in files:
  with open(os.path.join(npcFolderRoot, file + '.flow'), 'r', encoding='utf8') as flowFile:
    if(file == 'CORP020.BF'):
      print()
    rawContent = flowFile.read()
    # content = rawContent.split('}\n\n\n')
    msgFilePath = file + '.msg'
    msgNodes = loadMsgFile(os.path.join(npcFolderRoot, msgFilePath))
    vpLines = getVpLinesNew(msgNodes)
    soundBankInvokes = re.findall(r'MAIN_BYE_GREET_SCR[\s|\S]+UNKNOWN_FUNCTION_384', rawContent)
    for sndIvok in soundBankInvokes:
      event = re.findall(r'[\s][0-9]+;', sndIvok)
      eventIds = [i[1:-1] for i in event]
      eventIds.reverse()
      for vp in vpLines:
        for line in vpLines[vp]:
          tempMapPath = [*eventIds, line[ConstString.vpLineSoundIndex.value]]
          soundMpap = addToMap(tempMapPath, soundMpap, [line])

with open('field_npc.json', 'w', encoding='utf8') as jsonFile:
  jsonFile.write(json.dumps(soundMpap, ensure_ascii=False)) 
