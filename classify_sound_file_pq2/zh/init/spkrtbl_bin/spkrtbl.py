import os, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import (
    cacheRoot,
    rebuildCPKRoot,
    loadJson,
    readBinFile,
    dumpJson,
    fillToBytes,
    writeBinFile,
    oriCPKRoot,
)
from zh_common import replaceZhToJpKanji


def collectMsg():
    rawBytes = readBinFile(str(oriBinFile))
    byteIndex = 0
    msgIndex = 0
    rawBytesLen = len(rawBytes)
    msgMap = {}
    while byteIndex + lineWidth < rawBytesLen:
        msg = rawBytes[byteIndex + speakerStartOffset : byteIndex + lineWidth]
        msg = msg.replace(b"\x00", b"")
        msg = msg.decode("shiftjis")
        msgMap["{}_{}".format(targetFile, msgIndex)] = msg
        msgIndex += 1
        byteIndex += lineWidth
        print(msg)
    dumpJson(Path().joinpath(codeWorkplace, "spkrtbl-parts.json"), msgMap)


def rebuilBin():
    rawBytes = readBinFile(str(oriBinFile))
    byteIndex = 0
    msgIndex = 0
    rawBytesLen = len(rawBytes)
    msgMap = {}
    zhMsgs = loadJson(Path().joinpath(codeWorkplace, "spkrtbl-parts-zh.json"))
    rebuildBytes = b""
    while byteIndex + lineWidth < rawBytesLen:
        msgLineBytes = rawBytes[byteIndex : byteIndex + lineWidth]
        rawMsgBytes = msgLineBytes[speakerStartOffset:].replace(b"\x00", b"")

        zhMsg = zhMsgs["{}_{}".format(targetFile, msgIndex)]
        msgRp = replaceZhToJpKanji(zhMsg)
        msgBytes = msgRp.encode("shiftjis")
        lengthDiff = len(msgBytes) - len(rawMsgBytes)
        if lengthDiff <= 0:
            msgBytes += b"\x00" * -lengthDiff
        else:
            msgBytes = msgBytes[: len(rawMsgBytes)]
        if msgIndex == 5:
            print()

        rebuildBytes += msgLineBytes[:speakerStartOffset]
        rebuildBytes += msgBytes
        rebuildBytes += b"\x00" * (lineWidth - speakerStartOffset - len(msgBytes))
        msgIndex += 1
        byteIndex += lineWidth
    rebuildBytes += rawBytes[byteIndex:]
    writeBinFile(rebuildCpkTarget, rebuildBytes)
    pass


lineWidth = 40
speakerStartOffset = 16
# 0x08 是speaker id?

targetFile = "spkrtbl.bin"
pathParts = [
    "init",
]
workplace = Path().joinpath(cacheRoot, *pathParts)
cacheBinFile = Path().joinpath(workplace, targetFile)
rebuildCpkFolder = Path().joinpath(rebuildCPKRoot, *pathParts)
rebuildCpkTarget = Path().joinpath(rebuildCpkFolder, targetFile)
oriBinFile = Path().joinpath(oriCPKRoot, *pathParts, targetFile)
# move to _cache, avoiding any side effect to repack
codeWorkplace = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # collectMsg()
    rebuilBin()
