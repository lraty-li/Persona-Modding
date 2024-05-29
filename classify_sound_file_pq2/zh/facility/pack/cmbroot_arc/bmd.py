# data/init/*.bmd
import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import dumBmds, getMsgLines, parseMsgFile
from common import dumpJson
from msg_parser import rebuilAllMsg, RecompileType


# parse .msg
def parseMsgs(cacheFolder):
    msgMap = {}
    files = os.listdir(cacheFolder)
    msgFile = [i for i in files if i.endswith(".bmd.msg")]
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(cacheFolder, msgF))
        msgMap[msgF] = msgData
    return msgMap


def collect_msg(jsonOutPutRoot, unpackedPath):
    unpackedPath = Path(unpackedPath)
    cacheFolder = os.path.join(unpackedPath.parent, unpackedPath.name + "_cache")
    if not os.path.exists(cacheFolder):
        os.makedirs(cacheFolder, exist_ok=True)
    dumBmds(unpackedPath, cacheFolder)
    msgMap = parseMsgs(cacheFolder)
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


workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\pack\cmbroot_arc"

# unpacedkWorkplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\facility\pack\cmbroot_arc"
# collect_msg(workplace, unpacedkWorkplace)

cacheRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache"
cacheWorkplace = cacheRoot + r"\facility\pack\cmbroot_arc_cache"
reBuildBinRoot = cacheRoot + r"\facility\pack\cmbroot_arc"

def rebuildAllBmd():
    rebuildBmds(workplace, cacheWorkplace, reBuildBinRoot)

if __name__ == "__main__":
    rebuildAllBmd()
