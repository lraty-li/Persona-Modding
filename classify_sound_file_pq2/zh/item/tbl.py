from pathlib import Path
import sys, os

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from tbl_common import parseTblMsg
from common import dumpJson

if __name__ == "__main__":
    targets = [
        "skyitemequipeffect.tbl",
        "seaitemname.tbl",
        "equipitemnametable.tbl",
        "limititemnametable.tbl",
        "seaitemequipeffect.tbl",
        "skyitemname.tbl",
        "useitemnametable.tbl",
    ]

    cacheRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\item"
    msgMap = {}
    for tblF in targets:
        msgs = parseTblMsg(Path().joinpath(cacheRoot, tblF))
        msgMap[tblF] = msgs
    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\item")
    dumpJson("tbl.json", msgMap)
    # flatten
    flattenMap = {}
    for tblF in msgMap:
        msgInfos = msgMap[tblF]
        for index in range(len(msgInfos)):
            msg = msgInfos[index][0][0]
            flattenMap["{}_{}".format(tblF, index)] = msg
    dumpJson("tbl-parts.json", flattenMap)
    print()
