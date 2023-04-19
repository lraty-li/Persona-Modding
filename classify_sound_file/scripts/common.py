# from matplotlib.cbook import flatten
import os
import json
import re
from enum import Enum


class ConstString(Enum):
  noIndex = 'noIndex'
  ifMatchNoIndex = 'matchNoIndex'
  msgSpeaker = 'speaker'
  msgLines = 'lines'
  msgText = 'text'
  msgNodeTitle = 'title'
  vpLineSoundIndex = 'index'


paths = {
    # r"F:\Game\p5r_cpk\FIELD",
    r"F:\Game\p5r_cpk\SCRIPT": {},
    r"F:\Game\p5r_cpk\EVENT_DATA\MESSAGE": {},
    r"F:\Game\p5r_cpk\EVENT_DATA\SCRIPT": {
        ConstString.ifMatchNoIndex.value: False
    },
    r'F:\Game\p5r_cpk\FIELD\KF_EVENT': {}
}

# def cutOutScops(scopsSplitInex, functionField):
#   cuts = []
#   startingIndex = 0
#   for index in scopsSplitInex:
#     cuts.append(functionField[startingIndex])


def createFolder(folderPath):
  os.makedirs(folderPath, exist_ok=True, mode=0o777)


def getAdxId(adxName):
  return int(adxName.split('_')[1])


def cmpAdxName(s1, s2):
  id1 = getAdxId(s1)
  id2 = getAdxId(s2)
  if id1 < id2:
    return -1
  else:
    return 1


def inListCheck(target, lList):
  result = False
  for i in lList:
    if i in target:
      return True


def getFromMap(pathParts, mMap):
  if len(pathParts) == 0:
    return mMap
  mMap = getFromMap(pathParts[1:], mMap[pathParts[0]])
  return mMap


def addToMap(pathParts, mMap, target):
  if len(pathParts) == 0:
    # addTarget()
    if(type(target) == dict):
      if(type(mMap) == list):
        mMap.append(target)
      else:
        # todo 重复?
        mMap.update(target)
    elif(type(target) == list):
      if(type(mMap) == dict):
        mMap = target
      elif(len(target) != 0):
        mMap.append(*target)
    else:
      mMap = target
    return mMap
  part = pathParts[0]
  if part not in mMap.keys():
    mMap[part] = {}
  mMap[part] = addToMap(pathParts[1:], mMap[part], target)
  return mMap


def addVplines(event, msgNodes, msgMap, matchNoIndex=True):
  vpLines, vpLinesNoIndex = getVpLines(msgNodes)
  # if(len(vpLines) == 0):
  #   return msgMap
  if not matchNoIndex:
    vpLinesNoIndex.clear()

  eventIds = re.findall(r'[0-9]+', event)

  if(len(vpLines) != 0 and len(vpLinesNoIndex) != 0):
    # print("both type vp line", event)
    pass

  if(len(vpLines) > 1):
    msgMap = addToMap(eventIds, msgMap, vpLines)
  if(len(vpLinesNoIndex) > 1):
    msgMap = addToMap([*eventIds, ConstString.noIndex.value], msgMap, [vpLinesNoIndex])
  return msgMap


def getMsgs(msgFilePath, msgMap, matchNoIndex=True):
  msgNodes = loadMsgFile(msgFilePath)
  # todo 记录？
  # bypass test
  if(inListCheck(msgFilePath, ['TEST', 'PV', 'BK'])):
    # if('TEST' in msgFilePath or 'PV' in msgFilePath or 'BK' in msgFilePath):
    return msgMap
  if(msgFilePath == r'F:\Game\p5r_cpk\FIELD\KF_EVENT\HIT\EHIT_181_101_00.BF.msg'):
    print()
  # event id 来源
  eventInPath = re.search(r"([0-9]+_)+([0-9]+)", msgFilePath)
  if(eventInPath != None):
    event = eventInPath.group(0)
    msgMap = addVplines(event, msgNodes, msgMap, matchNoIndex)
  else:
    headerMatchers = map(lambda nodeHead: re.search(r"e[0-9]+_[0-9]+", nodeHead), msgNodes.keys())
    headerMatchers = list(filter(lambda matchResult: matchResult != None, headerMatchers))
    if(len(headerMatchers) == 0):
      return msgMap
    msgHeaders = tuple(set(match.group(0) for match in headerMatchers))
    for event in msgHeaders:
      subMsgNodesHeader = [header for header in msgNodes.keys() if event in header]
      subMsgNodes = {header: msgNodes[header] for header in subMsgNodesHeader}
      msgMap = addVplines(event, subMsgNodes, msgMap, matchNoIndex)
  # if(len(msgMap.keys()) != 0):
  #   print()
  return msgMap

# def isMsgHeaderWithSpeaker(line):
#   temp = "[msg e489_230_jose03 [约瑟]]"


def isVoice(line):
  # bypass vp 8 0 0 0
  # TODO 记录 [vp 8 0 0 0
  # if 'vp 8 0 0 0' in line:
  #   return False
  if (inListCheck(line, ['vp 8 0', 'vp 1 0', 'vp 6 0'])):
    # if "vp 8 0" in line or "vp 1 0" in line or "vp 6 0":
    return True
  else:
    return False


