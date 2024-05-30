import os, openai
import time
import threading
from open_ai import translate
from openai_api_ket import API_KEY
import sys

MUTI_THREADING_THREADHOLD = 70
MUTI_THREADING_SLEEP = 2

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
    outputPath = ctdJsonPath.replace(".json", "-parts-zh.json")
    msgs = loadJson(ctdJsonPath)
    msgMap = {}
    for ctdF in msgs:
        jpLine = msgs[ctdF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, ctdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(outputPath, msgMap)


def translate_init_cmptable_bin_bmds():
    workplaceRoot = (
        "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
    )
    os.chdir(workplaceRoot)
    msgJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\bmd-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        zhMsg = translate(client, jpLine)
        # zhMsg = "daw"
        print("{} | {}".format(jpLine, zhMsg))
        msgMap[bmdF] = zhMsg
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_event_init_bmds():
    workplaceRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt"
    os.chdir(workplaceRoot)
    msgJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt\bmd-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        zhMsg = translate(client, jpLine)
        # zhMsg = "daw"
        print("{} | {}".format(jpLine, zhMsg))
        msgMap[bmdF] = zhMsg
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_battle_message_mbm():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message"
    )
    os.chdir(workplaceRoot)
    mbmJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\mbm-parts.json"
    outputPath = mbmJsonPath.replace(".json", "-zh.json")
    mbmMsgLines = loadJson(mbmJsonPath)
    restKey = restKeys(outputPath, mbmMsgLines)
    msgMap = {}

    # flatten
    # mbmMsgLines = {}
    # for targFile in data:
    #     msgLinesOfFile = data[targFile]
    #     for lineKey in msgLinesOfFile:
    #         mbmMsgLines[lineKey] = msgLinesOfFile[lineKey]
    # if len(restKey) > 0:
    #     msgMap = loadJson(outputPath)
    for mbmF in restKey:
        jpLine = mbmMsgLines[mbmF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, mbmF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(outputPath, msgMap)


def restKeys(filePath, flattenMap):
    restKeys = flattenMap.keys()
    if os.path.exists(filePath):
        data = loadJson(filePath)
        restKeys = restKeys - data.keys()  # no order, set substance?
    return restKeys


def mutiThreadTranslate(client, jpLine, msgMap, mbmF):
    try:
        zhMsg = translate(client, jpLine)
        # TODO zhMsg may be None?
        zhMsg = "{}".format(zhMsg)
    except Exception as e:
        print(e)
        zhMsg = "ERROR"
    print("{} | {}".format(jpLine, zhMsg))
    msgMap[mbmF] = zhMsg


def translate_item_mbm():
    initThreadCount = threading.active_count()
    workplaceRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\item"
    os.chdir(workplaceRoot)
    mbmJsonPath = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\item\mbm-parts.json"
    )
    outputPath = mbmJsonPath.replace(".json", "-zh.json")
    mbmMsgLines = loadJson(mbmJsonPath)
    restKey = restKeys(outputPath, mbmMsgLines)
    msgMap = {}
    # if len(restKey) > 0:
    #     msgMap = loadJson(outputPath)
    for mbmF in restKey:
        jpLine = mbmMsgLines[mbmF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, mbmF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(outputPath, msgMap)


def translate_battle_message_bmds():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message"
    )
    os.chdir(workplaceRoot)
    msgJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\bmd-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, bmdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_tutorial_scr_msgs():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\tutorial\scr"
    )
    os.chdir(workplaceRoot)
    msgJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\tutorial\scr\msg-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        zhMsg = translate(client, jpLine)
        # zhMsg = "daw"
        print("{} | {}".format(jpLine, zhMsg))
        msgMap[bmdF] = zhMsg
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def trans_init_fcltable_ftd():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin"
    )
    os.chdir(workplaceRoot)
    # ctds = [i for i in files if i.endswith("ctd")]
    ctdJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin\ftd.json"
    msgs = loadJson(ctdJsonPath)
    msgMap = {}
    for ftdF in msgs:
        jpLine = msgs[ftdF][0]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, ftdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(ctdJsonPath.replace(".json", "-parts-zh.json"), msgMap)


