# data/init/*.bmd
import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import getMsgLines, parseMsgFile
from zh_common import dumpJson, atlusScriptCompiler


def dumBmds(cacheFolder):
    files = os.listdir(workplace)
    bmdFiles = [i for i in files if i.endswith(".bmd")]
    for bmdFile in bmdFiles:
        cacheBmdFile = os.path.join(cacheFolder, bmdFile)
        shutil.copy(os.path.join(workplace, bmdFile), cacheBmdFile)
        command = [
            atlusScriptCompiler,
            cacheBmdFile,
            "--Decompile -Library pq2 -Encoding SJ",
        ]
        os.system(" ".join(command))


# parse .msg
def parseMsgs(cacheFolder):
    msgMap = {}
    files = os.listdir(cacheFolder)
    msgFile = [i for i in files if i.endswith(".msg")]
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(cacheFolder, msgF))
        msgMap[msgF] = msgData
    return msgMap


if __name__ == "__main__":
    selfRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt"
    workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\event\txt"

    # evt_introduction.bmd

    # move to _cache, avoiding any side effect to repack cmptable_bin
    workplacePlib = Path(workplace)
    cacheFolder = os.path.join(workplacePlib.parent, workplacePlib.name + "_cache")
    if not os.path.exists(cacheFolder):
        os.mkdir(cacheFolder)
    dumBmds(cacheFolder)
    msgMap = parseMsgs(cacheFolder)
    os.chdir(cacheFolder)
    # msgMapPath = Path(workplace).stem + "-bmd.json"
    msgMapPath = str(Path().joinpath(selfRoot, "bmd.json"))
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )
    print()
