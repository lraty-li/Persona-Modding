# data/init/*.bmd
import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import getMsgLines, parseMsgFile
from common import dumpJson

# decompile all bmd
atlusScriptCompiler = (
    r"F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"
)

workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\event"


def dumpBfs(eventRoot):
    #!/usr/bin/python3
    deCompilerPath = (
        "F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"
    )

    import os, json

    # TODO 多线程
    bfFiles = {}
    for root, dirs, files in os.walk(eventRoot, topdown=False):
        for name in files:
            if name.endswith(".bf"):
                if root not in bfFiles.keys():
                    bfFiles[root] = [name]
                bfFiles[root].append(name)
                os.system(
                    deCompilerPath
                    + " "
                    + os.path.join(root, name).replace("\\", "/")
                    + " "
                    + "-Decompile -Library pq2 -Encoding SJ"
                )
                # print(os.path.join(root, name))

    print(len(bfFiles))


# parse .msg
def parseMsgs(folderRoot):
    msgMap = {}
    files = os.listdir(folderRoot)
    msgFile = [i for i in files if i.endswith(".msg")] #TODO .bf.msg
    for msgF in msgFile:
        msgData = parseMsgFile(os.path.join(folderRoot, msgF))
        msgMap[msgF] = msgData
    return msgMap


if __name__ == "__main__":
    eventRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\event"
    )
    dumpBfs(r'D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\event\support')

    # move to _cache, avoiding any side effect to repack
    workplacePlib = Path(workplace)
    cacheFolder = os.path.join(workplacePlib.parent, workplacePlib.name + "_cache")
    cacheFolder = workplace
    if not os.path.exists(cacheFolder):
        os.mkdir(cacheFolder)

    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event")

    msgMap = parseMsgs(cacheFolder)
    msgMapPath = "msg.json"
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )

    msgMap = parseMsgs(Path().joinpath(cacheFolder, "bgm"))
    msgMapPath = "msg-bgm.json"
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )

    msgMap = parseMsgs(Path().joinpath(cacheFolder, "support"))
    msgMapPath = "msg-support.json"
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )
    print()
