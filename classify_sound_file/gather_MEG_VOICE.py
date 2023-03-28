import os
# from collections import Counter

import functools
from common import *


# def parse(line):
#   index = 0
#  while index < len(line):
#   # [msg MSG_000_0_0 [新岛 真]]
#   # [s][f 4 10 65535 0 0][vp 8 0 0 2 65535 0]居然还有那么多女生啊。[n][f 1 3 65535][w][e]
#   if char == "[":
#     tagName

#   elif char == "]"

def fillEmpty(acbFolder, adxNames, mapContainer):
  for adx in adxNames:
    mapContainer = addToMap([acbFolder, adx], mapContainer, [])
  return mapContainer


def matchMSGLine(acbFolder, adxNames, mapContainer, msgs):
  orderList = [str(i) for i in range(1, 512)]
  if(acbFolder == "_vgmt_acb_ext_E228_101_00"):
    print()
  
  # global globalAdxCounter
  if([cur[:3] for cur in adxNames].count('Cue') == len(adxNames)):
    # all Cues
    # globalAdxCounter += len(list(adxNames))
    eventIds = re.findall(r'[0-9]+', acbFolder)
    susMsgs = []
    for msgMap in msgs:
      try:
        cueMsgLines = getFromMap(eventIds, msgMap)
      except KeyError as e:
        continue
      susMsgs.append(cueMsgLines)
    if(len(susMsgs) == 0):
      # 未搜索到任何msg, 生成空
      mapContainer = fillEmpty(acbFolder, adxNames, mapContainer)
      return mapContainer

    for msgGroup in susMsgs:
      cueLines =[]
      sortedKeys = sorted(list(msgGroup.keys()))
      if(len(sortedKeys) == 1 and sortedKeys[0] == ConstString.noIndex.value):
        continue # todo 输出废案？
        # 只有 noIndex 并且长度正好相等 ，偷鸡
        # cueLines = msgGroup[ConstString.noIndex.value]
        # if(len(cueLines) != len(adxNames)):
        #   mapContainer = fillEmpty(acbFolder, adxNames, mapContainer)
        # else:
        #   for adx, susMsgLine in zip(adxNames, cueLines):
        #     mapContainer = addToMap([acbFolder, adx], mapContainer, susMsgLine)
        # return mapContainer
      for adx in adxNames:
        adxId = str(int(adx[3:adx.index(".")]))
        try:
          mapContainer = addToMap([acbFolder, adx], mapContainer, msgGroup[adxId])
        except KeyError as e:
          mapContainer = addToMap([acbFolder, adx], mapContainer, [])
          continue


        # else
        # 不是纯noIndex, 先根据 Cue{id}.adx  id匹配
        
        # 再按顺序匹配noIndex？
      # if(len(cueLines) != len(adxNames)):
      #   mapContainer = fillEmpty(acbFolder, adxNames, mapContainer)
      #   print("cue voice line maybe mismatch in ", acbFolder)
      #   return mapContainer

      # if(len(msgGroup) > len(adxNames)):
      #   # 记录多出来的
      #   mapContainer = addToMap([acbFolder, "textWithoutVoice"], mapContainer, sortedCueMsgLines[len(adxNames):])
      # else:
      #   # mapContainer = addToMap([acbFolder, "textWithoutVoice"], mapContainer, adxNames[len(msgGroup):])
      #   pass

    return mapContainer
  else:
    # 移除e000000
    adxNames = list(filter(lambda x : x.startswith("e000000") == False, adxNames))
    # globalAdxCounter += len(adxNames)
    adxNameMatches = [re.search(r"e[0-9]+_[0-9]+_[0-9]+.adx", adx) for adx in adxNames]
    adxNameMatches = filter(lambda x : x != None, adxNameMatches)
    adxNames = [match.group(0) for match in adxNameMatches]
    # 分组，可能有不同event 的语音
    groupedAdxs = {}
    for adxName in adxNames:
      eventId = adxName[1:4]
      eventSubId = adxName[4:7]
      if(adxName == 'e748000_021_0006.adx'):
        print()
      groupedAdxs = addToMap([eventId, eventSubId], groupedAdxs, [adxName])

    for eventId in groupedAdxs:
      for eventSubId in groupedAdxs[eventId]:
        eventAdxNames = groupedAdxs[eventId][eventSubId]
        eventAdxNames.sort(key=functools.cmp_to_key(cmpAdxName))
        # eventAdxIds = [str(int(adxName.split("_")[1])) for adxName in eventAdxNames]
        susMsgGroup = []
        for msgMap in msgs:
          try:
            msg = msgMap[eventId][eventSubId]
          except KeyError as e:
            continue
          susMsgGroup.append(msg)

        # eventAdxIdsLength = len(eventAdxIds)
        for susMsgs in susMsgGroup:
          for index in range(len(eventAdxNames)):
            try:
              mapContainer = addToMap([acbFolder, eventAdxNames[index]], mapContainer, susMsgs[orderList[index]])
            except KeyError as e:
              mapContainer = addToMap([acbFolder, eventAdxNames[index]], mapContainer, {})
              # TODO 匹配失败？
              continue

          # msgIdsOnly = set(filter(lambda x : x != ConstString.noIndex.value, susMsgs.keys()))
          # if(len(set(eventAdxIds) & msgIdsOnly) == 0 and len(msgIdsOnly) == eventAdxIdsLength):
          #   pass
            # id完全错开，但是长度一致，且有id
            # susMsgsIds = list(sorted(msgIdsOnly))
            # for index in range(eventAdxIdsLength):
            #   mapContainer = addToMap([acbFolder, eventAdxNames[index]], mapContainer, susMsgs[susMsgsIds[index]])
          # else:



            # TODO msgIdsOnly eventAdxIds 对比？
            # id匹配（一般情况）
          # for eventAdxId in eventAdxIds:
          #   try:
          #     mapContainer = addToMap([acbFolder, eventAdxNames[eventAdxIds.index(eventAdxId)]], mapContainer, susMsgs[eventAdxId])
          #   except KeyError as e:
          #     mapContainer = addToMap([acbFolder, eventAdxNames[eventAdxIds.index(eventAdxId)]], mapContainer, {})
          #     # TODO 匹配失败？
          #     continue

    # for adx in adxNames:
    #   adxId = 0
    #   # TODO 有_00形式无被跳过？
    #   # match form e105001_028_0103
    #   match = re.search(r"e[0-9]+_[0-9]+_[0-9]+.adx", adx)
    #   if (match == None):
    #     continue
    #   event = match.group(0)
    #   eventId = event[1:4]
    #   eventSubId = event[4:7]
    #   adxId = int(match.group(0).split("_")[1])
    #   susMsgs = []
    #   for msgMap in msgs:
    #     try:
    #       msg = msgMap[eventId][eventSubId][str(adxId)]
    #     except KeyError as e:
    #       continue
    #     susMsgs.append(msg)
    #   # if(len(susMsgs) > 1):
    #   #   #todo muti
    #   #   print("muti lines")
    #   #   pass
    #   # if(len(susMsgs) == 0):
    #   #   print("unuse voice")
    #   #   #todo unuse
    #   #   pass
    #   mapContainer = addToMap([acbFolder, adx], mapContainer, susMsgs)
  return mapContainer

