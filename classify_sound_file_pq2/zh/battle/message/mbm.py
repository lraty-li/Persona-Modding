from pathlib import Path
import sys

from mbm_common import *

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import dumpJson
from msg_parser import parseLine, reJoinMsg




def isAscii(bByteInt):
    # 游戏原本的ASCII范围被用来表示某些图标，日文似乎全都是全角符号
    if bByteInt <= HEX_7F_VALUE:
        return True
    else:
        return False


def isSpecial(bByteInt):
    if bByteInt == HEX_F8_VALUE:  # b'\xf8'
        # unknow byte
        # f8 01,  f8 04, f8 00...
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
            if byte2 == 0x01:
                byteIndex += 2  # bypass itself
                msgLine += "[f8 01]"
                continue
            if byte2 == 0x11:
                msgLine += "[f8 11]"
                nextTwoByte = bBytes[byteIndex + 2 : byteIndex + 4]
                msgLine += "[{:02x} {:02x}]".format(
                    bBytes[byteIndex + 2], bBytes[byteIndex + 3]
                )
                byteIndex += 4  # bypass itself and next one byte
                continue
            else:
                print("Unimplement")
                raise Exception

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
            byteIndex += 2
            continue

    return msgLine


def getReveBinValue(bBytes):
    # bBytes = list(reversed(bBytes))
    sum = 0
    for bByteIndex in range(len(bBytes)):
        sum += bBytes[bByteIndex] << (8 * bByteIndex)
    return sum


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
            msgCount = getReveBinValue(header[MSG_COUNT_OFFSET : MSG_COUNT_OFFSET + 4])
            fileSize = getReveBinValue(header[FILE_SIZE_OFFSET : FILE_SIZE_OFFSET + 4])
            for index in range(msgCount):
                msgInfo = rawData[ 
                    HEADER_SIZE + index * MSG_INFO_SIZE 
                    : HEADER_SIZE + (index + 1) * MSG_INFO_SIZE
                ]  # fmt: skip
                # msg size
                # ... 4 ...,...5...
                # low byte, hight byte

                msgSize = getReveBinValue(
                    msgInfo[MSG_SIZE_OFFSET : MSG_SIZE_OFFSET + 4]
                )

                # msg start offset
                # ... 8 ...,...9...
                # low byte, hight byte
                
                msgLineStartOffset = getReveBinValue(
                    msgInfo[MSG_OFFSET : MSG_OFFSET + 4]
                )
                msgBytes = rawData[msgLineStartOffset : msgLineStartOffset + msgSize]
                msg = decodeMsgBytes(msgBytes)
                parsedMsg = parseLine(msg, False)
                # rejoined = reJoinMsg(parsedMsg[1], parsedMsg[0])
                # rejoined == msg
                
                msgNomber = getReveBinValue(msgInfo[MSG_NO_OFFSET : MSG_NO_OFFSET + 4])
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
                flattenMap["{}_{}_{}".format(fileName, msgIndex, index)] = oneMsgs[index]
    return flattenMap


if __name__ == "__main__":
    # skillexpbattle_player.mbm ? TODO 稀疏文件，很多msgInfo是空的
    # >>> [i for i in os.listdir('.') if i.endswith('.mbm')]
    targets = [
        "battlemessage.mbm",
        "skillburstexp.mbm",
        "skillcustom.mbm",
        "skillexpbattle.mbm",
        "skillexpbattle_enemy.mbm",
        "skillexpbattle_player.mbm",
    ]
    cacheRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\message"
    )

    targets = [Path().joinpath(cacheRoot, i) for i in targets]
    msgMap = decodeAllMbm(targets)
    flattenMsgMap = flattenTheMap(msgMap)
    outputJpJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\mbm.json"
    dumpJson(outputJpJson, msgMap)
    outputJpJsonP = Path(outputJpJson)
    dumpJson(Path().joinpath(outputJpJsonP.parent, outputJpJsonP.stem + '-parts.json'), flattenMsgMap)
    print()
