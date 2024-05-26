from pathlib import Path
import sys, os

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from tbl_common import parseTblMsg
from common import dumpJson

if __name__ == "__main__":
    targets = [
        "skillnametable.tbl",
        "enemynametable.tbl",
        "enemyskillnametable.tbl",
        "playerskillnametable.tbl",
        "personanametable.tbl",
    ]

    cacheRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\table"
    msgMap = {}
    for tblF in targets:
        msgs = parseTblMsg(Path().joinpath(cacheRoot, tblF))
        msgMap[tblF] = msgs
    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\table")
    dumpJson("tbl.json", msgMap)
    # flatten
    flattenMap = {}
    for tblF in msgMap:
        msgInfos = msgMap[tblF]
        for index in range(len(msgInfos)):
            # skillnametable 的第一条还真是空的...
            if(len(msgInfos[index][0]) == 0):
                msg = ''
            else:
                msg = msgInfos[index][0][0]
            flattenMap["{}_{}".format(tblF, index)] = msg
    dumpJson("tbl-parts.json", flattenMap)
    print()