def translate_battle_event_msgs(msgJsonPath):
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event"
    )
    os.chdir(workplaceRoot)
    msgLines = loadJson(msgJsonPath)
    msgMap = {}
    for msgF in msgLines:
        jpLine = msgLines[msgF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, msgF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_battle_support_message_bmds():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\support\message"
    )
    os.chdir(workplaceRoot)
    msgJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\support\message\bmd-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, bmdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_item_tbl():
    initThreadCount = threading.active_count()
    workplaceRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\item"
    os.chdir(workplaceRoot)
    mbmJsonPath = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\item\tbl-parts.json"
    )
    outputPath = mbmJsonPath.replace(".json", "-zh.json")
    mbmMsgLines = loadJson(mbmJsonPath)
    restKey = restKeys(outputPath, mbmMsgLines)
    msgMap = {}
    # if len(restKey) < len(mbmMsgLines):
    #     msgMap = loadJson(outputPath)
    for mbmF in restKey:
        jpLine = mbmMsgLines[mbmF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, mbmF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(outputPath, msgMap)


def translate_battle_table_tbl():
    initThreadCount = threading.active_count()
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\table"
    )
    os.chdir(workplaceRoot)
    mbmJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\table\tbl-parts.json"
    outputPath = mbmJsonPath.replace(".json", "-zh.json")
    mbmMsgLines = loadJson(mbmJsonPath)
    restKey = restKeys(outputPath, mbmMsgLines)
    msgMap = {}
    # if len(restKey) < len(mbmMsgLines):
    #     msgMap = loadJson(outputPath)
    for mbmF in restKey:
        jpLine = mbmMsgLines[mbmF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, mbmF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(outputPath, msgMap)


def translate_battle_facility_bmds():
    workplaceRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility"
    os.chdir(workplaceRoot)
    msgJsonPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\bmd-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, bmdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_battle_message_tbl():
    initThreadCount = threading.active_count()
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message"
    )
    os.chdir(workplaceRoot)
    mbmJsonPath = os.path.join(workplaceRoot, "tbl-parts.json")
    outputPath = mbmJsonPath.replace(".json", "-zh.json")
    mbmMsgLines = loadJson(mbmJsonPath)
    restKey = restKeys(outputPath, mbmMsgLines)
    msgMap = {}
    # if len(restKey) < len(mbmMsgLines):
    #     msgMap = loadJson(outputPath)
    for mbmF in restKey:
        jpLine = mbmMsgLines[mbmF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, mbmF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(outputPath, msgMap)


def translate_facility_msgs(msgJsonPath):
    # workplaceRoot = (
    #     r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event"
    # )
    # os.chdir(workplaceRoot)
    msgLines = loadJson(msgJsonPath)
    msgMap = {}
    for msgF in msgLines:
        jpLine = msgLines[msgF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, msgF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_init_bmds():
    workplaceRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init"
    os.chdir(workplaceRoot)
    msgJsonPath = r"bmd-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, bmdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_init_itemtbl_bin():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\itemtbl_bin"
    )
    os.chdir(workplaceRoot)
    msgJsonPath = r"itemtbl.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, bmdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_facility_pack_shop_arc_bmd():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\pack\shop_arc"
    )
    os.chdir(workplaceRoot)
    msgJsonPath = r"bmd-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, bmdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_facility_pack_shop_arc_bf(msgJsonPath):
    # workplaceRoot = (
    #     r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event"
    # )
    # os.chdir(workplaceRoot)
    msgLines = loadJson(msgJsonPath)
    msgMap = {}
    for msgF in msgLines:
        jpLine = msgLines[msgF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, msgF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_facility_pack_shop_arc_bmd():
    workplaceRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\pack\cmbroot_arc"
    os.chdir(workplaceRoot)
    msgJsonPath = r"bmd-parts.json"
    bmdMsgLines = loadJson(msgJsonPath)
    msgMap = {}
    for bmdF in bmdMsgLines:
        jpLine = bmdMsgLines[bmdF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, bmdF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)


def translate_facility_pack_cmbroot_arc_bf(msgJsonPath):
    msgLines = loadJson(msgJsonPath)
    msgMap = {}
    for msgF in msgLines:
        jpLine = msgLines[msgF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, msgF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)

def translate_Json(msgJsonPath):
    msgLines = loadJson(msgJsonPath)
    msgMap = {}
    for msgF in msgLines:
        jpLine = msgLines[msgF]
        while threading.active_count() > MUTI_THREADING_THREADHOLD:
            time.sleep(MUTI_THREADING_SLEEP)
        t = threading.Thread(
            target=mutiThreadTranslate, args=(client, jpLine, msgMap, msgF)
        )
        t.start()
    while threading.active_count() != 1:
        time.sleep(MUTI_THREADING_SLEEP)
    dumpJson(msgJsonPath.replace(".json", "-zh.json"), msgMap)

if __name__ == "__main__":
    # trans_init_cmptable_ctd()
    # translate_init_cmptable_bin_bmds()
    # translate_event_init_bmds()
    # translate_battle_message_mbm()
    # translate_battle_message_bmds()
    # translate_tutorial_scr_msgs()
    # translate_item_mbm()
    # trans_init_fcltable_ftd()
    # translate_battle_event_msgs(
    #     r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg-parts.json"
    # )
    # translate_battle_event_msgs(
    #     r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg-bgm-parts.json"
    # )
    # translate_battle_event_msgs(
    #     r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg-support-parts.json"
    # )
    # translate_battle_support_message_bmds()
    # translate_item_tbl()
    # translate_battle_table_tbl()
    # translate_battle_facility_bmds()
    # translate_battle_message_tbl()
    # translate_facility_msgs(
    #     r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\msg-parts.json"
    # )
    # translate_init_bmds()
    # translate_init_itemtbl_bin()
    # translate_facility_pack_shop_arc_bmd()
    # translate_facility_pack_shop_arc_bf(
    #     r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\pack\shop_arc\msg-parts.json"
    # )
    # translate_facility_pack_shop_arc_bmd()
    # translate_facility_pack_cmbroot_arc_bf(
    #     r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\pack\cmbroot_arc\msg-parts.json"
    # )
    translate_Json(r'D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\support\bvp-Bmd-parts.json')
