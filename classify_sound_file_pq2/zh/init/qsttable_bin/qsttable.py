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
from zh_common import replaceZhToJpKanjiBytes


def collectMsg():
    rawBytes = readBinFile(str(oriBinFile))
    byteIndex = 0
    msgIndex = 0
    # remove header, end of file

    rawBytes = rawBytes[HEAER_SIZE:-EOF_SIZE]
    rawBytesLen = len(rawBytes)
    msgMap = {}

    while byteIndex + lineWidth <= rawBytesLen:
        msg = rawBytes[byteIndex + speakerStartOffset : byteIndex + lineWidth]
        msg = msg.replace(b"\x00", b"")
        msg = msg.decode("shiftjis")
        msgMap["{}_{}".format(targetFile, msgIndex)] = msg
        msgIndex += 1
        byteIndex += lineWidth
        print(msg)
    dumpJson(
        Path().joinpath(
            codeWorkplace, "{}-parts.json".format(targetFile.replace(".", "_"))
        ),
        msgMap,
    )


def rebuilBin():
    rawBytes = readBinFile(str(oriBinFile))
    byteIndex = 0
    rawBytesLen = len(rawBytes)
    msgMap = {}
    zhMsgs = loadJson(
        Path().joinpath(
            codeWorkplace, "{}-parts-zh.json".format(targetFile.replace(".", "_"))
        )
    )
    rebuildBytes = b""
    for msgIndex in range(len(zhMsgs)):

        zhMsg = zhMsgs["{}_{}".format(targetFile, msgIndex)]
        msgRpBytes = replaceZhToJpKanjiBytes(zhMsg, lineWidth, filling=b"\x00",center=False)

        rebuildBytes += msgRpBytes
        msgIndex += 1
        byteIndex += lineWidth
    # add header
    rebuildBytes = rawBytes[:HEAER_SIZE] + rebuildBytes
    # add eof
    rebuildBytes += rawBytes[-EOF_SIZE:]
    writeBinFile(rebuildCpkTarget, rebuildBytes)
    pass


HEAER_SIZE = 56
EOF_SIZE = 16
lineWidth = 0x40
speakerStartOffset = 0
# 0x08 是speaker id?

targetFile = "qsttable.bin"
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
