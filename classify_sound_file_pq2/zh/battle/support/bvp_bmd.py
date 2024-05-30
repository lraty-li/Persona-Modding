import re
import os, shutil, sys


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import (
    RecompileType,
    atlusScriptCompiler,
    parseMsgFile,
    getMsgLines,
    MsgMapType,
    rebuilAllMsg,
    rebuilMsgFile,
    recompileMsg,
)
from common import dumpJson, cacheRoot, createPath, loadJson, rebuildCPKRoot
from bvp_commom import unapckBvp, repackBvp
from pathlib import Path


def dumpAllBvps(folderRoot):
    unpacked = []
    fileTarges = [i for i in os.listdir(folderRoot) if i.endswith(".bvp")]

    for fileTarge in fileTarges:
        bvpFilePath = str(Path().joinpath(folderRoot, fileTarge))
        outputPath = unapckBvp(bvpFilePath, selfPath)
        unpacked.append(outputPath)
    return unpacked


def dumBmds(workplace, outputFolder):
    files = os.listdir(workplace)
    bmdFiles = [i for i in files if i.endswith(".BMD")]
    for bmdFile in bmdFiles:
        cacheBmdFile = os.path.join(outputFolder, bmdFile)
        shutil.copy(os.path.join(workplace, bmdFile), cacheBmdFile)
        command = [
            atlusScriptCompiler,
            cacheBmdFile,
            "--Decompile -Library pq2 -Encoding SJ",
        ]
        os.system(" ".join(command))


# parse .msg
def parseMsgs(targetFolder):
    msgMap = {}
    files = os.listdir(targetFolder)
    msgFile = [i for i in files if i.endswith(".BMD.msg")]
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(targetFolder, msgF))
        msgMap[msgF] = msgData
    return msgMap


def collect_msg(workplace, outputRoot):
    targets = [
        i.replace(".bvp", "") for i in os.listdir(workplace) if i.endswith(".bvp")
    ]
    allMspMap = {}
    for targ in targets:
        bvpWrokplace = Path().joinpath(workplace, targ)
        bvpCachePath = Path().joinpath(workplace, targ + "_cache")
        createPath(bvpCachePath)
        # dumBmds(bvpWrokplace, bvpCachePath)
        msgMap = parseMsgs(str(bvpCachePath))
        allMspMap[targ] = msgMap
    msgMapPath = Path().joinpath(outputRoot, "bvp-Bmd.json")
    dumpJson(msgMapPath, allMspMap)
    msgParts = getMsgLines(msgMapPath, outptJson=True, fType=MsgMapType.BVP)
    print()


def rebuilBvp():
    targets = [
        i.replace(".bvp", "") for i in os.listdir(workplace) if i.endswith(".bvp")
    ]
    rawJson = os.path.join(selfPath, "bvp-Bmd.json")
    rawMsg = loadJson(rawJson)
    zhJson = rawJson.replace(".json", "-parts-zh.json")
    translatedMsg = loadJson(zhJson)

    for targ in targets:
        bvpCacheFolder = str(Path().joinpath(workplace, targ + "_cache"))
        reBuildBvpRoot = Path().joinpath(workplace, targ)
        transedBmds = []
        for msgFile in rawMsg[targ]:
            rebuildMsgPath = Path().joinpath(bvpCacheFolder, msgFile)
            msgFilePrefixed = "{}_{}".format(targ, msgFile)  # 屎山啊屎山
            rebuilMsgFile(
                rawMsg[targ][msgFile], translatedMsg, msgFilePrefixed, rebuildMsgPath
            )
            outputFileP = recompileMsg(msgFile, bvpCacheFolder, RecompileType.BMD)
            transedBmds.append(outputFileP)
        for bmdF in transedBmds:
            # 真的有必要保留大小写么...
            matchSubFix = re.search("bmd", msgFile, re.IGNORECASE)
            bmdSubFix = msgFile[matchSubFix.start() : matchSubFix.end()]
            targetBmdf = Path().joinpath(
                reBuildBvpRoot,
                Path(bmdF).name.replace(
                    ".{}.msg.bmd".format(bmdSubFix), ".{}".format(bmdSubFix)
                ),
            )
            shutil.copy(bmdF, targetBmdf)
        # rebuild bvp

        repackBvp(reBuildBvpRoot)
        outputBvpPath = Path().joinpath(reBuildBvpRoot.parent, targ + ".bvp")
        shutil.copy(
            outputBvpPath,
            Path().joinpath(rebuildCPKRoot, "battle", "support", targ + ".bvp"),
        )


workplace = Path().joinpath(cacheRoot, "battle", "support")
selfPath = os.path.dirname(os.path.abspath(__file__))
# move to _cache, avoiding any side effect to repack
workplacePlib = Path(workplace)


if __name__ == "__main__":
    # dumpAllBvps(str(workplace))
    # collect_msg(workplace, selfPath)
    rebuilBvp()
