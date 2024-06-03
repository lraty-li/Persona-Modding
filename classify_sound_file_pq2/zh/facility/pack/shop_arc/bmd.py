# data/init/*.bmd
import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import dumBmds, getMsgLines, parseMsgFile
from common import createPath, dumpJson, cacheRoot, rebuildCPKRoot
from msg_parser import rebuilAllMsg, RecompileType


# parse .msg
def parseMsgs(cacheFolder):
    msgMap = {}
    files = os.listdir(cacheFolder)
    notJoinTargets = ["msg_combine.bmd.msg", "msg_weapon.bmd.msg"]
    msgFile = [i for i in files if i.endswith(".bmd.msg")]
    for msgF in msgFile:
        shouldJoinLine = True
        if msgF in notJoinTargets:
            shouldJoinLine = False
        msgData = parseMsgFile(
            os.path.join(cacheFolder, msgF), joinMsgOneLine=shouldJoinLine
        )
        msgMap[msgF] = msgData
    return msgMap


def collect_msg():
    createPath(decompiledCacheFolder)
    dumBmds(unpackedToPath, decompiledCacheFolder)
    msgMap = parseMsgs(decompiledCacheFolder)
    msgMapPath = str(Path().joinpath(codeWorkplace, "bmd.json"))
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )
    return msgParts


def rebuildBmds(workplaceRoot, reBuildRoot, reBuildBinRoot):
    rawJson = os.path.join(workplaceRoot, "bmd.json")
    zhJson = os.path.join(workplaceRoot, "bmd-parts-zh.json")
    transedBmds = rebuilAllMsg(rawJson, zhJson, reBuildRoot, RecompileType.BMD)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bmd.msg.bmd", ".bmd")
        )
        shutil.copy(bmdF, targetBmdf)


def rebuildAllBmd():
    rebuildBmds(codeWorkplace, cacheWorkplace, reBuildBinRoot)


targetFile = "shop.arc"
pathPatrs = ["facility", "pack"]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
cacheWorkplace = Path().joinpath(cacheRoot, *pathPatrs)
reBuildBinRoot = Path().joinpath(rebuildCPKRoot, *pathPatrs)
unpackedToPath = Path().joinpath(cacheWorkplace, targetFile.replace(".", "_"))
decompiledCacheFolder = os.path.join(
    unpackedToPath.parent, unpackedToPath.name + "_cache"
)


if __name__ == "__main__":
    # collect_msg()

    rebuildBmds(codeWorkplace, decompiledCacheFolder, unpackedToPath)
