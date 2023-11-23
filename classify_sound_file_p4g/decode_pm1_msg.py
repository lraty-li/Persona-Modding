import os
surrgateFile = r'E:\Code\Git\Persona-Modding\zh_hans_for_megaten-fusion-tool\p4.tsv.txt'

SURROGATE_LENGTH = 13


def loadSurrgate(filePath=surrgateFile):
  surrgateMap = {}  # high surrg : low surrg : char
  with open(filePath, 'r', encoding='utf8') as file:
    lines = file.readlines()
    for line in lines:
      parts = line.split(' ')
      try:
        surrgateMap[parts[1]].update({parts[2]: parts[0]})
      except KeyError as e:
        surrgateMap[parts[1]] = {parts[2]: parts[0]}
  return surrgateMap


surrgateMap = loadSurrgate()  # global

# def handleLine(line):
#   length = len(line)
#   index = 0
#   while (index < length - 1):
#     char = line[index]
#     if (char == '['):
#       if (line[index + 1] == 'x'):
#         highSurrg = line[index+5:index+8]
#         lowSurrg = line[index+10:index+12]
#         rawSurrg = line[index:index+SURROGATE_LENGTH]
#     index += 1
#   pass


def translaterMSG(filePath):
  global surrgateMap
  translatedContenet = ''
  # translate [x 0xXX 0xXX]
  with open(filePath, 'r', encoding='utf8') as file:

    contenet = file.read()
    index = 0
    length = len(contenet)
    while (index < length):
      char = contenet[index]
      if (char == '['):
        if (contenet[index + 1] == 'x'):
          highSurrg = contenet[index+5:index+7]
          lowSurrg = contenet[index+10:index+12]
          try:  # 大小写
            translatedChar = surrgateMap[highSurrg][lowSurrg]
          except KeyError as e:
            translatedChar = contenet[index:index+SURROGATE_LENGTH]  # not found, do nothing
          translatedContenet += translatedChar
          index += SURROGATE_LENGTH
          continue
      translatedContenet += char
      index += 1
  splited = os.path.split(filePath)
  filename = splited[1]
  ouputFile = os.path.join(splited[0], '{}-translated'.format(splited[1]))
  with open(ouputFile, 'w+', encoding='utf8') as file:
    file.write(translatedContenet)

  return translatedContenet


def translateAllMsg(root):
  for root, dirs, files in os.walk(root):
    for name in files:
      if (name.endswith('.msg')):
        traslatedContenet = translaterMSG(os.path.join(root, name))


if __name__ == '__main__':
  eventRoot = r'E:\Temp\p4g_text\data_ck.cpk_unpacked\event'
  data = translateAllMsg(eventRoot)
  print("DONE")
