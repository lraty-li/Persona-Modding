from common import getMsgs,dumpJson
import os

def loadAllMsg(eventRoot, msgMap):
  for root, dirs, files in os.walk(eventRoot):
    for name in files:
      if (name.endswith('.msg-translated')):
        getMsgs(os.path.join(root, name), msgMap, )
  return msgMap

if __name__ == '__main__':

  msgMap = {}
  eventRoot = r'E:\Temp\p4g_text\data_ck.cpk_unpacked\event'
  msgMap = loadAllMsg(eventRoot, msgMap)
  dumpJson('./msgMap.json', msgMap)
    
  print('DONE')
