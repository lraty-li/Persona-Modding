import os, openai
from open_ai import translate
from openai_api_ket import API_KEY
import sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import loadJson, dumpJson

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
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt"
    )
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

if __name__ == "__main__":
    # trans_init_cmptable_ctd()
    # translate_init_bmds()
    translate_event_init_bmds()
