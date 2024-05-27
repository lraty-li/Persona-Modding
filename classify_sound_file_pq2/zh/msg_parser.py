import os
import regex as re
from enum import Enum

from zh_common import (
    atlusScriptCompiler,
    replaceZhToJpKanji,
    joinNewLineCtlStr,
)

from common import loadJson, dumpJson
from common import fillToBytes, valueToLittleBytes, readBinFile

def splitIntoBlocks(text):
    blocks = []
    start = 0
    reFindIter = re.finditer("\n\n", text, flags=0)
    for matchedIndex in reFindIter:
        blocks.append(text[start : matchedIndex.start(0)])
        start = matchedIndex.end(0)
    return blocks


def parseSpeaker(text):
    speaker = re.findall(r"(?<=\[msg .* \[).*(?=\]\])", text)
    if len(speaker) >= 1:
        return speaker[0]
    else:
        return ""


def reJoinMsg(ctlStrs, msg):
    # 尝试缝合：
    reJoin = ""
    msgLength = len(msg)
    msgCtlStrsLength = len(ctlStrs)
    if msgCtlStrsLength > msgLength:
        for i in range(msgCtlStrsLength):
            reJoin += ctlStrs[i]
            if i < msgLength:
                reJoin += msg[i]
    else:
        raise Exception("control string more  than msg?")
    return reJoin


def textPreProgress(text):
    # DEBUG
    # text = "　"
    # DEBUG END
    text = text.replace("\u3000", "  ")
    # text = text.replace("…", "..")
    # matchEllipsis = re.findall(r"…+。", text)
    # if len(matchEllipsis) > 0:
    #     text = text.replace("…", "...")
    return text


def reJoinJustMsg(ctlStrs, msg):
    oriCtlStrs = list(ctlStrs)
    reJoin = ""
    msgLength = len(msg)
    msgCtlStrsLength = len(ctlStrs)
    ctlStrNeedRemove = []
    if msgCtlStrsLength > msgLength:
        for i in range(msgCtlStrsLength):
            if ctlStrs[i] == "[n]":
                removeIndex = i
                ctlStrNeedRemove.append(removeIndex)
                reJoin += ","
            if i < msgLength:
                reJoin += msg[i]
    else:
        raise Exception("control string more  than msg?")
    ctlStrNeedRemove.reverse()
    for index in ctlStrNeedRemove:
        ctlStrs.pop(index)
    return reJoin, ctlStrs


# 要记录原本控制字符得信息，回填。总之能拼出来跟结构一模一样的文本
# [n] 临时替换为句号?
def parseLine(text, postProgress=True):
    reFindIter = re.finditer(r"\[.*?\]", text, flags=0)
    data = []
    msg = []
    preCtlStrStart = 0
    preCtlStrEnd = 0
    ctlStrs = []
    LastCtlStr = ""
    for matchedIndex in reFindIter:
        start = matchedIndex.start(0)
        end = matchedIndex.end(0)
        if preCtlStrEnd == start:
            # 合并控制字符
            LastCtlStr = text[preCtlStrStart:end]
            preCtlStrEnd = end
        else:
            # 遇到（跳过）了msg
            msg.append(text[preCtlStrEnd:start])
            ctlStrs.append(text[preCtlStrStart:preCtlStrEnd])
            preCtlStrStart = start
            preCtlStrEnd = end
            LastCtlStr = text[start:end]
            # 如果剩下的都是控制字符，无法再进入这个流程，就LastCtlStr吧
    ctlStrs.append(LastCtlStr)
    reJoin = reJoinMsg(ctlStrs, msg)
    if text != reJoin:
        print(text)
        print(reJoin)
        raise Exception("rejoin mismatch!")
    # 把[n] 合并掉，
    # TODO 之后拼回来的时候再手动添加
    if postProgress:
        joinedMsg, ctlStrsNoNewLine = reJoinJustMsg(ctlStrs, msg)

        msgNoU3000 = textPreProgress(joinedMsg)
        return [msgNoU3000, ctlStrsNoNewLine]  # use list for json
    else:
        return [msg, ctlStrs]  # use list for json


def progressBlock(block):
    lines = iter(block.split("\n"))
    header = next(lines)
    speaker = parseSpeaker(header)
    headerParts = []
    if len(speaker) == 0:
        # [msg ...]
        headerParts = [header[:-1], header[-1:]]
    else:
        # [msg ... [speaker]]
        rIndexL = header.rfind("[")
        rIndexR = header.rfind("]")  # -2
        headerParts = [header[: rIndexL + 1], header[rIndexR - 1 :]]

    data = []
    for line in lines:
        lineInfo = parseLine(line)
        data.append(lineInfo)

    return {"header": headerParts, "speaker": speaker, "linesInfo": data}


