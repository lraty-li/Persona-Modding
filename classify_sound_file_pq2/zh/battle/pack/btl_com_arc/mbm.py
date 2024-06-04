import os
from pathlib import Path
import sys


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import (
    writeBinFile,
    dumpJson,
    cacheRoot,
    loadJson,
    valueToLittleBytes,
    fillToBytes,
)
from mbm_common import decodeAllMbm, flattenTheMap
from zh_common import replaceZhToJpKanji
from mbm_common import (
    reJoinToBytes,
    MBM_HEADER_TEMPLATE,
    MSG_COUNT_OFFSET,
    HEADER_SIZE,
    MSG_INFO_SIZE,
    MSG_NO_OFFSET,
    MSG_SIZE_OFFSET,
    MSG_OFFSET,
)


def collectMsg():

    msgMap = decodeAllMbm(targets)
    flattenMsgMap = flattenTheMap(msgMap)
    outputJpJson = Path().joinpath(codeWorkplace, "mbm.json")
    dumpJson(outputJpJson, msgMap)
    outputJpJsonP = Path(outputJpJson)
    dumpJson(
        Path().joinpath(codeWorkplace, "mbm-parts.json"),
        flattenMsgMap,
    )


def rebuildAllMbm():
    rawJson = Path().joinpath(codeWorkplace, "mbm.json")
    translatedJson = Path().joinpath(codeWorkplace, "mbm-parts-zh.json")
    rebuildMbm(rawJson, translatedJson, reBuildBinRoot)


def rebuildMbm(rawJson, translatedJson, repackCpkRoot):

    rawData = loadJson(rawJson)
    translatedMsg = loadJson(translatedJson)
    msgMap = {}
    targets = []
    for file in rawData:
        msgMap[file] = []
        targets.append(file)
        msgInfos = rawData[file]
        for msgInfoIndex in range(len(msgInfos)):
            msgInfo = msgInfos[msgInfoIndex]
            msgs = msgInfo[0]
            ctlStrs = rawData[file][msgInfoIndex][1]
            transedMsgLines = []
            for index in range(len(msgs)):
                transMsg = translatedMsg["{}_{}_{}".format(file, msgInfoIndex, index)]
                transedMsgLines.append(transMsg)
            transedMsgLinesRp = []
            for line in transedMsgLines:
                replacedLine = replaceZhToJpKanji(line)
                # DEBUG
                transedMsgLinesRp.append(replacedLine)
                # transedMsgLinesRp.append(line)
                # DEBUG END
            msgBytes = reJoinToBytes(ctlStrs, transedMsgLinesRp)
            msgMap[file].append(msgBytes)

    # rebuild mbm files
    for targ in targets:
        msgLines = msgMap[targ]
        msgCount = len(msgLines)
        # build header
        fileHeader = list(bytes.fromhex(MBM_HEADER_TEMPLATE))

        msgCountBytes = valueToLittleBytes(msgCount)
        fileHeader = fillToBytes(MSG_COUNT_OFFSET, fileHeader, msgCountBytes)
        msgInfo = []
        msgArea = []
        msgAreaOffset = HEADER_SIZE + (msgCount * MSG_INFO_SIZE)
        for index in range(msgCount):
            # build msg info area
            msgInfoTempalte = list(bytes(MSG_INFO_SIZE))
            msgBytes = msgMap[targ][index]
            msgNoBytes = valueToLittleBytes(index)
            msgInfoTempalte = fillToBytes(MSG_NO_OFFSET, msgInfoTempalte, msgNoBytes)
            msgSize = len(msgBytes) + 2  # ff ff
            msgSizeBytes = valueToLittleBytes(msgSize)
            msgInfoTempalte = fillToBytes(
                MSG_SIZE_OFFSET, msgInfoTempalte, msgSizeBytes
            )
            msgOffsetBytes = valueToLittleBytes(msgAreaOffset)
            msgAreaOffset = msgAreaOffset + msgSize
            msgInfoTempalte = fillToBytes(MSG_OFFSET, msgInfoTempalte, msgOffsetBytes)
            msgInfo += msgInfoTempalte
            # build msg area
            msgArea += msgBytes
            msgArea += b"\xff\xff"
        # join all area
        mbmFileBytes = fileHeader + msgInfo + msgArea
        # TODO file size
        # just dump to repack root
        outputPath = Path().joinpath(repackCpkRoot, targ)
        writeBinFile(str(outputPath), mbmFileBytes)


targets = [
    "skillexpbattle.mbm",
    "skillexpbattle_enemy.mbm",
    "skillexpbattle_player.mbm",
]
targetBin = "btl_com.arc"
pathParts = [
    "battle",
    "pack",
]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))

cacheWorkplace = Path().joinpath(cacheRoot, *pathParts, targetBin.replace(".", "_"))
targets = [Path().joinpath(cacheWorkplace, i) for i in targets]
reBuildBinRoot = cacheWorkplace
unpackedToPath = Path(cacheWorkplace)
decompiledCacheFolder = os.path.join(
    unpackedToPath.parent, unpackedToPath.name + "_cache"
)

if __name__ == "__main__":
    # collectMsg()
    rebuildAllMbm()
