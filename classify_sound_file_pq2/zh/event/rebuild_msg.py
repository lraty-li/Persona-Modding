import os, shutil

import sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import atlusScriptCompiler,replaceZhToJpKanji, joinNewLineCtlStr,notFoundedCharWhenReplace
from common import rebuildCPKRoot, loadJson


reBuildCPKEventroot = os.path.join(rebuildCPKRoot, "event")
msgRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\event"

translatedMsgPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-maped.json"
translatedMsg = loadJson(translatedMsgPath)

rawMsgPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\msg_-ai_transl.json"

transedMsgToBeWrite = {}
rawMsg = loadJson(rawMsgPath)
failTargets = []
for msgFile in rawMsg:
    transMsgLines = []
    msgFileData = rawMsg[msgFile]
    for blockIndex in range(len(msgFileData)):
        block = msgFileData[blockIndex]
        # TODO translate speaker name
        speaker = block["speaker"]
        # if(len(speaker) != 0):
        #     print()
        transSpeaker = replaceZhToJpKanji(speaker)
        header = "{}{}{}".format(block["header"][0], transSpeaker, block["header"][1])
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
                else:
                    raise Exception 
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
    # TODO muti thread
    command = [
        atlusScriptCompiler,
        os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".flow")),
        outPutMsgPath,
        os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".msg.h")),
        "-Compile -OutFormat V2 -Library pq2 -Encoding SJ",
    ]
    os.system(" ".join(command))
    outPutBFname = os.path.join(msgOutPutRoot, msgFile.replace(".msg", ".flow.bf"))
    try:
        shutil.copy(
            outPutBFname,
            os.path.join(reBuildCPKEventroot, eventFolder, msgFile.replace(".msg", "")),
        )
        pass
    except FileNotFoundError as e:
        # recompile fail
        # TODO just bypass now
        # but the way to insert zh msg into bf file need still
        failTargets.append(msgFile)


print("fails")
print(failTargets)
print(notFoundedCharWhenReplace)
print("DONE")
