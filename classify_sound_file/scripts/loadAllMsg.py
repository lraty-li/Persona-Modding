from common import *

import os


def getAllMessage(folderRoot, config):
  msgMap = {}
  for folder in os.listdir(folderRoot):
    for file in os.listdir(os.path.join(folderRoot, folder)):
      if(file.endswith('msg')):
        msgMap = getMsgs(os.path.join(folderRoot, folder, file), msgMap, False if ConstString.ifMatchNoIndex.value in config.keys() else True)
  return msgMap


# event_data
def dumpEventDataMsg(eventDataPaths):
  # eventDataMsgs = {
  #     "".join(pathKey[3:].replace("\\", "_")): getAllMessage(pathKey, eventDataPaths[pathKey]) for pathKey in eventDataPaths
  # }
  eventDataMsgs = [
      getAllMessage(pathKey, eventDataPaths[pathKey]) for pathKey in eventDataPaths
  ]

  return eventDataMsgs


if __name__ == '__main__':

  # loadAllLocalMsg()

  msgs = {
      "".join(pathKey[3:].replace("\\", "_")): getAllMessage(pathKey, paths[pathKey]) for pathKey in paths
  }

  for i in msgs:
    with open("{}.json".format(i), 'w', encoding='utf8') as file:
      file.write(json.dumps(msgs[i], ensure_ascii=False))
  print('done')
