import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import (
    getMsgLines,
    parseMsgFile,
    rebuilAllMsg,
    rebuildFailBf,
    RecompileType,
)
from common import (
    dumpJson,
    atlusScriptCompiler,
    writeBinFile,
    cacheRoot,
    rebuildCPKRoot,
)


def dumpBfs(eventRoot, cacheRoot):

    import os, json

    # TODO 多线程
    bfFiles = {}
    for root, dirs, files in os.walk(eventRoot, topdown=False):
        for name in files:
            if name.endswith(".bf"):
                if root not in bfFiles.keys():
                    bfFiles[root] = [name]
                bfFiles[root].append(name)
                targetPath = os.path.join(root, name).replace("\\", "/")
                cacheTargetRoot = root.replace(eventRoot, cacheRoot)
                if not os.path.exists(cacheTargetRoot):
                    os.makedirs(cacheTargetRoot, exist_ok=True)
                cacheTargetPath = os.path.join(cacheTargetRoot, name).replace("\\", "/")
                # copy to _cache
                shutil.copy(targetPath, cacheTargetPath)
                os.system(
                    atlusScriptCompiler
                    + " "
                    + cacheTargetPath
                    + " "
                    + "-Decompile -Library pq2 -Encoding SJ"
                )
                # print(os.path.join(root, name))

    print(len(bfFiles))
    return bfFiles


# parse .bf.msg
# TODO refactor, .bmd.msg, .bf.msg
def parseBfMsgs(folderRoot):
    msgMap = {}
    files = os.listdir(folderRoot)
    msgFile = [i for i in files if i.endswith(".bf.msg")]
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(folderRoot, msgF))
        msgMap[msgF] = msgData
    return msgMap


def collectMsg():
    cacheFolder = cacheWorkplace
    workplace = str(unpacedkWorkplace)
    if not os.path.exists(cacheFolder):
        os.makedirs(cacheFolder, exist_ok=True)

    targets = dumpBfs(workplace, cacheFolder)

    msgMap = parseBfMsgs(cacheFolder)
    msgMapPath = str(Path().joinpath(codeWorkplace, "msg.json"))
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )
    return msgParts

def rebuildBf():

    rawJson = Path().joinpath(codeWorkplace, "msg.json")
    zhJson = Path().joinpath(codeWorkplace, "msg-parts-zh.json")
    transedBmds = rebuilAllMsg(
        rawJson, zhJson, cacheWorkplace, RecompileType.Tutorial_Scr_Bf
    )
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            unpacedkWorkplace, Path(bmdF).name.replace(".bf.flow.bf", ".bf")
        )
        shutil.copy(bmdF, str(targetBmdf))


target = "cmbroot.arc"
pathParts = ["facility", "pack"]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
unpacedkWorkplace = Path().joinpath(cacheRoot, *pathParts, target.replace(".", "_"))
cacheWorkplace = str(unpacedkWorkplace) + "_cache"
# oriBinPath = Path().joinpath(oriCPKRoot, *pathParts, target)
cacheBinPath = Path().joinpath(cacheRoot, *pathParts, target)
rebuildBinPath = Path().joinpath(rebuildCPKRoot, *pathParts, target)

if __name__ == "__main__":

    # collectMsg()

    rebuildBf()
