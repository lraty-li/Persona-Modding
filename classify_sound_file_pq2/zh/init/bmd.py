# data/init/*.bmd
import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import getMsgLines, parseMsgFile, dumBmds
from common import dumpJson, atlusScriptCompiler


# parse .msg
def parseMsgs(cacheFolder):
    msgMap = {}
    files = os.listdir(cacheFolder)
    msgFile = [i for i in files if i.endswith(".bmd.msg")]
    targetJoin = ['datquesthelp.bmd.msg']
    for msgF in msgFile:
        if(msgF in targetJoin):
            shouldJoinMsgOneLine = True
        else:
            shouldJoinMsgOneLine = False
        msgData = parseMsgFile(os.path.join(cacheFolder, msgF), shouldJoinMsgOneLine)
        msgMap[msgF] = msgData
    return msgMap

def collectMsg():
    # move to _cache, avoiding any side effect to repack
    workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init"
    workplacePlib = Path(workplace)
    cacheFolder = os.path.join(workplacePlib.parent, workplacePlib.name + "_cache")
    if not os.path.exists(cacheFolder):
        os.makedirs(cacheFolder, exist_ok=True)
    dumBmds(workplace, cacheFolder)
    msgMap = parseMsgs(cacheFolder)
    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init")
    msgMapPath = "bmd.json"
    dumpJson(msgMapPath, msgMap)
    msgParts = getMsgLines(
        msgMapPath,
    )

if __name__ == "__main__":
    
    collectMsg()

    # TODO 结果中有很多 0xA13
    # D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\dataccessory2help.bmd
    # 并且前后有函数调用？但反编译结果好像忽略掉了
    print()
