import os
from scripts.common import dumpJson, ConstString, loadJson
from scripts.loadAllMsg import dumpEventDataMsg
from scripts.single_line_event import dumpAllSngLineMsgs
from scripts.field_hit_init_msg import dumpAllsndVoiceDNGSetUpPaths
from scripts.gather_MEG_VOICE import matchAwbMsg
from datetime import datetime

msgFolderRoot = r'F:\Game\p5r_cpk\SC'

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
    ('FIELD', 'HIT'),
    ('FIELD', 'INIT'),
    ('SCRIPT', 'FIELD'),
]

# unpack all bmd/bf


def unPackAll(sndVoiceDNGSetUpPaths, eventDataPaths, singleLineEventIdPaths, charset='p5R_chinese_sim'):
  dumpTargetPaths = [
      *list(eventDataPaths.keys()),
      *singleLineEventIdPaths,
      *sndVoiceDNGSetUpPaths
  ]
  for dumpPath in dumpTargetPaths:
    for root, _, fileNames in os.walk(dumpPath):
      targetFiles = [i for i in fileNames if(i.endswith('.BF') or i.endswith('.BMD'))]
      for name in targetFiles:
        # TODO P5R_Japanese
        os.system(deCompilerPath + " " + os.path.join(root, name) + " " + "-Decompile -Library P5 -Encoding {}".format(charset))


def getMsgMap(sndVoiceDNGSetUpPaths, eventDataPaths, singleLineEventIdPaths):
  msgMap = []
  # SND_VOICE_DNGEVT_SETUP flow
  msgMap += dumpAllsndVoiceDNGSetUpPaths(msgFolderRoot, sndVoiceDNGSetUpPaths)

  # event_data
  msgMap += dumpEventDataMsg(eventDataPaths)

  # single line event, flow
  msgMap += dumpAllSngLineMsgs(singleLineEventIdPaths)
  return msgMap


if __name__ == '__main__':
  msgMapName = "msgMap-{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
  soundMapName = "soundMap-{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

  # unPackAll(
  #     [os.path.join(msgFolderRoot, *i) for i in sndVoiceDNGSetUpPaths],
  #     eventDataPaths,
  #     singleLineEventIdPaths)

  # msgMap = getMsgMap(sndVoiceDNGSetUpPaths, eventDataPaths, singleLineEventIdPaths)
  # dumpJson(msgMapName, msgMap)

  msgMapName = 'E:\Code\Git\Persona-Modding\classify_sound_file\msgMap-2023-04-12-01-21-06.json'
  msgMap = loadJson(msgMapName)
  # match awbs
  soundMap = matchAwbMsg(soundFolderRoot, msgMap)
  dumpJson(soundMapName, soundMap)
