import os
from common import dumpJson, ConstString, loadJson
from loadAllMsg import dumpEventDataMsg
from single_line_event import dumpAllSngLineMsgs
from field_hit_init_msg import dumpAllsndVoiceDNGSetUpPaths
from gather_MEG_VOICE import matchAwbMsg
from datetime import datetime

msgFolderRoot = r'F:\Game\p5r_cpk\JP'

soundFolderRoot = r'F:\Game\p5r_cpk\SOUND\EVENT'

deCompilerPath = "D:\Game\P5RModding\AtlusScriptToolchain.1\AtlusScriptCompiler.exe"

# event_data
eventDataPaths = {
    # r"F:\Game\p5r_cpk\FIELD",
    os.path.join(msgFolderRoot, 'SCRIPT'): {},
    os.path.join(msgFolderRoot, 'EVENT_DATA', 'MESSAGE'): {},
    os.path.join(msgFolderRoot, 'EVENT_DATA', 'SCRIPT'): {
        ConstString.ifMatchNoIndex.value: False
    },
    os.path.join(msgFolderRoot, 'FIELD', 'KF_EVENT'): {}
}

singleLineEventIdPaths = [
    # eventSubID;
    # eventID;

    os.path.join(msgFolderRoot, 'FIELD', 'NPC'),
    os.path.join(msgFolderRoot, 'CAMP', 'CHAT'),
]

sndVoiceDNGSetUpPaths = [
    # SND_VOICE_DNGEVT_SETUP( eventId, eventSubId)
    os.path.join(msgFolderRoot, 'FIELD', 'HIT'),
    os.path.join(msgFolderRoot, 'FIELD', 'INIT'),
    os.path.join(msgFolderRoot, 'SCRIPT', 'FIELD'),
]

# unpack all bmd/bf
def unPackAll(sndVoiceDNGSetUpPaths, eventDataPaths, singleLineEventIdPaths):
    dumpTargetPaths = [
      *list(eventDataPaths.keys()),
      *singleLineEventIdPaths,
      *sndVoiceDNGSetUpPaths
    ]
    for dumpPath in dumpTargetPaths:
      for root, _, fileNames in os.walk(dumpPath):
        targetFiles = [i for i in fileNames if(i.endswith('.BF') or i.endswith('.BMD'))]
        for name in targetFiles:
          os.system(deCompilerPath + " " + os.path.join(root, name)+ " " + "-Decompile -Library P5 -Encoding p5R_chinese_sim")


def getMsgMap(sndVoiceDNGSetUpPaths, eventDataPaths, singleLineEventIdPaths):
  msgMap = []
  # SND_VOICE_DNGEVT_SETUP flow
  msgMap += dumpAllsndVoiceDNGSetUpPaths(sndVoiceDNGSetUpPaths)

  # event_data
  msgMap += dumpEventDataMsg(eventDataPaths)

  # single line event, flow
  msgMap += dumpAllSngLineMsgs(singleLineEventIdPaths)
  dumpJson("msgMap".format(datetime.timestamp(datetime.now())), msgMap)
  return msgMap

if __name__ == '__main__':
  # unPackAll(sndVoiceDNGSetUpPaths, eventDataPaths, singleLineEventIdPaths)

  # msgMap = getMsgMap(sndVoiceDNGSetUpPaths, eventDataPaths, singleLineEventIdPaths)

  msgMap = loadJson("./msgMap-jp.json")
  # match awbs
  soundMap = matchAwbMsg(soundFolderRoot, msgMap)
  dumpJson("soundMap-jp", soundMap)
