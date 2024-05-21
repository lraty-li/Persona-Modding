from pathlib import Path

HEX_F8_VALUE = b"\xf8"[0]
HEX_7F_VALUE = b"\x7F"[0]
HEX_FF_VALUE = b"\xff"[0]


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
            # bypass next byte too
            byteIndex += 2
            continue
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


def decodeAllMbm(tTargets):
    for index in range(len(targets)):
        targ = targets[index]
        print("\n"+Path(targ).name)
        sum = 0
        with open(targ, "rb") as file:
            rawData = file.read()
            HEADER_SIZE = 0x20
            MSG_COUNT_OFFSET = 0x10
            MSG_INFO_SIZE = 0x10
            header = rawData[:HEADER_SIZE]
            msgCount = header[MSG_COUNT_OFFSET]
            msgAreaOffset = HEADER_SIZE + msgCount * MSG_INFO_SIZE
            for index in range(msgCount):
                msgInfo = rawData[
                    HEADER_SIZE
                    + index * MSG_INFO_SIZE : HEADER_SIZE
                    + (index + 1) * MSG_INFO_SIZE
                ]
                # msg size
                # ... 4 ...,...5...
                # low byte, hight byte
                msgSize = (msgInfo[5] << 8) + msgInfo[4]
                # msg start offset
                # ... 8 ...,...9...
                # low byte, hight byte
                msgLineStartOffset = (msgInfo[9] << 8) + msgInfo[8]
                msgBytes = rawData[msgLineStartOffset : msgLineStartOffset + msgSize]
                # unkown = msgInfo[9]
                # if unkown == 3:
                #     print()
                msg = decodeMsgBytes(msgBytes)
                print("{} {}".format(msgInfo[0], msg))
                # print("{} {}".format(hex(msgInfo[0]), msg))
                # printBytes(msgBytes)

        # print("sum {}".format(hex(sum)))


if __name__ == "__main__":
    targets = [
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\message\skillburstexp.mbm",
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\item\skyitemequipexplain.mbm",
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\message\skillcustom.mbm",
    ]
    decodeAllMbm(targets)
