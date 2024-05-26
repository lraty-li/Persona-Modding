import sys, os

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import replaceZhToJpKanji
from common import loadJson, valueToLittleBytes, valueToLittleBytes, getReveBinValue


def reJoinMsgBytes(msgs, otherBytes):
    reJoin = []
    otherBytesLength = len(otherBytes)
    msgsLength = len(msgs)
    if otherBytesLength < msgsLength:
        raise Exception("msgs more than otherBytes")
    for index in range(otherBytesLength):
        reJoin += otherBytes[index]
        if index < msgsLength:
            msgBytes = msgs[index].encode("shiftjis")
            reJoin += msgBytes
    return reJoin


def splitBytes(bBytes):
    inMsgLine = False  # status
    msgPiece = []
    otherBytesPiece = []
    index = 0
    rawBytesLength = len(bBytes)
    rawBytes = bBytes
    otherBytes = []
    msgs = []
    while index < rawBytesLength:
        twoBytes = rawBytes[index : index + 2]

        if inMsgLine:
            try:
                if twoBytes == b"\x00":
                    raise UnicodeDecodeError("shiftjis", bBytes, index, -1, "")
                char = twoBytes.decode("shiftjis")
                msgPiece += char
                index += 2
                continue
            except UnicodeDecodeError:
                inMsgLine = False
                msgs.append(msgPiece)
                msgPiece = []
                otherBytesPiece += twoBytes
                index += 2
                continue
        else:
            try:
                if twoBytes == b"\x00":
                    raise UnicodeDecodeError("shiftjis", bBytes, index, -1, "")
                char = twoBytes.decode("shiftjis")
                inMsgLine = True
                otherBytes.append(otherBytesPiece)
                otherBytesPiece = []
                msgPiece += char
                index += 2
                continue
            except UnicodeDecodeError:
                otherBytesPiece += twoBytes
                index += 2
                continue
    if len(msgPiece) > 0:
        msgs.append(msgPiece)
    if len(otherBytesPiece) > 0:
        otherBytes.append(otherBytesPiece)
    msgs = ["".join(i) for i in msgs]
    # 合并方式：
    # 从otherBytes 开始，互相拉链式缝合回去
    # rejoin check
    rejoined = reJoinMsgBytes(msgs, otherBytes)
    if bytes(rejoined) != bBytes:
        raise Exception("rejoin fail")
    return msgs, otherBytes


def parseTblMsg(filePath):
    rawBytes = []
    with open(filePath, "rb") as file:
        rawBytes = file.read()
    byteIndex = 0
    # 文件开头的两字节的值乘2的结果，表示接下来用于表示长度信息的字节数
    # 以 skyitemequipeffect 为例
    # 开头两字节 12 00， 值为 18，接下来的18*2 个字节是长度信息
    # 这个长度信息的字节数（除以2）比实际上的文本段数多1，因为那些字节通过往前相减能够得到文本的长度 / 自身加上对应文本长度得到下一两个字节
    # 同时也可以 2+18*2 , 得到文本的开始地址
    HEADER_BYTE_SIZE = 2
    msgInfoBytesCount = getReveBinValue(rawBytes[:HEADER_BYTE_SIZE]) * 2

    msgAreaStart = msgInfoBytesCount + HEADER_BYTE_SIZE
    msgInfoBytes = rawBytes[HEADER_BYTE_SIZE:msgAreaStart]
    msgBytes = rawBytes[msgAreaStart:]
    # 还是按规则读取
    msgLengthOffset = 0
    byteIndex = 0
    msgMap = []
    msgCounter = 0
    while byteIndex < msgInfoBytesCount:
        msgLength = (
            getReveBinValue(msgInfoBytes[byteIndex : byteIndex + 2]) - msgLengthOffset
        )
        msg = msgBytes[msgLengthOffset : msgLengthOffset + msgLength]
        msgsOfLine, otherBytes = splitBytes(msg)
        if len(msgsOfLine) > 1:
            # 一行文本被未知字符切断了
            raise Exception("implement")
        msgMap.append([msgsOfLine, otherBytes])
        msgLengthOffset += msgLength
        byteIndex += 2
    return msgMap


def rebuildTblBytes(rawJsonPath, translatedJsonPath):
    # DEBUG
    # translatedJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\mbm-parts.json"
    # DEBUG END
    allFileBytes = {}
    rawData = loadJson(rawJsonPath)
    translatedMsg = loadJson(translatedJsonPath)
    msgMap = {}
    targets = []
    for file in rawData:
        msgMap[file] = []
        targets.append(file)
        msgInfos = rawData[file]
        for msgInfoIndex in range(len(msgInfos)):
            msgInfo = msgInfos[msgInfoIndex]
            msgs = msgInfo[0]
            ctlStrs = msgInfo[1]
            transedMsgLinesRp = []
            for index in range(len(msgs)):
                # 虽然兼容单行文本被切断的状态，但还是先不用了
                # transMsg = translatedMsg["{}_{}_{}".format(file, msgInfoIndex, index)]
                transMsg = translatedMsg["{}_{}".format(file, msgInfoIndex)]
                replacedLine = replaceZhToJpKanji(transMsg)
                # 限制翻译后文本不得超过原长度
                # TODO 但既然能处理好偏移，理论上可以比原本的长
                jpMsg = msgs[index]
                zhMinusJp = len(replacedLine) - len(jpMsg)
                if zhMinusJp <= 0:
                    # 如果长度不够，用全角空格补足
                    # BUG replaceZhToJpKanji 会把全角空格换回半角空格...，所以先替换算了
                    # zhMinusJp=0 不能放到else
                    replacedLine += "　" * abs(zhMinusJp)
                else:
                    replacedLine = replacedLine[:-zhMinusJp]

                transedMsgLinesRp.append(replacedLine)

            msgBytes = reJoinMsgBytes(transedMsgLinesRp, ctlStrs)
            msgMap[file].append(msgBytes)

    # DEBUG
    # targets = ["skillburstexp.mbm"]
    # DEBUG END

    # rebuild tbl files
    for targ in targets:
        msgSizeOffset = 0
        msgLines = msgMap[targ]
        msgCount = len(msgLines)
        # build header
        fileHeader = valueToLittleBytes(msgCount, 2)  # 文件开头的两字节
        msgInfo = []
        msgArea = []
        for index in range(msgCount):
            # build msg info area
            msgBytes = msgMap[targ][index]
            # # 未知字符已经 reJoinMsgBytes 了
            # # otherBytes = rawData[targ][index][1]
            # # msgBytes += [bByte for _ in otherBytes for bByte in _]
            # 不额外加b\x00 ，otherBytes保留了
            # 并且有偏移，
            msgSizeOffset += len(msgBytes)
            msgSizeBytes = valueToLittleBytes(msgSizeOffset, 2)
            msgInfo += msgSizeBytes
            # build msg area
            msgArea += msgBytes
        # join all area
        tblFileBytes = fileHeader + bytes(msgInfo) + bytes(msgArea)
        allFileBytes[targ] = tblFileBytes
    return allFileBytes
