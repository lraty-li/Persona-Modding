import os, shutil, re
from pathlib import Path
import sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import (
    dumpJson,
    getReveBinValue,
    loadJson,
    cacheRoot,
    oriCPKRoot,
    rebuildCPKRoot,
)
from zh_common import unpackBin, replaceZhToJpKanji


workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin"

# [i for i in os.listdir('.') if i.endswith('ctd')]


os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin")

HEADER_SIZE = 16


def bytesListToIntList(bytesList):
    if type(bytesList) == bytes:
        bytesList = [bytesList]
    return [[byte for byte in bBytes] for bBytes in bytesList]


def parseFtd(filePath):
    rawBytes = []
    allByteSplited = []
    msgs = []
    with open(filePath, "rb") as file:
        rawBytes = file.read()
    rawBytesLength = len(rawBytes)
    fileHeader = rawBytes[:HEADER_SIZE]
    endOfFile = []
    index = HEADER_SIZE

    blockSize = int(getReveBinValue(fileHeader[:4]) / getReveBinValue(fileHeader[4:8]))
    # 根据 '行宽' 把文件分块
    while index < rawBytesLength:
        remainByteCount = rawBytesLength - index
        if remainByteCount < blockSize:
            if remainByteCount != HEADER_SIZE:
                # raise Exception("Not header and implement")
                pass
            endOfFile = rawBytes[index:]
            break
        msgBytes = rawBytes[index : index + blockSize]
        allByteSplited.append(msgBytes)
        index += blockSize
    # header + allByteSplited + ender 应该与原文件一致
    # 把message 部分处理，按 00 切断
    for splitedBytes in allByteSplited:
        partStartIndex = 0
        msgParts = []
        reFindIter = re.finditer(b"\x00+", splitedBytes)
        for matchedIndex in reFindIter:
            start = matchedIndex.start(0)
            msgParts.append(splitedBytes[partStartIndex:start])
            end = matchedIndex.end(0)
            msgParts.append(splitedBytes[start:end])
            partStartIndex = end
        # 选去掉 \x 00 后的最长的作为 'message' ？
        noZeroMsgParts = [i.replace(b"\x00", b"") for i in msgParts]
        partLengths = [len(i) for i in noZeroMsgParts]
        longestIndex = partLengths.index(max(partLengths))
        # 直接 decode 应该没问题吧
        msgBytes = msgParts[longestIndex]
        msg = msgBytes.decode("shiftjis")
        noMsgBytes = (
            msgParts[:longestIndex] + msgParts[longestIndex + 1 :]
        )  # BUG? longestIndex + 1 越界？
        noMsgIntList = bytesListToIntList(noMsgBytes)
        msgs.append([msg, noMsgIntList, longestIndex])  # longestIndex 用于rejoin,
    msgs.insert(0, ["", bytesListToIntList(fileHeader), 0])
    msgs.append(["", bytesListToIntList(endOfFile), 0])
    return msgs



def collectMsg():
    msgMap = {}

    for target in ftdTargets:
        # if target == "cmpDifficultItem.ctd":
        #     print()
        msgs = []
        ctdLines = parseFtd(os.path.join(unpacedkWorkplace, target))
        for lineIndex in range(len(ctdLines)):
            msgMap["{}_{}".format(target, lineIndex)] = ctdLines[lineIndex]

    dumpJson(str(ftdJsonPath), msgMap)
    msgMapParts = {}
    for i in msgMap:
        msgMapParts[i] = msgMap[i][0]
    dumpJson(str(ftdPartsJsonPath), msgMapParts)


def rebuildFtd():
    zhJson = str(ftdPartsJsonPath).replace("-parts.json", "-parts-zh.json")
    zhMsg = loadJson(zhJson)
    jpMsg = loadJson(ftdJsonPath)

    # keep the order of msg
    ctdMsgCountMap = {}
    for key in jpMsg:
        spliterIndex = key.rfind("_")
        ctdFile = key[:spliterIndex]
        lineIndexStr = key[spliterIndex + 1 :]
        lienIndex = int(lineIndexStr)

        if ctdFile in ctdMsgCountMap.keys():
            if lienIndex < ctdMsgCountMap[ctdFile]:
                continue
        ctdMsgCountMap[ctdFile] = lienIndex

    rpMsgMap = {}
    for ctdF in ctdMsgCountMap:
        replacedMsgs = []
        headerBytesList = jpMsg["{}_{}".format(ctdF, 0)][1][0]
        endOfFileBytesList = []
        eofBytesListlist = jpMsg["{}_{}".format(ctdF, ctdMsgCountMap[ctdF])][1]
        if len(eofBytesListlist) > 0:
            # 可能会没有文件尾
            endOfFileBytesList = eofBytesListlist[0]
        msgBytesList = []
        for index in range(1, ctdMsgCountMap[ctdF]):
            jpMapKey = "{}_{}".format(ctdF, index)
            line = zhMsg["{}_{}".format(ctdF, index)]
            jpLine = jpMsg[jpMapKey][0]
            replacedLine = replaceZhToJpKanji(line)
            # 目前是机翻，所以限制翻译后文本不得长于原始文本，
            # 实际上也不知道最多能多长，毕竟有那些意义不明的'分隔符'
            replacedLineBytes = replacedLine.encode("shiftjis")
            jpLineBytes = jpLine.encode("shiftjis")
            zhMinusJp = len(replacedLineBytes) - len(jpLineBytes)
            if zhMinusJp <= 0:
                # 如果长度不够，补足
                # zhMinusJp=0 不能放到else
                replacedLineBytes += b"\x00" * abs(zhMinusJp)
            else:
                replacedLineBytes = replacedLineBytes[:-zhMinusJp]
            # 回插消息块
            reJoinBytesList = jpMsg[jpMapKey][1]
            reJoinBytesList = [bytes(x) for x in reJoinBytesList]
            reJoinIndex = jpMsg[jpMapKey][2]
            reJoinBytesList.insert(reJoinIndex, replacedLineBytes)
            # flatten
            reJoinBytesList = [x for x in reJoinBytesList]
            reJoinBytes = b"".join(reJoinBytesList)
            msgBytesList.append(reJoinBytes)
            # 可以在这读下原文件头，检查reJoinBytes长度是不是msg block 大小
        msgBytes = b"".join(msgBytesList)
        # rebuild file
        fileBytes = bytes(headerBytesList) + msgBytes + bytes(endOfFileBytesList)
        with open(os.path.join(unpacedkWorkplace, ctdF), "wb") as file:
            file.write(fileBytes)


target = "tutorialtable.bin"
pathParts = [
    "init",
]
ftdTargets = [
    "tutorialConditions.ftd",
]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
unpacedkWorkplace = Path().joinpath(cacheRoot, *pathParts, target.replace(".", "_"))
cacheWorkplace = str(unpacedkWorkplace) + "_cache"
oriBinPath = Path().joinpath(oriCPKRoot, *pathParts, target)
cacheBinPath = Path().joinpath(cacheRoot, *pathParts, target)
rebuildBinPath = Path().joinpath(rebuildCPKRoot, *pathParts, target)

ftdJsonPath = Path().joinpath(codeWorkplace, "ftd.json")
ftdPartsJsonPath = Path().joinpath(codeWorkplace, "ftd-parts.json")


if __name__ == "__main__":
    # collectMsg()
    rebuildFtd()
