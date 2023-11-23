import re
import os
import json

def loadMsgFile(msgFilePath):
  msgNodes = {}
  with open(msgFilePath, "r", encoding='utf8') as msgFile:
    lines = msgFile.readlines()
    index = 0
    lineCount = len(lines)
    while index < lineCount:
      line = lines[index]
      jumpCounter = 1
      # todo real [] parser
      if "[msg" in line:
        msgKey = line.split(" ")[1]
        msgKey = msgKey.replace(']\n', '')
        msgNodes["{}".format(msgKey)] = {'speaker': line.split(msgKey)[1][2:-3], 'msg_lines': []}
        # dont care out bound
        tempLine = lines[index+jumpCounter]
        while tempLine != "\n":
          jumpCounter += 1
          # todo 会不会重复?
          tempLine = tempLine.replace('\n','') # remove[-1]?
          msgNodes[msgKey]['msg_lines'].append(tempLine)
          tempLine = lines[index+jumpCounter]

        index += jumpCounter
      else:
        index += 1
    return msgNodes


def merge480(msgNodes):
  # [f 6 1 6 0 480 480] 需要就近连接
  msgTitles = [msgTitle for msgTitle in msgNodes.keys()]
  legth = len(msgTitles)
  index = 0
  while index < legth:
    
    currTitle = msgTitles[index]# 开始拉屎
    currLines = msgNodes[currTitle]['msg_lines']
    next480Lines = []
    for line in currLines:
      if ('f 6 1 6 0 480' in line):
        # 将之后的nodes的lines合并到这个node
        next480Lines.clear()
        try:
          while index < legth:
            title = msgTitles[index+1]
            nextLines = msgNodes[title]['msg_lines']
            for nextLine in nextLines:
              if (('f 6 1 6 0 480' in nextLine) and not ('f 6 1 6 2 0 ' in nextLine)):
                next480Lines.append(nextLine)
              else:
                raise Exception('stop')
            msgNodes.pop(title)
            index += 1
        except Exception as e:
          break
      # 合并为单条语音

    if (len(next480Lines) > 0):
      msgNodes[currTitle]['msg_lines'] = [''.join(currLines + next480Lines)]
    else:
      pass
    index += 1
  return msgNodes


def getMsgs(msgFilePath, msgMap):

  msgNodes = loadMsgFile(msgFilePath)
  msgNodes = merge480(msgNodes)
  os.path.split(msgFilePath)
  event = re.findall(r'(\d+)', os.path.split(msgFilePath)[-1])
  if (len(event) < 2):
    raise Exception('event may error')
  msgMap = addVplines(event, msgNodes, msgMap)
  return msgMap


def addVplines(event, msgNodes, msgMap):
  vpLines, vpLinesNoIndex = getVpLines(msgNodes)
  eventIds = event
  msgMap = addToMap(eventIds, msgMap, vpLines)
  return msgMap

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

def getVpLines(msgNodes):
  vpLinesMap = {}
  vpLinesNoIndex = []
  # msgFilePath = r"F:\Game\p5r_cpk\EVENT_DATA\MESSAGE\E700\E702_011.BMD.msg"
  # msgNodes = loadMsgFile(msgFilePath)
  # collect vp lines
  for node in msgNodes:
    lines = msgNodes[node]['msg_lines']
    speaker = msgNodes[node]['speaker']
    for line in lines:
      if isVoice(line):
        text, vpTags = cutLine(line)
        if (len(vpTags) == 0 or len(text) == 0):
          continue
        vpLineIndexing = getVpTagIndex(vpTags[0])
        if (len(vpTags) > 1):
          # 取最靠近text的vp tag
          print("muti vp tags in \n {}".format(line))
          vpLineIndexing = getVpTagIndex(vpTags[-1])
        data = {
            'text': text,
            'speaker': speaker,
            # 'title': node
        }
        if vpLineIndexing == '0':
          # 顺序问题, msgNodes 逐行处理，应该没问题
          vpLinesNoIndex.append(data)
        else:
          vpLinesMap[vpLineIndexing] = data

  return vpLinesMap, vpLinesNoIndex


def isVoice(line):
  if (inListCheck(line, ['f 6 1 6 2 0', 'f 3 1 1 0 0'])):
    return True
  else:
    return False


def getVpTagIndex(vpTag):
  return vpTag.split(" ")[-1].replace(']', '')


def inListCheck(target, lList):
  result = False
  for i in lList:
    if i in target:
      return True


def cutLine(line):
  index = 0
  text = ""
  tags = []
  vpTags = []

  tags = re.findall(r'\[[\w| ]+\]', line)
  texts = re.findall(r'(?<=\])[^\[]+(?=\[)', line)
  text = "".join(texts)

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

def createFolder(folderPath):
  os.makedirs(folderPath, exist_ok=True, mode=0o777)
