import os, shutil
import regex as re
from enum import Enum
from common import atlusScriptCompiler

from zh_common import (
    replaceZhToJpKanji,
    joinNewLineCtlStr,
)

from common import loadJson, dumpJson
from common import fillToBytes, valueToLittleBytes, readBinFile


class RecompileType(Enum):
    BMD = 1
    BF = 2
    Tutorial_Scr_Bf = 3
    Unknown_Func_Bf = 4


class MsgMapType(Enum):
    BMD = 1
    BVP = 2  # twice nested
    EVENT = 3


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


def _dashConcat(lList):
    return "_".join([str(i) for i in lList])


def _collectMapedLins(lineInfo, pathIndexs, inLineIndex=0):
    msgLine = lineInfo[0]
    mapEntry = {}
    mKey = ""
    if type(msgLine) == str:
        mKey = _dashConcat(pathIndexs + [0])
        mapEntry[mKey] = msgLine
    elif type(msgLine) == list:
        for msgInnerLineIndex in range(len(msgLine)):
            # if(spliter in msg):
            #     raise Exception("{} is in msg".format(spliter))
            mKey = _dashConcat(pathIndexs + [msgInnerLineIndex])
            mValue = lineInfo[0][msgInnerLineIndex]
            mapEntry[mKey] = mValue

    return mapEntry


def getMsgLines(msgMapPath, outptJson=True, fType=MsgMapType.BMD):
    msgPartsMap = {}
    msgMap = loadJson(msgMapPath)
    spliter = "|"
    msgPartsMap = {}
    for fileName in msgMap.keys():
        contenet = msgMap[fileName]
        if fType == MsgMapType.BMD:
            for blockIndex in range(len(contenet)):
                block = contenet[blockIndex]
                for lineInfoIndex in range(len(block["linesInfo"])):
                    lineInfo = block["linesInfo"][lineInfoIndex]
                    mappedEntry = _collectMapedLins(
                        lineInfo, [fileName, blockIndex, lineInfoIndex]
                    )
                    msgPartsMap.update(mappedEntry)
        elif fType == MsgMapType.BVP or fType == MsgMapType.EVENT:
            for targ in contenet:
                blocks = contenet[targ]
                for blockIndex in range(len(blocks)):
                    block = blocks[blockIndex]
                    for lineInfoIndex in range(len(block["linesInfo"])):
                        lineInfo = block["linesInfo"][lineInfoIndex]
                        mappedEntry = _collectMapedLins(
                            lineInfo, [fileName, targ, blockIndex, lineInfoIndex]
                        )
                        msgPartsMap.update(mappedEntry)
        else:
            raise Exception("unimplement")

    # G, 翻译会去掉分隔符，不如直接来吧
    if outptJson:
        dumpJson(str(msgMapPath).replace(".json", "-parts.json"), msgPartsMap)
    return msgPartsMap


def rebuildBlockLines(blockLines, msgFile, translatedMsg, blockIndex):
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
                # check if message is shiftjis
                # TODO fix charset
                #     "～": "～",
                reJoinedLine.encode("shiftjis")
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
        # 真的有必要保留大小写么...
        matchSubFix = re.search(r"(?<=\.).*(?=\.msg)", msgFile, re.IGNORECASE)
        if matchSubFix != None:
            bmdSubFix = msgFile[matchSubFix.start() : matchSubFix.end()]
        else:
            # fail bf, may be ***.bf.msg
            matchSubFix = "bmd"
            raise Exception("unable to match input file subfix")

        outputFileName = os.path.join(
            msgOutPutRoot,
            # 似乎编译结果固定返回小写
            msgFile.replace("{}.msg".format(bmdSubFix), "{}.msg.bmd".format(bmdSubFix)),
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
        outputPath = rebuildOneMsg(msgFile, reBuildRoot, rawMsg, translatedMsg, fType)
        recompiledFiles.append(outputPath)
    return recompiledFiles


def rebuildOneMsg(msgFile, reBuildRoot, rawMsg, translatedMsg, fType):
    outputPath = os.path.join(reBuildRoot, msgFile)
    rebuilMsgFile(rawMsg[msgFile], translatedMsg, msgFile, outputPath)
    msgOutPutRoot = reBuildRoot
    if fType == RecompileType.BF:
        eventFolder = msgFile[:2] + "00"
        msgOutPutRoot = os.path.join(reBuildRoot, eventFolder)
    elif fType == RecompileType.Tutorial_Scr_Bf:
        msgOutPutRoot = reBuildRoot
    outputFileP = recompileMsg(msgFile, msgOutPutRoot, fType)
    return outputFileP


def rebuildFailBf(target, oriRoot, cacheRoot, rawJsonPath):
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
    # TODO 之前的有没有重建message？
    rawJsonPath = os.path.join(cacheRoot, rawJsonPath)
    # TODO duplicate loading,hand over out all these map loading logic
    rawJson = loadJson(rawJsonPath)
    zhJson = loadJson(
        rawJsonPath.replace(".json", "-parts-zh.json"),
    )
    bmdFilePath = rebuildOneMsg(
        target + ".msg", cacheRoot, rawJson, zhJson, RecompileType.Unknown_Func_Bf
    )
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


def dumBmds(workplace, cacheFolder):
    files = os.listdir(workplace)
    bmdFiles = [i for i in files if i.endswith(".bmd")]
    for bmdFile in bmdFiles:
        cacheBmdFile = os.path.join(cacheFolder, bmdFile)
        shutil.copy(os.path.join(workplace, bmdFile), cacheBmdFile)
        command = [
            atlusScriptCompiler,
            cacheBmdFile,
            "--Decompile -Library pq2 -Encoding SJ",
        ]
        os.system(" ".join(command))
