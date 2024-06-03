import shutil
import sys, os
from pathlib import Path


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import writeBinFile, cacheRoot, oriCPKRoot, rebuildCPKRoot
from zh_common import unpackBin
from arc_common import getArcFileNames, rebuildArcBytes

# from zh_common import repackBin


def repack():

    repackTargets = getArcFileNames(oriBinPath, arcHeader)
    repackedArcBytes = rebuildArcBytes(unpacedkWorkplace, repackTargets, arcHeader)
    writeBinFile(rebuildBinPath, repackedArcBytes)


def dumpFromOri():
    shutil.copy(
        oriBinPath,
        cacheBinPath,
    )
    unpackBin(cacheBinPath)


target = "top.arc"
arcHeader = b"\x04\x00\x00\x00"
pathParts = ["facility", "pack"]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
unpacedkWorkplace = Path().joinpath(cacheRoot, *pathParts, target.replace(".", "_"))
cacheWorkplace = str(unpacedkWorkplace) + "_cache"
oriBinPath = Path().joinpath(oriCPKRoot, *pathParts, target)
cacheBinPath = Path().joinpath(cacheRoot, *pathParts, target)
rebuildBinPath = Path().joinpath(rebuildCPKRoot, *pathParts, target)


if __name__ == "__main__":
    # dumpFromOri()
    repack()
