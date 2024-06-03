# data/init/*.bmd
import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import dumBmds, getMsgLines, parseMsgFile
from common import dumpJson, rebuildCPKRoot, createPath, cacheRoot
from msg_parser import rebuilAllMsg, RecompileType


# parse .msg
def parseMsgs(cacheFolder):
    msgMap = {}
    files = os.listdir(cacheFolder)
    msgFile = [i for i in files if i.endswith(".bmd.msg")]
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(cacheFolder, msgF), joinMsgOneLine=False)
        msgMap[msgF] = msgData
    return msgMap


def collectMsg(jsonOutPutRoot, unpackedPath, cacheWorkplace):
    createPath(cacheWorkplace)
    dumBmds(unpackedPath, cacheWorkplace)
    msgMap = parseMsgs(cacheWorkplace)
    msgMapPath = str(Path().joinpath(jsonOutPutRoot, "bmd.json"))
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )
    return msgParts


def rebuildBmds(workplaceRoot, rebuildMsgOutputRoot, moveToRoot):
    rawJson = os.path.join(workplaceRoot, "bmd.json")
    zhJson = os.path.join(workplaceRoot, "bmd-parts-zh.json")

    transedBmds = rebuilAllMsg(rawJson, zhJson, rebuildMsgOutputRoot, RecompileType.BMD)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            moveToRoot, Path(bmdF).name.replace(".bmd.msg.bmd", ".bmd")
        )
        shutil.copy(bmdF, targetBmdf)


pathParts = ["facility", "pack"]
target = "top.arc"
# move to _cache, avoiding any side effect to repack
codeWorkplace = os.path.dirname(os.path.abspath(__file__))

unpacedkWorkplace = Path().joinpath(cacheRoot, *pathParts, target.replace(".", "_"))
cacheWorkplace = str(unpacedkWorkplace) + "_cache"
cacheBinPath = Path().joinpath(cacheRoot, *pathParts, target)
rebuildBinPath = Path().joinpath(rebuildCPKRoot, *pathParts, target)

def rebuildAllBmd():
    rebuildBmds(
        codeWorkplace,
        cacheWorkplace,
        unpacedkWorkplace,
    )


if __name__ == "__main__":
    # collectMsg(str(codeWorkplace),unpacedkWorkplace, cacheWorkplace)
    rebuildAllBmd()
