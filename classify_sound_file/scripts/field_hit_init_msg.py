# 偷鸡大失败
from common import *
import os
import re

paths = [

    # r"F:\Game\p5r_cpk\FIELD\KF_EVENT",
    # r"F:\Game\p5r_cpk\FIELD\NPC"
    r"F:\Game\p5r_cpk\SCRIPT\FIELD",  # TODO 主，都去这里找message，再去另外两个的flow找引用？
]
# search flow event sound invoke
#     SND_VOICE_DNGEVT_SETUP( 486, 30 );


def filterFlow(msgFolderRoot, folderRoot, sndIvokMap):
  # filter flows with sound refer

  # scriptFieldRoot = r"F:\Game\p5r_cpk\SCRIPT\FIELD"
  scriptFieldRoot = os.path.join(msgFolderRoot, 'SCRIPT', 'FIELD')
  reMSGInvokPattern = r'MSG\( \w+ \);'

  flows = os.listdir(folderRoot)
  flows = [file for file in flows if file.endswith(".flow")]
  for flowFile in flows:
    flowFilePath = os.path.join(folderRoot, flowFile)
    with open(flowFilePath, 'r') as file:
      rawContent = file.read()
      content = rawContent.split('}\n\n\n')
      msgNodes = loadMsgFile(flowFilePath[:-5] + '.msg')
      vpLines = getVpLinesNew(msgNodes)

      for functionField in content:
        soundBankInvokes = re.findall(r'SND_VOICE_DNGEVT_SETUP\( [0-9]+, [0-9]+ \);', functionField)
        # 似乎每个SND_VOICE_DNGEVT_SETUP去read的field script都是一样的, 但如果分布在两个函数，还是会重复加入
        soundBankInvokes = set(soundBankInvokes)
        if(len(soundBankInvokes) > 1):
          print("muti sound invok in one fucionField", folderRoot, flowFilePath)
        for soundInvok in soundBankInvokes:
          event = re.findall(r'[0-9]+', soundInvok)
          eventId = event[0].zfill(3)
          eventSubId = event[1].zfill(3)
          # sndIvokMap = addToMap([flowFile, eventId, eventSubId, 'content'], sndIvokMap, [content])
          # dont' care shit code now

          # own msg but add msg with sound only
          msgInvokes = re.findall(reMSGInvokPattern, functionField)
          pureMsgInvokes = [lien.split(" ")[1] for lien in msgInvokes]
          for msgTitle in pureMsgInvokes:
            # 覆盖式
            for line in vpLines[msgTitle]:
              sndIvokMap = addToMap([eventId, eventSubId, line[ConstString.vpLineSoundIndex.value]], sndIvokMap, [line])

          # field load
          fldScptLoad = re.findall(r'FLD_SCRIPT_READ\( [0-9]+, [0-9]+, [0-9]+ \);', functionField)
          if(len(fldScptLoad) > 1):
            print("muti fldScptLoad in one fucionField", folderRoot, flowFilePath)
          for fldRead in fldScptLoad:
            scirpt = re.findall(r'[0-9]+', fldRead)
            scirptId = scirpt[0]
            scirptId1 = scirpt[1]
            scirptId2 = scirpt[2]
            scirptFileName = "FSCR{:04d}_{:03d}_{:03d}.BF".format(int(scirptId), int(scirptId1), int(scirptId2))
            # msgInvokes = re.findall(reMSGInvokPattern, functionField)
            scriptFlowPath = scirptFileName + '.flow'

            msgFilePath = scirptFileName + ".msg"
            msgNodes = loadMsgFile(os.path.join(scriptFieldRoot, msgFilePath))
            vpLines = getVpLinesNew(msgNodes)
            for msgTitle in vpLines:
              lines = vpLines[msgTitle]
              for line in lines:
                sndIvokMap = addToMap([eventId, eventSubId, line[ConstString.vpLineSoundIndex.value]], sndIvokMap, line)
              # print()

        # var sound invok
        varFldScptLoads = re.findall(r'SND_VOICE_DNGEVT_SETUP\( [a-zA-Z_]+\w+, [a-zA-Z_]+\w+ \);', functionField)

        for sndLoad in varFldScptLoads:
          # todo 全局搜索第一个参数，域内搜索第二个
          sndLoad = sndLoad[sndLoad.index('('): sndLoad.index(')')]
          # possible value
          varNames = re.findall(r'[a-zA-Z_]+\w+', sndLoad)
          pattern1stParam = varNames[0] + r' = 0x[0-9]+'
          eventIdHex = re.search(pattern1stParam, rawContent).group(0).split(' ')[2]
          eventId = str(int(eventIdHex, 16)).zfill(3)
          # for varName in varNames:
          pattern = varNames[1] + ' == [0-9]+ \)\s+{[^}]*'
          matchs = re.finditer(pattern, functionField)
          scops = []
          for match in matchs:
            index = match.span()
            scops.append(functionField[index[0]:index[1]])
          for ifScop in scops:
            msgInvokes = re.findall(reMSGInvokPattern, ifScop)

            pureMsgInvokes = [lien.split(" ")[1] for lien in msgInvokes]
            eventSubId = re.search(r'== [0-9]+', ifScop).group(0).split(' ')[1]
            eventSubId = eventSubId.zfill(3)
            for msgTitle in pureMsgInvokes:
              lines = vpLines[msgTitle]
              for line in lines:
              # 覆盖式
                sndIvokMap = addToMap([eventId, eventSubId, line[ConstString.vpLineSoundIndex.value]], sndIvokMap, [line])

  return sndIvokMap

def dumpAllsndVoiceDNGSetUpPaths(msgFolderRoot, paths):
  refMap = []
  for path in paths:
    soundMap = {}
    refMap.append(filterFlow(msgFolderRoot, os.path.join(msgFolderRoot, *path), soundMap))
  return refMap

if __name__ == '__main__':

  sPaths = [
      r"F:\Game\p5r_cpk\FIELD\HIT",
      r"F:\Game\p5r_cpk\FIELD\INIT",
      r"F:\Game\p5r_cpk\SCRIPT\FIELD"
  ]

  # files = os.listdir(scriptFieldRoot)
  # flows = [file for file in files if file.endswith(".flow")]

  refMap = []

  for folder in sPaths:
    sndIvokMap = {}
    refMap.append(filterFlow(folder, sndIvokMap))
  # own refence msg   自己就有，但是要按msg header 分组

  # outer refence， msg 在

  with open('script_out.json', 'w', encoding='utf8') as file:
    file.write(json.dumps(refMap, ensure_ascii=False))

  print('DONE')
