import sys, os
from pathlib import Path



sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import (
    writeBinFile,
)
from zh_common import unpackBin
from arc_common import getArcFileNames, rebuildArcBytes
# from zh_common import repackBin

def repack():
    arcUnpackedPath = os.path.join(targetRoot, targetFile.replace(".", "_"))

    repackTargets = getArcFileNames(oriArcPath)
    repackedArcBytes = rebuildArcBytes(
        arcUnpackedPath,
        repackTargets,
    )
    writeBinFile(os.path.join(cpkRoot, targetFile),repackedArcBytes)

if __name__ == "__main__":
    targetRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\facility\pack"
    )
    targetFile = "cmbroot.arc"
    # unpackBin(os.path.join(targetRoot,targetFile))

    cpkRoot = r"F:\TMP\cpk_output_workplace\datacpk\facility\pack"
    oriArcPath = r"F:\TMP\cpk_output_workplace\ori-data\facility\pack\cmbroot.arc"

    repack()

