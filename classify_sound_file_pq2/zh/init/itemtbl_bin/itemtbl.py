# collect text manually

import sys, re, os

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import readBinFile, writeBinFile, dumpJson, loadJson
from zh_common import replaceZhToJpKanji

oriFilePath = (
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\itemtbl.bin"
)
workPlace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\itemtbl_bin"

# 以0x16(十进制22)字节为一块读取
BLOCK_SIZE = 0x16


def getTextAreaIndex(bBytes):
    textHeader = b"\x4E\x55\x4C\x4C"
    textStartOffset = list(re.finditer(textHeader, bBytes))[0].start()
    return textStartOffset


def collectText():
    rawBytes = readBinFile(oriFilePath)
    textBytes = rawBytes[getTextAreaIndex(rawBytes) :]
    byteIndex = 0
    msgs = []
    while byteIndex < len(textBytes):
        text = textBytes[byteIndex : byteIndex + BLOCK_SIZE]
        textEnder = list(re.finditer(b".\x00\x00", text))
        if len(textEnder) > 0:
            textEnd = textEnder[0].start()
            text = text[: textEnd + 1]
        else:
            raise Exception
        msgs.append(text.decode("shiftjis"))
        # print(text.decode("shiftjis"))
        byteIndex += BLOCK_SIZE

    # flatten map
    msgMap = {}
    for i in range(len(msgs)):
        msgMap["{}_{}".format("itemtbl.bin", i)] = msgs[i]

    dumpJson("itemtbl.json", msgMap)
    return msgMap


def rebuild():
    rebuildBinPath = r'F:\TMP\cpk_output_workplace\datacpk\init\itemtbl.bin'
    rawBytes = readBinFile(oriFilePath)
    frontPart = rawBytes[: getTextAreaIndex(rawBytes)]
    zhMap = loadJson("itemtbl-zh.json")
    msgBytes = b""
    for index in range(len(zhMap)):
        zhMsg = zhMap["{}_{}".format("itemtbl.bin", index)]
        zhMsgRp = replaceZhToJpKanji(zhMsg)
        zhMsgRpBytes = zhMsgRp.encode("shiftjis")
        diff = len(zhMsgRpBytes) - BLOCK_SIZE
        if diff > 0:
            zhMsgRpBytes = zhMsgRpBytes[:BLOCK_SIZE]
        else:
            zhMsgRpBytes += b"\x00" * abs(diff)
        msgBytes += zhMsgRpBytes
    fileBytes = frontPart + msgBytes
    writeBinFile(rebuildBinPath, fileBytes)


if __name__ == "__main__":
    os.chdir(workPlace)
    rebuild()
    print()
