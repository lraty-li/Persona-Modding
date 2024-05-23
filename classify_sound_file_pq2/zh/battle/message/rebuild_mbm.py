import sys
from pathlib import Path
from mbm_common import *

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import loadJson
from zh_common import replaceZhToJpKanji
from msg_parser import parseLine, reJoinMsg


def ctlStrsToBytes(text):
    bBytes = []
    if len(text) == 0:
        return []
    else:
        hexStrs = text[1:-1].replace("][", " ")
        hexStrs = hexStrs.split(" ")
        bBytes = bytes.fromhex("".join(hexStrs))
        return bBytes


def reJoinToBytes(ctlStrs, msg):
    # 尝试缝合：
    reJoin = []
    msgLength = len(msg)
    msgCtlStrsLength = len(ctlStrs)
    if msgCtlStrsLength > msgLength:
        for i in range(msgCtlStrsLength):
            ctlBytes = ctlStrsToBytes(ctlStrs[i])
            reJoin += ctlBytes
            if i < msgLength:
                # BUG 修复字符集，hall to full width 有很多非shiftjis部分
                reJoin += msg[i].encode("shiftjis")
    else:
        raise Exception("control string more than msg?")
    return reJoin


def valueToLittleBytes(value):
    # reverd
    # input : 19,088,743
    # output 67 45 23 01
    return value.to_bytes(4, "little")


def fillToBytes(start, container, bBytes):
    if len(bBytes) > len(container):
        raise
    else:
        for bbyte in bBytes:
            container[start] = bbyte
            start += 1
    return container


def writeMbmFile(filepaht, data):
    with open(filepaht, "wb") as file:
        file.write(bytes(data))


if __name__ == "__main__":
    rawJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\mbm.json"
    translatedJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\mbm-parts-zh.json"
    repackCpkRoot= r'F:\TMP\cpk_output_workplace\datacpk\battle\message'
    # DEBUG
    # translatedJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\mbm-parts.json"
    # DEBUG END

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
            # TODO 某些翻译失败的文本简单过滤，但是应该放到translate.py
            # TODO replace with charset
            transedMsgLinesRp = []
            for line in transedMsgLines:
                if "'" in line:
                    print()
                replacedLine = replaceZhToJpKanji(line)
                # DEBUG
                transedMsgLinesRp.append(replacedLine)
                # transedMsgLinesRp.append(line)
                # DEBUG END
            msgBytes = reJoinToBytes(ctlStrs, transedMsgLinesRp)
            msgMap[file].append(msgBytes)
    # DEBUG
    # targets = ["skillburstexp.mbm"]
    # DEBUG END

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
        # just dump to repack root
        outputPath = Path().joinpath(repackCpkRoot,targ)
        writeMbmFile(str(outputPath), mbmFileBytes)

print()
