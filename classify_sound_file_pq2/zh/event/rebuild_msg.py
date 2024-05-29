import os, shutil

import sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import (
    replaceZhToJpKanji,
    joinNewLineCtlStr,
    notFoundedCharWhenReplace,
)
from msg_parser import rebuilMsgFile
from common import rebuildCPKRoot, loadJson, atlusScriptCompiler

def rebuildEventMsg():

    reBuildCPKEventroot = os.path.join(rebuildCPKRoot, "event")
    msgRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\event"

    translatedMsgPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-maped.json"
    translatedMsg = loadJson(translatedMsgPath)

    rawMsgPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\msg_-ai_transl.json"

    transedMsgToBeWrite = {}
    rawMsg = loadJson(rawMsgPath)
    failTargets = []
    for msgFile in rawMsg:
        # transMsgLines = []
        # msgFileData = rawMsg[msgFile]
        # for blockIndex in range(len(msgFileData)):
        #     block = msgFileData[blockIndex]
        #     # TODO translate speaker name
        #     speaker = block["speaker"]
        #     # if(len(speaker) != 0):
        #     #     print()
        #     transSpeaker = replaceZhToJpKanji(speaker)
        #     header = "{}{}{}".format(block["header"][0], transSpeaker, block["header"][1])
        #     transMsgLines.append(header)
        #     for lineInfoIndex in range(len(block["linesInfo"])):
        #         # text = lineInfo[0]
        #         translatedMsgLine = translatedMsg[
        #             "{}_{}_{}_{}".format(msgFile, blockIndex, lineInfoIndex, 0)
        #         ]
        #         lineInfo = block["linesInfo"][lineInfoIndex]
        #         ctlStrs = lineInfo[1]
        #         reJoinedLine = ""
        #         for index in range(len(ctlStrs)):
        #             reJoinedLine += ctlStrs[index]
        #             if index < 1:  # 文本都被合并成一行了
        #                 # replace chars before insert [n], otherwise [n] would be replaced
        #                 replacedLine = replaceZhToJpKanji(translatedMsgLine)
        #                 reJoinedLine += joinNewLineCtlStr(replacedLine)
        #         transMsgLines.append(reJoinedLine)
        #     transMsgLines.append("\n")
        #     transMsgLines.append("\n")
        # transedMsgToBeWrite[msgFile] = transMsgLines
        # 写入文件
        eventFolder = msgFile[:2] + "00"
        msgOutPutRoot = os.path.join(msgRoot, eventFolder)
        outPutMsgPath = os.path.join(msgOutPutRoot, msgFile)
        rebuilMsgFile(rawMsg[msgFile], translatedMsg, msgFile, outPutMsgPath)

        # with open(outPutMsgPath, "w") as file:
        #     for line in transMsgLines:
        #         if line != "\n":
        #             file.write(line + "\n")
        #         else:
        #             file.write(line)

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

if __name__ == "__main__":
    rebuildEventMsg()

# print("fails")
# print(failTargets)
# print(notFoundedCharWhenReplace)
# print("DONE")
[
    "e808_020.bf.msg",
    "e808_030.bf.msg",
    "e808_040.bf.msg",
    "e808_050.bf.msg",
    "e808_060.bf.msg",
    "e808_120.bf.msg",
    "e808_130.bf.msg",
    "e810_060.bf.msg",
    "e813_080.bf.msg",
    "e818_030.bf.msg",
    "e818_040.bf.msg",
    "e821_060.bf.msg",
    "e824_050.bf.msg",
    "e828_040.bf.msg",
    "e828_045.bf.msg",
    "e835_030.bf.msg",
    "e835_040.bf.msg",
    "e840_060.bf.msg",
    "e843_030.bf.msg",
    "e843_035.bf.msg",
    "e843_040.bf.msg",
    "e843_045.bf.msg",
    "e843_060.bf.msg",
    "e846_035.bf.msg",
    "e846_040.bf.msg",
    "e846_060.bf.msg",
    "e846_070.bf.msg",
]