def parseMsgFile(filePath):
    blocksData = []
    with open(filePath, "r") as msgFile:
        msgRaw = msgFile.read()
        msgBlocks = splitIntoBlocks(msgRaw)
        for block in msgBlocks:
            data = progressBlock(block)
            blocksData.append(data)
    return blocksData


def getMsgLines(msgMapPath, outptJson=True):
    msgPartsMap = {}
    msgMap = loadJson(msgMapPath)
    spliter = "|"
    msgBatchedMap = {}
    for event in msgMap.keys():
        blocks = msgMap[event]
        msgs = []
        for blockIndex in range(len(blocks)):
            block = blocks[blockIndex]
            for lineInfoIndex in range(len(block["linesInfo"])):
                lineInfo = block["linesInfo"][lineInfoIndex]
                if type(lineInfo[0]) == str:
                    msgPartsMap[
                        "{}_{}_{}_{}".format(event, blockIndex, lineInfoIndex, 0)
                    ] = lineInfo[0]
                    continue
                for msgInnerLineIndex in range(len(lineInfo[0])):
                    # if(spliter in msg):
                    #     raise Exception("{} is in msg".format(spliter))
                    msgPartsMap[
                        "{}_{}_{}_{}".format(
                            event, blockIndex, lineInfoIndex, msgInnerLineIndex
                        )
                    ] = lineInfo[0][msgInnerLineIndex]

    # G, 翻译会去掉分隔符，不如直接来吧
    if outptJson:
        dumpJson(msgMapPath.replace(".json", "-parts.json"), msgPartsMap)
    return msgPartsMap


class RecompileType(Enum):
    BMD = 1
    BF = 2
    Tutorial_Scr_Bf = 3
    Unknown_Func_Bf = 4


def rebuildBlockLines(blockLines, msgFile, translatedMsg, blockIndex):
    if msgFile == "evt_introduction.bmd.msg":
        print()
    transMsgLines = []
    for lineInfoIndex in range(len(blockLines)):
        # text = lineInfo[0] #TODO hand over the translatedMsg logic to outside
        translatedMsgLine = translatedMsg[
            "{}_{}_{}_{}".format(msgFile, blockIndex, lineInfoIndex, 0)
        ]
        lineInfo = blockLines[lineInfoIndex]
        ctlStrs = lineInfo[1]
        reJoinedLine = ""
        for index in range(len(ctlStrs)):
            reJoinedLine += ctlStrs[index]
            if index < 1:  # 文本都被合并成一行了
                # replace chars before insert [n], otherwise [n] would be replaced
                replacedLine = replaceZhToJpKanji(translatedMsgLine)
                reJoinedLine += joinNewLineCtlStr(replacedLine)
        transMsgLines.append(reJoinedLine)
    transMsgLines.append("\n")
    # transMsgLines.append("\n")
    return transMsgLines


def rebuildBlockHeader(blockData):
    # TODO translate speaker name
    # TODO BUG 寄，speaker是没翻译的，编码中可能不包含这些文字
    block = blockData
    speaker = block["speaker"]
    transSpeaker = replaceZhToJpKanji(speaker)
    header = "{}{}{}".format(block["header"][0], transSpeaker, block["header"][1])
    return header


def rebuilMsg(rawData, translatedMsg, msgFile):
    msgFileData = rawData
    transMsgLines = []
    for blockIndex in range(len(msgFileData)):
        if blockIndex == 28:
            print()
        block = msgFileData[blockIndex]
        header = rebuildBlockHeader(block)
        transMsgLines.append(header)
        blockLines = rebuildBlockLines(
            block["linesInfo"], msgFile, translatedMsg, blockIndex
        )
        transMsgLines += blockLines
    return transMsgLines


def rebuilMsgFile(rawData, translatedMsg, msgFile, outputPath):
    transMsgLines = rebuilMsg(rawData, translatedMsg, msgFile)
    with open(outputPath, "w") as file:
        for line in transMsgLines:
            if line != "\n":
                file.write(line + "\n")
            else:
                file.write(line)
    return


