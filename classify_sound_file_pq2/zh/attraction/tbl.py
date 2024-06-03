from pathlib import Path
import sys, os

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from tbl_common import parseTblMsg, rebuildTblBytes
from common import dumpJson, cacheRoot, writeBinFile, rebuildCPKRoot


def collectMsg():
    targets = [i for i in os.listdir(cacheWorkplaceRoot) if i.endswith(".tbl")]
    msgMap = {}
    for tblF in targets:
        msgs = parseTblMsg(Path().joinpath(cacheWorkplaceRoot, tblF))
        msgMap[tblF] = msgs
    outputJsonPath = os.path.join(codeWorkplace, "tbl.json")
    dumpJson(outputJsonPath, msgMap)
    # flatten
    flattenMap = {}
    for tblF in msgMap:
        msgInfos = msgMap[tblF]
        for index in range(len(msgInfos)):
            msg = msgInfos[index][0][0]
            flattenMap["{}_{}".format(tblF, index)] = msg
    dumpJson(outputJsonPath.replace(".json", "-parts.json"), flattenMap)
    print()


def rebuildTbl():
    rawJson = Path().joinpath(codeWorkplace, "tbl.json")
    translatedJson = Path().joinpath(codeWorkplace, "tbl-parts-zh.json")
    repackCpkRoot = Path().joinpath(rebuildCPKRoot, *pathParts)
    data = rebuildTblBytes(rawJson, translatedJson)
    for tblF in data:
        writeBinFile(Path().joinpath(repackCpkRoot, tblF), data[tblF])


pathParts = ["attraction"]
cacheWorkplaceRoot = Path().joinpath(cacheRoot, *pathParts)
codeWorkplace = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    # collectMsg()
    rebuildTbl()
    print()
