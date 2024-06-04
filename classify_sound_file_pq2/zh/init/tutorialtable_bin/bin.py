import shutil
import sys, os
from pathlib import Path


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import writeBinFile, cacheRoot, oriCPKRoot, rebuildCPKRoot
from zh_common import unpackBin,repackBin
from arc_common import getArcFileNames, rebuildArcBytes

# from zh_common import repackBin


def repack():

    repackBin(unpacedkWorkplace, rebuildBinPath)

def dumpFromOri():
    shutil.copy(
        oriBinPath,
        cacheBinPath,
    )
    unpackBin(cacheBinPath)


target = "tutorialtable.bin"
pathParts = ["init",]
codeWorkplace = os.path.dirname(os.path.abspath(__file__))
unpacedkWorkplace = Path().joinpath(cacheRoot, *pathParts, target.replace(".", "_"))
cacheWorkplace = str(unpacedkWorkplace) + "_cache"
oriBinPath = Path().joinpath(oriCPKRoot, *pathParts, target)
cacheBinPath = Path().joinpath(cacheRoot, *pathParts, target)
rebuildBinPath = Path().joinpath(rebuildCPKRoot, *pathParts, target)


if __name__ == "__main__":
    # dumpFromOri()
    repack()
