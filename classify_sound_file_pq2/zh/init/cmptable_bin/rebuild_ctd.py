# 把中文字符替换成字库的日文汉字
import os

import shutil
import sys

from ctd_commom import unpackedBin

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import *

sys.path.append(
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
)
from ctd_commom import targets, BLOCK_SIZE, HEADER_SIZE


workPlaceRoot = (
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
)
cacheRoot = "D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\cmptable_bin"

os.chdir(workPlaceRoot)
rebuildFolder = "rebuild"
zhJson = "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\ctd-zh.json"
jpJson = (
    "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\ctd.json"
)
zhMsg = loadJson(zhJson)
jpMsg = loadJson(jpJson)
msgMap = {}

# keep the order of msg
ctdMsgCountMap = {}
for key in jpMsg:
    ctdFile, lineIndexStr = key.split('_')
    lienIndex = int(lineIndexStr)

    if(ctdFile in ctdMsgCountMap.keys()):
        if(lienIndex < ctdMsgCountMap[ctdFile]):
            continue
    ctdMsgCountMap[ctdFile] = lienIndex
rpMsgMap = {}

for ctdF in ctdMsgCountMap:
    replacedMsgs = []
    for index in range(ctdMsgCountMap[ctdF]):
        line = zhMsg['{}_{}'.format(ctdF, index)]
        replacedLine = replaceZhToJpKanji(line)
        replacedMsgs.append(replacedLine)
    rpMsgMap[ctdF] = replacedMsgs
    with open(os.path.join(workPlaceRoot, rebuildFolder, ctdF), "wb") as file:
        # header
        header = ""
        with open(os.path.join(cacheRoot, ctdF), "rb") as valFile:
            header = valFile.read(HEADER_SIZE)
        file.write(header)
        # msg block
        index = 0
        for msg in replacedMsgs:
            containerBytes = []
            for char in msg:
                try:
                    containerBytes += char.encode("shiftjis")
                except UnicodeEncodeError as e:
                    print("ERROR: No shiftjis encoding of {} in {}".format(char, ctdF))
                    containerBytes += " ".encode("shiftjis")
            byteSub = BLOCK_SIZE - len(containerBytes)
            if byteSub < 0:
                print("WARN msg too long: {}".format(jpMsg[ctdF][index]))
                containerBytes = containerBytes[:32]
            else:
                containerBytes += [0] * byteSub
            file.write(bytes(containerBytes))
            index += 1
        # end
        file.write(header)

#TODO ctd_common
rebuildCtdRoot = (
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\rebuild"
)

for targ in targets:
    shutil.copy(os.path.join(rebuildCtdRoot, targ), os.path.join(unpackedBin, targ))

# dumpJson(zhJson.replace(".json", "-rp.json"), rpMsgMap)
