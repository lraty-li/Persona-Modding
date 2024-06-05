import os, sys
from pathlib import Path
from enum import Enum

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import (
    writeBinFile,
    cacheRoot,
    oriCPKRoot,
    rebuildCPKRoot,
    readBinFile,
    dumpJson,
    fillToBytes,
    loadJson,
)
from zh_common import unpackBin, replaceZhToJpKanjiBytes
from arc_common import getArcFileNames, rebuildArcBytes
from tbl_common import reJoinMsgBytes


class DecodeStatus(Enum):
    Default = 0
    FirstByteZero = 1
    decodeOneByteFin = 2
    decodeOneByteNotPassNext = 3


offsets = {"1": {"start": 0x4B548A, "end": 0x4B7689}}


def splitBytesCodeBin(bBytes):
    status = DecodeStatus.Default
    inMsgLine = False  # status
    msgPiece = []
    otherBytesPiece = []
    index = 0
    rawBytesLength = len(bBytes)
    rawBytes = bBytes
    otherBytes = []
    msgs = []
    indexReadAdd = 2
    while 1:
        if index + 2 > rawBytesLength:
            break
        decodeTarget = rawBytes[index : index + indexReadAdd]
        try:
            char = decodeTarget.decode("shiftjis")
            if decodeTarget == b"\x0a" or decodeTarget[:1] == b"\x0a":
                # 换行符放入other byte
                status = DecodeStatus.decodeOneByteNotPassNext
                raise UnicodeDecodeError("shiftjis", bBytes, index, -1, "")
            if not inMsgLine:
                inMsgLine = True
                otherBytes.append(otherBytesPiece)
                otherBytesPiece = []
            msgPiece += char
            index += indexReadAdd
            if status == DecodeStatus.decodeOneByteFin:
                #  解码一字节成功，恢复每两位读取。避免错位
                indexReadAdd = 2
            continue
        except UnicodeDecodeError:
            if status == DecodeStatus.Default:
                # 尝试只解码1字节
                indexReadAdd = 1
                status = DecodeStatus.decodeOneByteFin
                continue

            if status == DecodeStatus.decodeOneByteFin:
                # 单字节解码失败了，下一字节也直接加入otherBytesPiece
                indexReadAdd = 2
                decodeTarget = rawBytes[index : index + indexReadAdd]

            if inMsgLine:
                inMsgLine = False
                msgs.append(msgPiece)
                msgPiece = []
            otherBytesPiece += decodeTarget
            index += indexReadAdd
            if status == DecodeStatus.decodeOneByteNotPassNext:
                indexReadAdd = 2
            status = DecodeStatus.Default
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


def collectMsg(num, rawBytes):

    start = offsets[str(num)]["start"]
    end = offsets[str(num)]["end"]
    rawBytes = readBinFile(oriBinPath)
    msgs = rawBytes[start:end]
    # 81 41 0A 82 6D 82 64, 在现有的splitBytes 0A 82 被合并读取导致打乱
    splitedMsg = splitBytesCodeBin(msgs)
    msgMap = {}
    msgMap[str(num)] = splitedMsg
    dumpJson(outputJsonPath, msgMap)
    # flatten
    flattenMsgMap = {}
    msgLines = splitedMsg[0]
    for index in range(len(msgLines)):
        flattenMsgMap["codeBin_{}_{}".format(num, index)] = msgLines[index]
    dumpJson(outputPartsJsonPath, flattenMsgMap)
    print()


def buildPatchBytes(num, zhMsgMap, rawData):

    start = offsets[str(num)]["start"]
    end = offsets[str(num)]["end"]
    jpMsgs = rawData[0]
    jpOtherBytes = rawData[1]
    zhMsgRps = []
    for index in range(len(zhMsgMap)):
        if("codeBin_{}_{}".format(num, index) == 'codeBin_1_246'):
            print()
        zhMsg = zhMsgMap["codeBin_{}_{}".format(num, index)]
        jpMsg = jpMsgs[index]
        #TODO 填充不能为 00 ，之前的缺失可能原因
        #TODO 81 40 显示为X，字库问题
        #TODO 居中，允许从两侧fill
        zhMsgRpBytes = replaceZhToJpKanjiBytes(zhMsg, len(jpMsg.encode("shiftjis")),filling=b'\x20')
        zhMsgRps.append(zhMsgRpBytes)
    joinedBytes = reJoinMsgBytes(zhMsgRps, jpOtherBytes)
    assert len(joinedBytes) == end - start
    return joinedBytes


def patchAll():
    target = 1
    zhMsgMap = loadJson(zhJsonPath)
    rawMsgMap = loadJson(outputJsonPath)

    joinedBytes = buildPatchBytes(target, zhMsgMap, rawMsgMap[str(target)])
    fileBytes = fillToBytes(offsets[str(target)]["start"], rawBytes[:], joinedBytes)
    outputPath = r'D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool\cci\cxi0\exefs\code.bin'
    # writeBinFile(Path().joinpath(codeWorkplace, "test.bin"), fileBytes)
    writeBinFile(outputPath, fileBytes)
    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool")
    os.system(r'.\3dstool.exe -cvtfz exefs cci\cxi0\exefs.bin --header cci\cxi0\exefs\exefsheader.bin --exefs-dir cci\cxi0\exefs')
    os.system(r'.\3dstool.exe -cvtf cxi cci\0.cxi --header cci\cxi0\ncchheader.bin --exh cci\cxi0\exh.bin --logo cci\cxi0\logo.bcma.lz --plain cci\cxi0\plain.bin --exefs cci\cxi0\exefs.bin --romfs cci\cxi0\romfs.bin --not-encrypt')


targetFile = "code.bin"
pathParts = [targetFile.replace(".", "_")]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
oriBinPath = Path().joinpath(cacheRoot, *pathParts, targetFile)
outputJsonPath = Path().joinpath(codeWorkplace, "msg.json")
outputPartsJsonPath = Path().joinpath(codeWorkplace, "msg-parts.json")
zhJsonPath = Path().joinpath(codeWorkplace, "msg-parts-zh.json")
rawBytes = readBinFile(oriBinPath)  # 文件很大，不重复读取

if __name__ == "__main__":
    # collectMsg(1)
    patchAll()
