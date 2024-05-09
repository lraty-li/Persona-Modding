import json, os, shutil


scriptCompiler = r"f:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"
reBuildCPKroot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\output_workplace\datacpk\event"
msgRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\event"
translatedMsgPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\build_fake_charset\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-maped.json"
zhChar2JpKanjiPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\build_fake_charset\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-zhChar2JpKanji.json"
JpKanji2zhCharPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\build_fake_charset\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-JpKanji2zhChar.json"
rawMsgPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\msg_-ai_transl.json"


def loadJson(filePath):
    with open(filePath, "r") as file:
        return json.loads(file.read())


def replaceZhToJpKanji(text):
    replacedLine = ""
    for char in text:
        if char in zhChar2JpKanji.keys():
            replacedLine += zhChar2JpKanji[char]
        else:
            replacedLine += char  # 被跳过的部分，所以不会有编码
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


translatedMsg = loadJson(translatedMsgPath)
zhChar2JpKanji = loadJson(zhChar2JpKanjiPath)
JpKanji2zhChar = loadJson(JpKanji2zhCharPath)
rawMsg = loadJson(rawMsgPath)

transedMsgToBeWrite = {}
for msgFile in rawMsg:
    transMsgLines = []
    msgFileData = rawMsg[msgFile]
    for blockIndex in range(len(msgFileData)):
        block = msgFileData[blockIndex]
        header = block["header"]
        transMsgLines.append(header)
        for lineInfoIndex in range(len(block["linesInfo"])):
            # text = lineInfo[0]
            translatedMsgLine = translatedMsg[
                "{}_{}_{}_{}".format(msgFile, blockIndex, lineInfoIndex, 0)
            ]
            lineInfo = block["linesInfo"][lineInfoIndex]
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
        transMsgLines.append("\n")
    transedMsgToBeWrite[msgFile] = transMsgLines
    # 写入文件
    eventFolder = msgFile[:2] + "00"
    msgOutPutRoot = os.path.join(msgRoot, eventFolder)
    outPutMsgPath = os.path.join(msgOutPutRoot, msgFile)
    with open(outPutMsgPath, "w") as file:
        for line in transMsgLines:
            if line != "\n":
                file.write(line + "\n")
            else:
                file.write(line)

    # 编译文件
    # TODO BUG 寄，speaker是没翻译的，编码中可能不包含这些文字
    command = [
        scriptCompiler,
        os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".flow")),
        outPutMsgPath,
        os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".msg.h")),
        "-Compile -OutFormat V2 -Library pq2 -Encoding SJ",
    ]
    os.system(" ".join(command))
    outPutBFname = os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".flow.bf"))
    shutil.copy(
        outPutBFname,
        os.path.join(reBuildCPKroot, eventFolder, msgFile.replace(".msg", "")),
    )

print("DONE")
