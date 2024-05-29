import sys, os
from pathlib import Path


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import (
    writeBinFile,
)
from arc_common import getArcFileNames, rebuildArcBytes

# from zh_common import repackBin


def rebuilArc():
    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\pack")
    arcHeader = b"\x04\x00\x00\x00"

    cpkRoot = r"F:\TMP\cpk_output_workplace\datacpk\facility\pack"
    arcUnpackedPath = os.path.join(targetRoot, targetFile.replace(".", "_"))

    oriArcPath = r"F:\TMP\cpk_output_workplace\ori-data\facility\pack\shop.arc"
    repackTargets = getArcFileNames(oriArcPath, arcHeader)
    repackedArcBytes = rebuildArcBytes(arcUnpackedPath, repackTargets, arcHeader)
    writeBinFile(os.path.join(cpkRoot, targetFile), repackedArcBytes)


targetRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\facility\pack"
targetFile = "shop.arc"
if __name__ == "__main__":
    # unpackBin(os.path.join(targetRoot,targetFile))

    rebuilArc()
