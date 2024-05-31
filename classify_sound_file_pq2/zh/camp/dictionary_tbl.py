import sys, os
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import (
    getMsgLines,
    parseMsgFile,
    rebuilAllMsg,
    rebuildFailBf,
    RecompileType,
)
from common import (
    dumpJson,
    atlusScriptCompiler,
    loadJson,
    writeBinFile,
    cacheRoot,
    rebuildCPKRoot,
    readBinFile,
    fillToBytes,
)

from zh_common import replaceZhToJpKanji, zhChar2JpKanji


def collectText():
    rawData = readBinFile(str(Path().joinpath(cacheWorkplaceRoot, target)))
    msgCount = int(len(rawData) / lineWidth)
    msgMap = {}
    for index in range(msgCount):
        msgBytes = rawData[
            index * lineWidth + msgOffset : index * lineWidth + msgOffsetEnd
        ]
        msgBytes = msgBytes.replace(b"\x00", b"")
        msg = msgBytes.decode("shiftjis")
        msgMap["{}_{}".format(target, index)] = msg
        print(msg)
    dumpJson(Path().joinpath(codeWorkplace, "dictionary_tbl.json"), msgMap)


def rebuildTbl():
    rawData = readBinFile(str(Path().joinpath(cacheWorkplaceRoot, target)))
    msgCount = int(len(rawData) / lineWidth)
    zhJsonPath = Path().joinpath(codeWorkplace, "dictionary_tbl-zh.json")
    transdMsg = loadJson(zhJsonPath)
    msgs = []
    newTblBytes = []
    for index in range(msgCount):
        zhMsg = transdMsg["{}_{}".format(target, index)]
        rawDataLine = rawData[index * lineWidth : (index * lineWidth) + lineWidth]
        oriJpBytes = rawDataLine[msgOffset:msgOffsetEnd].replace(b"\x00", b"")
        zhMsgRpBytes = replaceZhToJpKanji(zhMsg).encode("shiftjis")
        lengthDiff = len(oriJpBytes) - len(zhMsgRpBytes)
        if lengthDiff < 0:
            zhMsgRpBytes = zhMsgRpBytes[:lengthDiff]
        else:
            zhMsgRpBytes += b"\x00" * lengthDiff  # 不知道用00 填充会不会有问题
        newTblBytes += fillToBytes(msgOffset, list(rawDataLine), zhMsgRpBytes)
    writeBinFile(Path().joinpath(rebuildCPKRoot, "camp", target), bytes(newTblBytes))


target = "dictionary.tbl"
cacheWorkplaceRoot = Path().joinpath(cacheRoot, "camp")
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
lineWidth = 0x3C
msgOffset = 0x08
msgOffsetEnd = 0x1B + 1

if __name__ == "__main__":
    # collectText()
    rebuildTbl()
