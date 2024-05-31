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


def parseBfMsgs(folderRoot):
    msgMap = {}
    files = os.listdir(folderRoot)
    msgFile = [i for i in files if i.endswith(".bf.msg")]
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(folderRoot, msgF))
        msgMap[msgF] = msgData
    return msgMap


def collectMsg():
    if not os.path.exists(cacheFolder):
        os.makedirs(cacheFolder, exist_ok=True)

    targets = dumpBfs(str(workplace), cacheFolder)

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
    reBuildRoot = cacheFolder
    targetFile = 'cmppoem.bf'
    rebuildBytes = rebuildFailBf(
        targetFile, workplace, cacheFolder, os.path.join(codeWorkplace, "msg.json")
    )
    writeBinFile(Path().joinpath(rebuildCpkFolder, targetFile), rebuildBytes)


workplace = Path().joinpath(cacheRoot, "camp")
rebuildCpkFolder = Path().joinpath(rebuildCPKRoot, "camp")
# move to _cache, avoiding any side effect to repack
codeWorkplace = os.path.dirname(os.path.abspath(__file__))

cacheFolder = os.path.join(workplace.parent, workplace.name + "_cache")
if __name__ == "__main__":

    # collectMsg()

    rebuildBf()
