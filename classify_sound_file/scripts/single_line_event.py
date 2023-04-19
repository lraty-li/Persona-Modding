from common import *
import os
import re

# TODO root base
# TODO 合并 field_npc


def dumpSngLineMsgs(soundMap, folderRoot):

  files = [i for i in os.listdir(folderRoot) if i.endswith('.BF')]
  for file in files:
    with open(os.path.join(folderRoot, file + '.flow'), 'r', encoding='utf8') as flowFile:
      rawContent = flowFile.read()
      # content = rawContent.split('}\n\n\n')
      msgFilePath = file + '.msg'
      msgNodes = loadMsgFile(os.path.join(folderRoot, msgFilePath))
      vpLines = getVpLinesNew(msgNodes)
      soundBankInvokes = re.findall(r'[\s][0-9]+;[\s|\S]+UNKNOWN_FUNCTION_384', rawContent)
      for sndIvok in soundBankInvokes:
        event = re.findall(r'[\s][0-9]+;', sndIvok)
        eventIds = [i[1:-1].zfill(3) for i in event]
        eventIds.reverse()
        for vp in vpLines:
          for line in vpLines[vp]:
            tempMapPath = [*eventIds, line[ConstString.vpLineSoundIndex.value]]
            soundMap = addToMap(tempMapPath, soundMap, [line])

  return soundMap


def dumpAllSngLineMsgs(paths):
  msgs = []
  for path in paths:
    soundMap = {}
    soundMap = dumpSngLineMsgs(soundMap, path)
    msgs.append(soundMap)
  return msgs
