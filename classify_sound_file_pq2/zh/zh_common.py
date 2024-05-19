import json
import os
from pathlib import Path
pakPack = "f:\modding\persona-tools\AtlusFileSystemLibrary-release\PAKPack.exe"
atlusScriptCompiler = (
    r"F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"
)

# build the charset need
zhChar2JpKanjiPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\build_fake_charset\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-zhChar2JpKanji.json"
JpKanji2zhCharPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\build_fake_charset\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-JpKanji2zhChar.json"


def loadJson(filePath):
    with open(filePath, "r") as file:
        return json.loads(file.read())


def dumpJson(filePath, data):
    with open(
        filePath,
        "w",
    ) as file:
        file.write(json.dumps(data, ensure_ascii=False))


def replaceZhToJpKanji(text):
    replacedLine = ""
    for char in text:
        if char in zhChar2JpKanji.keys():
            replacedLine += zhChar2JpKanji[char]
        else:
            print("WARN: {} not found in zhChar2JpKanji".format(char))
            #TODO 区分是跳过部分还是无编码
            # replacedLine += char  # 被跳过的部分，所以不会有编码
            replacedLine += ' '  # 被跳过的部分，所以不会有编码
    return replacedLine


SPLITERS = ["，", "。", "？", "…", "?", "!", "."]
NEW_LINE_THREADHOLD = 22


def joinNewLineCtlStr(text):
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
    command = [pakPack, "unpack", filePath, str(outputPath)]
    os.system(" ".join(command))


def repackBin(folderPath, outputPath=None):
    targPth = Path(folderPath)
    if outputPath == None:
        outputPath = os.path.join(targPth.parent, targPth.name.replace("_", "."))
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    command = [pakPack, "pack", folderPath, "v2", outputPath]
    os.system(" ".join(command))


zhChar2JpKanji = loadJson(zhChar2JpKanjiPath)
JpKanji2zhChar = loadJson(JpKanji2zhCharPath)
