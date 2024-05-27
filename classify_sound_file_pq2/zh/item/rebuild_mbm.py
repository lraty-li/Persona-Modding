import sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from mbm_common import *
from common import loadJson, writeBinFile, valueToLittleBytes,fillToBytes
from zh_common import replaceZhToJpKanji
from msg_parser import parseLine, reJoinMsg


if __name__ == "__main__":
    rawJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\item\mbm.json"
    translatedJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\item\mbm-parts-zh.json"
    repackCpkRoot= r'F:\TMP\cpk_output_workplace\datacpk\Item'
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
            transedMsgLinesRp = []
            for line in transedMsgLines:
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
        #TODO file size
        # just dump to repack root
        outputPath = Path().joinpath(repackCpkRoot,targ)
        writeBinFile(str(outputPath), mbmFileBytes)

print()
