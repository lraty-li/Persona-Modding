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


def collectMsg(jsonOutPutRoot, unpackedPath):

    createPath(decompiledCacheFolder)
    dumBmds(unpackedPath, decompiledCacheFolder)
    msgMap = parseMsgs(decompiledCacheFolder)
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

targetBin = 'btl_com.arc'
pathParts = ["battle", "pack",]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))

cacheWorkplace = Path().joinpath(cacheRoot, *pathParts, targetBin.replace('.','_'))
reBuildBinRoot = cacheWorkplace
unpackedToPath = Path(cacheWorkplace)
decompiledCacheFolder = os.path.join(
    unpackedToPath.parent, unpackedToPath.name + "_cache"
)


def rebuildAllBmd():
    rebuildBmds(
        codeWorkplace,
        decompiledCacheFolder,
        reBuildBinRoot,
    )


if __name__ == "__main__":
    # collectMsg(str(codeWorkplace),cacheWorkplace)
    rebuildAllBmd()
