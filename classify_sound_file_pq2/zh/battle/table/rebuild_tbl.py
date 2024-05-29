import sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import writeBinFile
from tbl_common import rebuildTblBytes

def rebuildTbl():

    rawJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\table\tbl.json"
    translatedJson = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\table\tbl-parts-zh.json"
    )
    repackCpkRoot = r"F:\TMP\cpk_output_workplace\datacpk\battle\table"
    data = rebuildTblBytes(rawJson, translatedJson)
    for tblF in data:
        writeBinFile(Path().joinpath(repackCpkRoot, tblF), data[tblF])

if __name__ == "__main__":
    rebuildTbl()