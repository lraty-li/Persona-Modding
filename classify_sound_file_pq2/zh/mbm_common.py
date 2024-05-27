from pathlib import Path
import sys

HEX_F8_VALUE = b"\xf8"[0]
HEX_80_VALUE = b"\x80"[0]
HEX_7F_VALUE = b"\x7F"[0]
HEX_FF_VALUE = b"\xff"[0]


HEADER_SIZE = 0x20
MSG_COUNT_OFFSET = 0x10
MSG_INFO_SIZE = 0x10
MSG_NO_OFFSET = 0x0
MSG_SIZE_OFFSET = 0x4
MSG_OFFSET = 0x8
FILE_SIZE_OFFSET = 0xC

MBM_HEADER_TEMPLATE = "00 00 00 00 4D 53 47 32 00 00 01 00 84 03 00 00 1E 00 00 00 20 00 00 00 00 00 00 00 00 00 00 00"
MBM_MSG_INFO_TEMPLATE = "00 00 00 00 0E 00 00 00 00 02 00 00 00 00 00 00"

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import parseLine
from common import getReveBinValue


def isAscii(bByteInt):
    # 游戏原本的ASCII范围被用来表示某些图标，日文似乎全都是全角符号
    if bByteInt <= HEX_7F_VALUE:
        return True
    else:
        return False


def isSpecial(bByteInt):
    # if bByteInt == HEX_F8_VALUE or bByteInt == HEX_80_VALUE:  # b'\xf8' b'\x80'
    if bByteInt in [0xF8, 0x80, 0x87]:
        # unknow byte
        # f8 01,  f8 04, f8 00...
        # 80 01, 80 04
        # TODO 80 00 , 0A 00,  will be parsed as ascii
        return True
    else:
        return False


def printBytes(bBytes):
    for bByte in bBytes:
        print("{:02x}".format(bByte), end=" ")
    print("\n")


def readBinData(filePath):
    rawData = ""
    with open(filePath, "rb") as file:
        rawData = file.read()
    return rawData


def bypasDeooBytes(bBytes, startIndex, byteCount=1):
    msgLine = ""
    byteIndex = 0
    while byteIndex < byteCount:
        msgLine += "[{:02x} {:02x}]".format(
            bBytes[startIndex + byteIndex], bBytes[startIndex + byteIndex + 1]
        )
        byteIndex += 2
    return msgLine


def bytesShouldBypassed(secondByte):
    if secondByte in [0x01, 0x55, 0x06, 0x02, 0x44]:
        return 2
    elif secondByte in [0x11, 0x04, 0x42, 0x41, 0x15, 0x19]:
        return 4
    else:
        raise Exception("Unimplement")


def decodeMsgBytes(bBytes):
    msgLine = ""
    byteIndex = 0
    while byteIndex < len(bBytes):
        byte1 = bBytes[byteIndex]

        if isAscii(byte1):
            msgLine += bytes(byte1).decode("shiftjis")
            byteIndex += 1
            continue
        elif isSpecial(byte1):
            # TODO how too keep bypassed bytes
            # bypass next byte too # f8 01 should not bypass next
            byte2 = bBytes[byteIndex + 1]

            bpassCount = bytesShouldBypassed(byte2)
            msgLine += bypasDeooBytes(bBytes, byteIndex, bpassCount)
            byteIndex += bpassCount

        elif byte1 == HEX_FF_VALUE:
            # TODO how too keep bypassed bytes
            break
        else:
            byte1And2 = bBytes[byteIndex : byteIndex + 2]
            try:
                msgLine += byte1And2.decode("shiftjis")
                # TODO collect bytes
            except UnicodeDecodeError as e:
                print("WARN: fail to decode {}".format(byte1And2))
                raise Exception("fail to decode")
            byteIndex += 2
            continue

    return msgLine

def getMsgOfInfo(rawData, msgInfo):
    # msg size
    # ... 4 ...,...5...
    # low byte, hight byte

    msgSize = getReveBinValue(msgInfo[MSG_SIZE_OFFSET : MSG_SIZE_OFFSET + 4])

    # msg start offset
    # ... 8 ...,...9...
    # low byte, hight byte

    msgLineStartOffset = getReveBinValue(msgInfo[MSG_OFFSET : MSG_OFFSET + 4])
    msgBytes = rawData[msgLineStartOffset : msgLineStartOffset + msgSize]
    msg = decodeMsgBytes(msgBytes)
    parsedMsg = parseLine(msg, False)
    # rejoined = reJoinMsg(parsedMsg[1], parsedMsg[0])
    # rejoined == msg
    return parsedMsg


def decodeAllMbm(tTargets):
    msgMap = {}
    decodedMsg = {}
    for index in range(len(tTargets)):
        targ = tTargets[index]
        decodedMsg["{}".format(targ.name)] = []
        print("\n" + Path(targ).name)
        sum = 0
        rawData = readBinData(targ)
        if True:  # TODO format

            header = rawData[:HEADER_SIZE]
            msgCount = getReveBinValue(header[MSG_COUNT_OFFSET : MSG_COUNT_OFFSET + 4]) #BUG？ 2byte 
            fileSize = getReveBinValue(header[FILE_SIZE_OFFSET : FILE_SIZE_OFFSET + 4])
            # skyitemfoodeffect.mbm 的 file size 怎么不对的......
            firstMsgInfo = rawData[HEADER_SIZE : HEADER_SIZE + MSG_INFO_SIZE]
            msgAreaStartOffset = getReveBinValue(
                firstMsgInfo[MSG_OFFSET : MSG_OFFSET + 4]
            )
            # collect all msg nombering
            # msg info 编号不一定是连续的
            msgInfoArea = rawData[HEADER_SIZE:msgAreaStartOffset]
            # msgNombers = []
            # for index in range(int(len(msgInfoArea) / MSG_INFO_SIZE)):
            #     msgInfoStartOffset = index * MSG_INFO_SIZE
            #     nomb = getReveBinValue(
            #         msgInfoArea[msgInfoStartOffset : msgInfoStartOffset + 4]
            #     )
            #     if nomb > 0:
            #         msgNombers.append(nomb)

            firsetMsg = getMsgOfInfo(rawData, firstMsgInfo)
            decodedMsg["{}".format(targ.name)].append(firsetMsg)

            for index in range(int(len(msgInfoArea) / MSG_INFO_SIZE)):
                #  应该直接跳到对应的msginfo读取，而不是顺序读下去，是稀疏的
                # 把msg info 部分切出来，然后找编号部分非零的
                msgInfoOffset = HEADER_SIZE + (index * MSG_INFO_SIZE)
                msgInfo = rawData[msgInfoOffset : msgInfoOffset + MSG_INFO_SIZE]
                msgNomber = getReveBinValue(msgInfo[MSG_NO_OFFSET : MSG_NO_OFFSET + 4])
                if msgNomber == 0:
                    continue
                parsedMsg = firsetMsg = getMsgOfInfo(rawData, msgInfo)

                # { filename: [[ msg, ctlStrs],[msg,ctlStr]...],...}
                decodedMsg["{}".format(targ.name)].append(parsedMsg)

    return decodedMsg


def flattenTheMap(mMap):
    flattenMap = {}
    for fileName in mMap:
        msgClts = mMap[fileName]
        for msgIndex in range(len(msgClts)):
            oneMsgInfo = msgClts[msgIndex]
            oneMsgs = oneMsgInfo[0]
            for index in range(len(oneMsgs)):
                flattenMap["{}_{}_{}".format(fileName, msgIndex, index)] = oneMsgs[
                    index
                ]
    return flattenMap


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