def recompileMsg(msgFile, msgOutPutRoot, fType):
    # 编译文件
    # TODO muti thread

    outPutMsgPath = os.path.join(msgOutPutRoot, msgFile)
    outputFileName = ""
    if fType == RecompileType.BF:
        compileParam = "-Compile -OutFormat V2 -Library pq2 -Encoding SJ"
        command = [
            atlusScriptCompiler,
            os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".flow")),
            outPutMsgPath,
            os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".msg.h")),
            compileParam,
        ]
        outputBfName = os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".flow.bf"))
        outputFileName = outputBfName

    elif fType == RecompileType.BMD:
        compileParam = "--Compile -OutFormat V1 -Library pq2 -Encoding SJ"
        command = [
            atlusScriptCompiler,
            outPutMsgPath,
            compileParam,
        ]
        outputFileName = os.path.join(
            msgOutPutRoot, msgFile.replace("bmd.msg", "bmd.msg.bmd")
        )

    elif fType == RecompileType.Tutorial_Scr_Bf:
        compileParam = "-Compile -OutFormat V2 -Library pq2 -Encoding SJ"
        command = [
            atlusScriptCompiler,
            os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".flow")),
            outPutMsgPath,
            os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".msg.h")),
            compileParam,
        ]
        outputBfName = os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".flow.bf"))
        outputFileName = outputBfName
    elif fType == RecompileType.Unknown_Func_Bf:
        compileParam = "--Compile -OutFormat V1 -Library pq2 -Encoding SJ"
        command = [
            atlusScriptCompiler,
            outPutMsgPath,
            compileParam,
        ]
        outputFileName = os.path.join(
            msgOutPutRoot, msgFile.replace(".bf.msg", ".bf.msg.bmd")
        )

    os.system(" ".join(command))
    return outputFileName


def rebuilAllMsg(unTransMsgPath, transMsgPath, reBuildRoot, fType):
    translatedMsg = loadJson(transMsgPath)
    rawMsg = loadJson(unTransMsgPath)
    recompiledFiles = []
    for msgFile in rawMsg:
        outputPath = os.path.join(reBuildRoot, msgFile)
        rebuilMsgFile(rawMsg[msgFile], translatedMsg, msgFile, outputPath)
        msgOutPutRoot = reBuildRoot
        if fType == RecompileType.BF:
            eventFolder = msgFile[:2] + "00"
            msgOutPutRoot = os.path.join(reBuildRoot, eventFolder)
        elif fType == RecompileType.Tutorial_Scr_Bf:
            msgOutPutRoot = reBuildRoot
        outputFileP = recompileMsg(msgFile, msgOutPutRoot, fType)
        recompiledFiles.append(outputFileP)
    return recompiledFiles


def rebuildFailBf(target, oriRoot, cacheRoot):
    # rebuild Bf file unable to decompile correctly
    # original bf file
    oriBfFilePath = os.path.join(oriRoot, target)
    oriBfFile = readBinFile(oriBfFilePath)
    # seach bmd file header of origin bf file ，truncate
    # 07 00 00 00 __ __ 00 00 4D 53 47 31 00 00 00 00  ........MSG1....
    bmdHeaderRegx = b"\x07\x00\x00\x00..\x00\x00\x4d\x53\x47\x31\x00\x00\x00\x00"
    bmdHeaderStartOffset = list(re.finditer(bmdHeaderRegx, oriBfFile))[0].start()
    oriBfFrontPart = oriBfFile[:bmdHeaderStartOffset]

    # build bmd file,
    msgFileName = target.replace(".bf", ".bf.msg")
    bmdFilePath = recompileMsg(msgFileName, cacheRoot, RecompileType.Unknown_Func_Bf)

    # concat origin bf file's front part bytes and  bmd bytes
    bmdFileBytes = readBinFile(bmdFilePath)
    rebuildBfBytes = list(oriBfFrontPart + bmdFileBytes)

    # fix whole file size
    totalFileSizeByte = valueToLittleBytes(len(rebuildBfBytes))
    rebuildBfBytes = fillToBytes(0x4, rebuildBfBytes, totalFileSizeByte)
    rebuildBfBytes = fillToBytes(0x6C, rebuildBfBytes, totalFileSizeByte)
    # fix message part(bmd) file size
    bmdFileSizeByte = bmdFileBytes[0x4 : 0x4 + 2]
    rebuildBfBytes = fillToBytes(0x58, rebuildBfBytes, bmdFileSizeByte)
    return bytes(rebuildBfBytes)
