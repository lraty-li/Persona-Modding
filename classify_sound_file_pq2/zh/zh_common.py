import os
from pathlib import Path

from common import loadJson, zhChar2JpKanjiPath, JpKanji2zhCharPath

pakPack = "f:\modding\persona-tools\AtlusFileSystemLibrary-release\PAKPack.exe"


zhChar2JpKanji = loadJson(zhChar2JpKanjiPath)
JpKanji2zhChar = loadJson(JpKanji2zhCharPath)

# clear?
notFoundedCharWhenReplace = []


def replaceZhToJpKanji(text):
    replacedLine = ""
    for char in text:
        if char in zhChar2JpKanji.keys():
            replacedLine += zhChar2JpKanji[char]
        else:
            # TODO 区分是跳过部分还是无编码
            # replacedLine += char  # 被跳过的部分，所以不会有编码
            if char in JpKanji2zhChar.keys():
                replacedLine += " "
            else:
                print(
                    "WARN: {} not found in zhChar2JpKanji or JpKanji2zhChar".format(
                        char
                    )
                )
                replacedLine += " "
                notFoundedCharWhenReplace.append(char)
    return replacedLine


def replaceZhToJpKanjiBytes(text, targetBytesLength, filling=b"\x00", center=True):
    textRp = replaceZhToJpKanji(text)
    textRpBytes = textRp.encode("shiftjis")
    lengthDiff = targetBytesLength - len(textRpBytes)
    if lengthDiff < 0:
        textRpBytes = textRpBytes[:lengthDiff]
    else:
        if center:
            textRpBytes = (
                filling * int(lengthDiff / 2)
                + textRpBytes
                + filling * int((lengthDiff + 1) / 2)
            )
        else:
            textRpBytes = textRpBytes + filling * int(lengthDiff)
    return textRpBytes


SPLITERS = ["，", "。", "？", "…", "?", "!", "."]
# \"
NEW_LINE_THREADHOLD = 18


def joinNewLineCtlStr(text):
    # TODO custom NEW_LINE_THREADHOLD
    if len(text) > NEW_LINE_THREADHOLD:
        splited = False
        for spliter in SPLITERS:
            if spliter in text:
                spliterIndex = text.rfind(spliter)
                frontPart = joinNewLineCtlStr(text[:spliterIndex])
                if spliterIndex + 1 == len(text):
                    backPart = ""
                else:
                    backPart = joinNewLineCtlStr(text[spliterIndex + 1 :])
                return "{}{}[n]{}".format(frontPart, spliter, backPart)
        if not splited:
            # 后部的文本就是很长，没有标点符号,直接折半
            frontPart = joinNewLineCtlStr(text[: int(len(text) / 2)])
            backPart = joinNewLineCtlStr(text[int(len(text) / 2) :])
            return "{}[n]{}".format(frontPart, backPart)
            # raise Exception("not splited")
    else:
        return text


def unpackBin(filePath, outputPath=None):
    targPth = Path(filePath)
    if outputPath == None:
        outputPath = Path().joinpath(targPth.parent, targPth.name.replace(".", "_"))
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    command = [pakPack, "unpack", str(filePath), str(outputPath)]
    os.system(" ".join(command))


def repackBin(folderPath, outputPath=None):
    targPth = Path(folderPath)
    if outputPath == None:
        outputPath = os.path.join(targPth.parent, targPth.name.replace("_", "."))
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    command = [pakPack, "pack", str(folderPath), "v2", str(outputPath)]
    os.system(" ".join(command))
    return outputPath
