import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import getMsgLines, parseMsgFile
from common import dumpJson
from zh_common import atlusScriptCompiler


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
                #copy to _cache
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
#TODO refactor, .bmd.msg, .bf.msg
def parseBfMsgs(folderRoot):
    msgMap = {}
    files = os.listdir(folderRoot)
    msgFile = [i for i in files if i.endswith(".bf.msg")]
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(folderRoot, msgF))
        msgMap[msgF] = msgData
    return msgMap


if __name__ == "__main__":
    workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\facility"
    # move to _cache, avoiding any side effect to repack
    workplacePlib = Path(workplace)
    cacheFolder = os.path.join(workplacePlib.parent, workplacePlib.name + "_cache")
    if not os.path.exists(cacheFolder):
        os.makedirs(cacheFolder, exist_ok=True)

    targets = dumpBfs(workplace, cacheFolder)

    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility")

    msgMap = parseBfMsgs(cacheFolder)
    msgMapPath = "msg.json"
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )
