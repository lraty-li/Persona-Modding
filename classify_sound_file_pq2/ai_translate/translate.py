import os, openai
from open_ai import translate
from openai_api_ket import API_KEY
import sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import loadJson, dumpJson

client = openai.OpenAI(
    api_key=API_KEY,
    base_url="https://api.v36.cm/v1/",
)


def trans_init_cmptable_ctd():
    workplaceRoot = (
        "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
    )
    os.chdir(workplaceRoot)
    # ctds = [i for i in files if i.endswith("ctd")]
    ctdJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\ctd.json"
    msgs = loadJson(ctdJsonPath)
    msgMap = {}
    for ctdF in msgs:
        jpLine = msgs[ctdF]
        zhMsg = translate(client, jpLine)
        # zhMsg = "debug"
        print("{} | {}".format(msgs[ctdF], zhMsg))
        msgMap[ctdF] = zhMsg
    dumpJson(ctdJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_init_bmds():
    workplaceRoot = (
        "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
    )
    os.chdir(workplaceRoot)
    bmdJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\bmd-parts.json"
    bmdMsgLines = loadJson(bmdJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        zhMsg = translate(client, jpLine)
        # zhMsg = "daw"
        print("{} | {}".format(jpLine, zhMsg))
        msgMap[bmdF] = zhMsg
    dumpJson(bmdJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_event_init_bmds():
    workplaceRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt"
    os.chdir(workplaceRoot)
    bmdJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt\bmd-parts.json"
    bmdMsgLines = loadJson(bmdJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        zhMsg = translate(client, jpLine)
        # zhMsg = "daw"
        print("{} | {}".format(jpLine, zhMsg))
        msgMap[bmdF] = zhMsg
    dumpJson(bmdJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_battle_message_mbm():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message"
    )
    os.chdir(workplaceRoot)
    mbmJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\mbm-parts.json"
    outputPath = mbmJsonPath.replace(".json", "-zh.json")
    lastKey = readLastKey(outputPath)
    mbmMsgLines = loadJson(mbmJsonPath)
    mbmKeys = []
    msgMap = {}
    mbmMsgLinesKeys = list(mbmMsgLines.keys())
    if len(lastKey) > 0:
        mbmKeys = mbmMsgLinesKeys[mbmMsgLinesKeys.index(lastKey) + 1 :]
        msgMap = loadJson(outputPath)
    else:
        mbmKeys = mbmMsgLinesKeys

    # flatten
    # mbmMsgLines = {}
    # for targFile in data:
    #     msgLinesOfFile = data[targFile]
    #     for lineKey in msgLinesOfFile:
    #         mbmMsgLines[lineKey] = msgLinesOfFile[lineKey]
    for mbmF in mbmKeys:
        jpLine = mbmMsgLines[mbmF]
        try:
            zhMsg = translate(client, jpLine)
        except Exception as e:
            print(e)
            break
        print("{} | {}".format(jpLine, zhMsg))
        msgMap[mbmF] = zhMsg
    dumpJson(outputPath, msgMap)


def readLastKey(filePath):
    if os.path.exists(filePath):
        data = loadJson(filePath)
        return list(data.keys())[-1]  # no order, set substance?
    else:
        return ""

def translate_battle_message_bmds():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message"
    )
    os.chdir(workplaceRoot)
    bmdJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\bmd-parts.json"
    bmdMsgLines = loadJson(bmdJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        zhMsg = translate(client, jpLine)
        # zhMsg = "daw"
        print("{} | {}".format(jpLine, zhMsg))
        msgMap[bmdF] = zhMsg
    dumpJson(bmdJsonPath.replace(".json", "-zh.json"), msgMap)

def translate_tutorial_scr_msgs():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\tutorial\scr"
    )
    os.chdir(workplaceRoot)
    bmdJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\tutorial\scr\msg-parts.json"
    bmdMsgLines = loadJson(bmdJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        zhMsg = translate(client, jpLine)
        # zhMsg = "daw"
        print("{} | {}".format(jpLine, zhMsg))
        msgMap[bmdF] = zhMsg
    dumpJson(bmdJsonPath.replace(".json", "-zh.json"), msgMap)



if __name__ == "__main__":
    # trans_init_cmptable_ctd()
    # translate_init_bmds()
    # translate_event_init_bmds()
    # translate_battle_message_mbm()
    # translate_battle_message_bmds()
    translate_tutorial_scr_msgs()
