import shutil
import sys, os
from pathlib import Path


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import createPath, dumpJson, writeBinFile, rebuildCPKRoot, oriCPKRoot
from arc_common import getArcFileNames, rebuildArcBytes

from msg_parser import RecompileType, dumBmds, getMsgLines, parseMsgFile, rebuilAllMsg
from common import cacheRoot
from zh_common import unpackBin


# parse .msg
def parseMsgs(cacheFolder):
    msgMap = {}
    files = os.listdir(cacheFolder)
    msgFile = [i for i in files if i.endswith(".bmd.msg")]
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(cacheFolder, msgF), joinMsgOneLine=False)
        msgMap[msgF] = msgData
    return msgMap


def collectMsg(jsonOutPutRoot, unpackedPath, decompiledCacheFolder):
    unpackBin(os.path.join(cacheWorkplaceRoot,target))
    createPath(decompiledCacheFolder)
    dumBmds(unpackedPath, decompiledCacheFolder)
    msgMap = parseMsgs(decompiledCacheFolder)
    msgMapPath = str(Path().joinpath(jsonOutPutRoot, "bmd.json"))
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


def rebuilArc():
    rebuildBmds(codeWorkplace, decompiledCacheFolder, unpackedToPath)
    repackTargets = getArcFileNames(oriArcPath, arcHeader)
    repackedArcBytes = rebuildArcBytes(unpackedToPath, repackTargets, arcHeader)
    writeBinFile(targetRebuildCpkPath, repackedArcBytes)


target = "skladdex.arc"
arcHeader = b"\x02\x00\x00\x00"
cacheWorkplaceRoot = Path().joinpath(cacheRoot, "camp")
targetRebuildCpkPath = Path().joinpath(rebuildCPKRoot, "camp", target)
oriArcPath = Path().joinpath(oriCPKRoot, "camp", target)
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
unpackedToPath = Path().joinpath(cacheWorkplaceRoot, target.replace(".", "_"))
decompiledCacheFolder = os.path.join(
    unpackedToPath.parent, unpackedToPath.name + "_cache"
)
if __name__ == "__main__":
    
    # collectMsg(str(codeWorkplace), unpackedToPath,decompiledCacheFolder)

    rebuilArc()
