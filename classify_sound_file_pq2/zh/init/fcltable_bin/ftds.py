import os, shutil, re

import sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import dumpJson, getReveBinValue
from zh_common import unpackBin


workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin"

# [i for i in os.listdir('.') if i.endswith('ctd')]


os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin")

HEADER_SIZE = 16


def bytesListToIntList(bytesList):
    if type(bytesList) == bytes:
        bytesList = [bytesList]
    return [[byte for byte in bBytes] for bBytes in bytesList]


def parseFtd(filePath):
    rawBytes = []
    allByteSplited = []
    msgs = []
    with open(filePath, "rb") as file:
        rawBytes = file.read()
    rawBytesLength = len(rawBytes)
    fileHeader = rawBytes[:HEADER_SIZE]
    endOfFile = []
    index = HEADER_SIZE

    blockSize = int(getReveBinValue(fileHeader[:4]) / getReveBinValue(fileHeader[4:8]))
    # 根据 '行宽' 把文件分块
    while index < rawBytesLength:
        remainByteCount = rawBytesLength - index
        if remainByteCount < blockSize:
            if remainByteCount != HEADER_SIZE:
                # raise Exception("Not header and implement")
                pass
            endOfFile = rawBytes[index:]
            break
        msgBytes = rawBytes[index : index + blockSize]
        allByteSplited.append(msgBytes)
        index += blockSize
    # header + allByteSplited + ender 应该与原文件一致
    # 把message 部分处理，按 00 切断
    for splitedBytes in allByteSplited:
        partStartIndex = 0
        msgParts = []
        reFindIter = re.finditer(b"\x00+", splitedBytes)
        for matchedIndex in reFindIter:
            start = matchedIndex.start(0)
            msgParts.append(splitedBytes[partStartIndex:start])
            end = matchedIndex.end(0)
            msgParts.append(splitedBytes[start:end])
            partStartIndex = end
        # 选去掉 \x 00 后的最长的作为 'message' ？
        noZeroMsgParts = [i.replace(b"\x00", b"") for i in msgParts]
        partLengths = [len(i) for i in noZeroMsgParts]
        longestIndex = partLengths.index(max(partLengths))
        # 直接 decode 应该没问题吧
        msgBytes = msgParts[longestIndex]
        msg = msgBytes.decode("shiftjis")
        noMsgBytes = (
            msgParts[:longestIndex] + msgParts[longestIndex + 1 :]
        )  # BUG? longestIndex + 1 越界？
        noMsgIntList = bytesListToIntList(noMsgBytes)
        msgs.append([msg, noMsgIntList, longestIndex])  # longestIndex 用于rejoin,
    msgs.insert(0, ["", bytesListToIntList(fileHeader), 0])
    msgs.append(["", bytesListToIntList(endOfFile), 0])
    return msgs
    # TODO rejoin check

    # 起码目前来看是2 bytes 对齐的
    # inMsgLine = False  # status
    # msgPiece = []
    # otherBytesPiece = []
    # while index < rawBytesLength:
    #     twoBytes = rawBytes[index : index + 2]
    #     if inMsgLine:
    #         try:
    #             if twoBytes == b"\x00\x00":
    #                 raise UnicodeDecodeError
    #             char = twoBytes.decode("shiftjis")
    #             msgPiece += char
    #             index += 2
    #             continue
    #         except UnicodeDecodeError:
    #             inMsgLine = False
    #             msgs.append(msgPiece)
    #             msgPiece = []
    #             otherBytesPiece += twoBytes
    #             index += 2
    #             continue
    #     else:
    #         try:
    #             if twoBytes == b"\x00\x00":
    #                 raise UnicodeDecodeError
    #             char = twoBytes.decode("shiftjis")
    #             inMsgLine = True
    #             otherBytes.append(otherBytesPiece)
    #             otherBytesPiece = []
    #             msgPiece += char
    #             index += 2
    #             continue
    #         except UnicodeDecodeError:
    #             otherBytesPiece += twoBytes
    #             index += 2
    #             continue


if __name__ == "__main__":
    msgMap = {}
    targets = [
        "fclSimpleHelp.ftd",
        "fclBPItemName.ftd",  # BLOCK SIZE?
        "fclHelpTable_NOFFICE.ftd",
        "fclNetWorkStr.ftd",
        "fclFesRootHelp.ftd",
        "fclFesRootHelpCosplay.ftd",
        "fclFesRootHelpEx.ftd",
        "fclFesDgDeteailHelp.ftd",
        "fclFesDgTopHelp.ftd",
        "fclHelpTable_COMBINE.ftd",
        "fclHelpTable_COMBINE_ROOT.ftd",
        "fclHelpTable_NETWORK_ROOT.ftd",
        "fclHelpTable_SHOP.ftd",
        "fclSpreadText.ftd",
        "fclSuggestTypeName.ftd",
        "fclHelpTable_LIVER.ftd",
        "fclFesPartyDeteailHelp.ftd",
        "fclFesTopMenu.ftd",
        "fclHelpTable_ELVGIRL_ROOT.ftd",
        "fclHelpTable_NETWORK.ftd",
        "fclHelpTable_NETWORK_E.ftd",
        "fclWeaponTypeName.ftd",
        "fclNetWorkEditMenu.ftd",
        "fclWeaponHelp.ftd",
        "fclWeaponTopMenu.ftd",
        "fclCombineTopMenuText.ftd",
        "fclFesDgMenu.ftd",
        "fclFesDgTopMenu.ftd",
        "fclNofficeTopMenu.ftd",
        "fclFesPartyMenu.ftd",
        "fclNofficeCommandHelp.ftd",
        "fclCombineRootText.ftd",
        "fclFesEvtMenu.ftd",
        "fclHelpTable_ELVGIRL.ftd",
        "fclHelpTable_ELVGIRL_E.ftd",
        "fclHelpTable_SHOP_M.ftd",
        "fclItemTopMenu.ftd",
        "fclNetWorkQRCodeMenu.ftd",
        "fclNofficeCancelConfMenu.ftd",
        "fclNofficeQuestTopMenu.ftd",
        "fclSearchText.ftd",
        "fclWeaponCategoryName.ftd",
        "fclElvGirlText.ftd",
        "fclFesEvtDeteailHelp.ftd",
        "fclHelpTable_NOFFICE_E_BLUE.ftd",
        "fclHelpTable_NOFFICE_M.ftd",
        "fclItemHelp.ftd",
        "fclViewTypeText.ftd",
        "fclWeaponSellList.ftd",
        "fclMatelialInfo.ftd",
    ]
    # 复制原版的.bin文件到cache，免得读取到已经替换文字后的文件
    # originalBin = r"f:\TMP\cpk_output_workplace\datacpk\init\fcltable.bin"
    cacheBin = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\fcltable.bin"
    )
    # shutil.copy(originalBin, cacheBin)
    # unpackBin(cacheBin)
    for target in targets:
        # if target == "cmpDifficultItem.ctd":
        #     print()
        msgs = []
        ctdLines = parseFtd(os.path.join(cacheBin.replace(".", "_"), target))
        for lineIndex in range(len(ctdLines)):
            msgMap["{}_{}".format(target, lineIndex)] = ctdLines[lineIndex]

    dumpJson("ftd.json", msgMap)
    print("DONE")
