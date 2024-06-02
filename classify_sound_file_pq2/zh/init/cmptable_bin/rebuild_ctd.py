# 把中文字符替换成字库的日文汉字
import os

import shutil
import sys

sys.path.append(
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
)
from ctd_commom import unpackedBin as ctdUnpackedBin

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import loadJson, replaceZhToJpKanji

sys.path.append(
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
)
from ctd_commom import targets, BLOCK_SIZE, HEADER_SIZE


def rebuildCtd():
    workPlaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
    )
    cacheRoot = (
        "D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\cmptable_bin"
    )

    os.chdir(workPlaceRoot)
    rebuildFolder = "rebuild"
    zhJson = "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\ctd-parts-zh.json"
    jpJson = "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\ctd.json"
    zhMsg = loadJson(zhJson)
    jpMsg = loadJson(jpJson)
    msgMap = {}

    # keep the order of msg
    ctdMsgCountMap = {}
    for key in jpMsg:
        ctdFile, lineIndexStr = key.split("_")
        lienIndex = int(lineIndexStr)

        if ctdFile in ctdMsgCountMap.keys():
            if lienIndex < ctdMsgCountMap[ctdFile]:
                continue
        ctdMsgCountMap[ctdFile] = lienIndex
    rpMsgMap = {}

    for ctdF in ctdMsgCountMap:
        if ctdF == "cmpConfigItem.ctd":
            print()
        replacedMsgs = []
        for index in range(
            ctdMsgCountMap[ctdF] + 1
        ):  # BUG ctdMsgCountMap[ctdF]是最大索引，range的话会少一位，应该 +1
            line = zhMsg["{}_{}".format(ctdF, index)]
            replacedLine = replaceZhToJpKanji(line)
            replacedMsgs.append(replacedLine)
        rpMsgMap[ctdF] = replacedMsgs
        rebuildCtdBytes = b""
        oriHeader = b""
        with open(os.path.join(cacheRoot, ctdF), "rb") as valFile:
            oriHeader = valFile.read(HEADER_SIZE)
        if True:
            # header
            rebuildCtdBytes += oriHeader
            # msg block
            index = 0
            for msg in replacedMsgs:
                containerBytes = list(msg.encode("shiftjis"))
                byteSub = BLOCK_SIZE - len(containerBytes)
                if byteSub < 0:
                    print("WARN msg too long: {}".format(msg))
                    containerBytes = containerBytes[:BLOCK_SIZE]
                else:
                    containerBytes += [0] * byteSub
                rebuildCtdBytes += bytes(containerBytes)
                index += 1
            # end
            rebuildCtdBytes += oriHeader
            with open(os.path.join(workPlaceRoot, rebuildFolder, ctdF), "wb") as file:
                file.write(rebuildCtdBytes)

    # TODO ctd_common
    rebuildCtdRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\rebuild"

    for targ in targets:
        shutil.copy(
            os.path.join(rebuildCtdRoot, targ), os.path.join(ctdUnpackedBin, targ)
        )

    # dumpJson(zhJson.replace(".json", "-rp.json"), rpMsgMap)


if __name__ == "__main__":
    rebuildCtd()