def cutLine(line):
  # tagStarts = [i for i, x in enumerate(line) if x == "["]
  # tagEnds = [i for i, x in enumerate(line) if x == "]"]

  index = 0
  text = ""
  tags = []
  vpTags = []

  tags = re.findall(r'\[[\w| ]+\]', line)
  texts = re.findall(r'(?<=\])[^\[]+(?=\[)', line)
  text = "".join(texts)
  # # cut out tags
  # for i, j in zip(tagStarts, tagEnds):
  #   tags.append(line[i:j+1])

  # # cut out text
  # joinedList = list(zip(tagEnds[:-1], tagStarts[1:]))
  # flatedJoinedList = list(flatten(joinedList))
  # for i, j in joinedList:
  #   if abs(j - i) == 1:
  #     flatedJoinedList.remove(i)
  #     flatedJoinedList.remove(j)
  # if(len(flatedJoinedList) == 0):
  #   return text, vpTags
  #   # no text
  #   # MSG_025_5_0 E400\E409_001.BMD.msg
  # text = line[flatedJoinedList[0] + 1: flatedJoinedList[-1]]

  # pre prgress

  for tag in tags:
    if isVoice(tag):
      vpTags.append(tag)
  return text, vpTags


def dumpJson(filePath, obj, sureAscii=False):
  if(not filePath[-5:] == '.json'):
    filePath += '.json'
  with open(filePath, 'w', encoding='utf8') as file:
    file.write(json.dumps(obj, ensure_ascii=sureAscii))


def loadJson(filePath):
  if(not filePath[-5:] == '.json'):
    filePath += '.json'
  with open(filePath, 'r', encoding='utf8') as file:
    return json.load(file)


def loadAllLocalMsg():
  filenames = ["{}.json".format("".join(path[3:].replace("\\", "_"))) for path in paths]

  jsons = []
  for fileName in filenames:
    jsons.append(loadJson(fileName))
  # DEUG BEGIN
  # jsons += loadJson("./script_out.json")
  # jsons.append(loadJson("./field_npc.json"))
  # jsons.append(loadJson("./camp_chat.json"))

  # DEBUG END
  return jsons


def loadMsgFile(msgFilePath):
  msgNodes = {}
  with open(msgFilePath, "r", encoding='utf8') as msgFile:
    lines = msgFile.readlines()
    index = 0
    while index < len(lines):
      line = lines[index]
      jumpCounter = 1
      # todo real [] parser
      if "[msg" in line:
        msgKey = line.split(" ")[1]
        msgNodes["{}".format(msgKey)] = {ConstString.msgSpeaker.value: line.split(msgKey)[1][2:-3], ConstString.msgLines.value: []}
        # dont care out bound
        tempLine = lines[index+jumpCounter]
        while tempLine != "\n":
          jumpCounter += 1
          # todo 会不会重复?
          msgNodes[msgKey][ConstString.msgLines.value].append(tempLine)
          tempLine = lines[index+jumpCounter]

        index += jumpCounter
      else:
        index += 1
    return msgNodes


def getVpTagIndex(vpTag):
  return vpTag.split(" ")[4]


def getVpLines(msgNodes):
  vpLinesMap = {}
  vpLinesNoIndex = []
  # msgFilePath = r"F:\Game\p5r_cpk\EVENT_DATA\MESSAGE\E700\E702_011.BMD.msg"
  # msgNodes = loadMsgFile(msgFilePath)
  # collect vp lines
  for node in msgNodes:
    lines = msgNodes[node][ConstString.msgLines.value]
    speaker = msgNodes[node][ConstString.msgSpeaker.value]
    for line in lines:
      if isVoice(line):
        text, vpTags = cutLine(line)
        if(len(vpTags) == 0 or len(text) == 0):
          continue
        vpLineIndexing = getVpTagIndex(vpTags[0])
        if(len(vpTags) > 1):
          # todo 按照多条重复添加？
          # 取最靠近text的vp tag
          print("muti vp tags in \n {}".format(line))
          vpLineIndexing = getVpTagIndex(vpTags[-1])
        data = {
            ConstString.msgText.value: text,
            ConstString.msgSpeaker.value: speaker,
            ConstString.msgNodeTitle.value: node
        }
        if vpLineIndexing == '0':
          # 顺序问题, msgNodes 逐行处理，应该没问题
          vpLinesNoIndex.append(data)
        else:
          # TODO 同一个文件同index是可能的，script按照message node header各自索引音频
          vpLinesMap[vpLineIndexing] = data

  return vpLinesMap, vpLinesNoIndex


def getVpLinesNew(msgNodes):
  vpLinesMap = {}
  # collect vp lines
  for node in msgNodes:
    lines = msgNodes[node][ConstString.msgLines.value]
    speaker = msgNodes[node][ConstString.msgSpeaker.value]
    for line in lines:
      if isVoice(line):
        text, vpTags = cutLine(line)
        if(len(vpTags) == 0 or len(text) == 0):
          continue
        vpLineIndexing = getVpTagIndex(vpTags[0])
        if(len(vpTags) > 1):
          # todo 按照多条重复添加？
          # 取最靠近text的vp tag
          print("muti vp tags in \n {}".format(line))
          vpLineIndexing = getVpTagIndex(vpTags[-1])
        data = {
            ConstString.msgText.value: text,
            ConstString.msgSpeaker.value: speaker,
            # ConstString.msgNodeTitle.value : node,
            ConstString.vpLineSoundIndex.value: vpLineIndexing
        }
        # 某些msg文件存储了不同event sound ref，可能id重复，通过title 索引，并且略过非声音msg的处理
        vpLinesMap = addToMap([node], vpLinesMap, [data])
        # vpLinesMap[node] = data

  return vpLinesMap