def matchAwbMsg(soundRoot, msgMap):
  # soundRoot = r"F:\Game\p5r_cpk\SOUND\EVENT"
  soundMap = {}
  # acbOnly = []

  # globalAdxCounter = 0
  acbFolderPrefix = "_vgmt_acb_ext_E"

  tempFolders = os.listdir(soundRoot)
  acbFolders = list(filter(lambda n: str(n).startswith(acbFolderPrefix), tempFolders))

  for acbFolder in acbFolders:
    try:
      awbFiles = os.listdir(os.path.join(soundRoot, acbFolder, "awb"))
    except FileNotFoundError as e:
      # print(e.filename)
      # acbOnly.append(acbFolder)
      continue
    soundMap = matchMSGLine(acbFolder, awbFiles, soundMap, msgs=msgMap)
  return soundMap



if __name__ == '__main__':
  from loadAllMsg import dumpEventDataMsg
  
  msgMap = loadJson("./Game_p5r_cpk_EVENT_DATA_MESSAGE.json")
  soundFolderRoot = r'F:\Game\p5r_cpk\SOUND\EVENT'
  matchAwbMsg(soundFolderRoot, [msgMap])

  print()
  
  soundRoot = r"F:\Game\p5r_cpk\SOUND\EVENT"

  globalAdxCounter = 0
  acbFolderPrefix = "_vgmt_acb_ext_E"

  tempFolders = os.listdir(soundRoot)
  acbFolders = list(filter(lambda n: str(n).startswith(acbFolderPrefix), tempFolders))
  soundMap = {}

  msgNotFound = []

  unuse = {}

  acbOnly = []
  msgs = loadAllLocalMsg()
  for acbFolder in acbFolders:
    try:
      awbFiles = os.listdir(os.path.join(soundRoot, acbFolder, "awb"))
    except FileNotFoundError as e:
      print(e.filename)
      acbOnly.append(acbFolder)
      continue
    soundMap = matchMSGLine(acbFolder, awbFiles, soundMap, msgs=msgs)
    # print(len(awbFiles))

  with open('soundMap-readable.json', 'w', encoding='utf8') as file:
    file.write(json.dumps(soundMap, ensure_ascii=False))

  '''
  ['_vgmt_acb_ext_E119_001_SE', '_vgmt_acb_ext_E484_100_SE', '_vgmt_acb_ext_E511_220_SE', '_vgmt_acb_ext_E511_393_SE', '_vgmt_acb_ext_E511_553_SE', '_vgmt_acb_ext_E511_590_SE', '_vgmt_acb_ext_E511_596_SE', '_vgmt_acb_ext_E511_601_SE', '_vgmt_acb_ext_E511_604_SE', '_vgmt_acb_ext_E511_625_SE']
  '''

  print("acb folder only:", acbOnly)
  # print(globalAdxCounter)
  print("DONE")
