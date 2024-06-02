# data/init/*.bmd
import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import dumBmds, getMsgLines, parseMsgFile
from common import dumpJson, cacheRoot, oriCPKRoot
from zh_common import unpackBin
from msg_parser import rebuilAllMsg, RecompileType


# parse .msg
def parseMsgs(cacheFolder):
    msgMap = {}
    msgNotJoined = ["msg_combine.bmd.msg", "msg_combine_lvup.bmd.msg"]
    files = os.listdir(cacheFolder)
    msgFile = [i for i in files if i.endswith(".bmd.msg")]
    for msgF in msgFile:
        shouldJoinLine = True
        if msgF in msgNotJoined:
            shouldJoinLine = False
        msgData = parseMsgFile(os.path.join(cacheFolder, msgF), shouldJoinLine)
        msgMap[msgF] = msgData
    return msgMap


def collect_msg(jsonOutPutRoot, unpackedPath, cacheFolderPath):
    unpackedPath = Path(unpackedPath)
    if not os.path.exists(cacheFolderPath):
        os.makedirs(cacheFolderPath, exist_ok=True)
    dumBmds(unpackedPath, cacheFolderPath)
    msgMap = parseMsgs(cacheFolderPath)
    os.chdir(jsonOutPutRoot)
    msgMapPath = "bmd.json"
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )
    print()


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
    rebuildBmds(codeWorkplace, cacheWorkplace, unpacedkWorkplace)


target = "cmbroot.arc"
pathParts = ["facility", "pack"]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
unpacedkWorkplace = Path().joinpath(cacheRoot, *pathParts, target.replace(".", "_"))
cacheWorkplace = str(unpacedkWorkplace) + "_cache"
oriBinPath = Path().joinpath(oriCPKRoot, *pathParts, target)
cacheBinPath = Path().joinpath(cacheRoot, *pathParts, target)

if __name__ == "__main__":

    # collect_msg(codeWorkplace, unpacedkWorkplace, cacheWorkplace)
    rebuildAllBmd()
