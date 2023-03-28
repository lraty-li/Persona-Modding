from common import *
import os
import re

# TODO root base
# TODO 合并 field_npc
campChatFolderRoot = r'F:\Game\p5r_cpk\CAMP\CHAT'

files = [i for i in os.listdir(campChatFolderRoot) if i.endswith('.BF')]

soundMpap = {}

for file in files:
  with open(os.path.join(campChatFolderRoot, file + '.flow'), 'r', encoding='utf8') as flowFile:
    rawContent = flowFile.read()
    # content = rawContent.split('}\n\n\n')
    msgFilePath = file + '.msg'
    msgNodes = loadMsgFile(os.path.join(campChatFolderRoot, msgFilePath))
    vpLines = getVpLinesNew(msgNodes)
    soundBankInvokes = re.findall(r'[\s][0-9]+;[\s|\S]+UNKNOWN_FUNCTION_384', rawContent)
    for sndIvok in soundBankInvokes:
      event = re.findall(r'[\s][0-9]+;', sndIvok)
      eventIds = [i[1:-1].zfill(3) for i in event]
      eventIds.reverse()
      for vp in vpLines:
        for line in vpLines[vp]:
          tempMapPath = [*eventIds, line[ConstString.vpLineSoundIndex.value]]
          soundMpap = addToMap(tempMapPath, soundMpap, [line])

with open('camp_chat.json', 'w', encoding='utf8') as jsonFile:
  jsonFile.write(json.dumps(soundMpap, ensure_ascii=False)) 
