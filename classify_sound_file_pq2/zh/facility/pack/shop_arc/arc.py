import sys, os
from pathlib import Path


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import (
    writeBinFile,
)
from arc_common import getArcFileNames, rebuildArcBytes
# from zh_common import repackBin


if __name__ == "__main__":
    targetRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\facility\pack"
    )
    targetFile = "shop.arc"
    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\pack")
    # unpackBin(os.path.join(targetRoot,targetFile))

    cpkRoot = r"F:\TMP\cpk_output_workplace\datacpk\facility\pack"
    # repackBin(
    #     os.path.join(targetRoot, targetFile.replace(".", "_")),
    #     os.path.join(cpkRoot, targetFile),
    # )
    arcUnpackedPath = os.path.join(targetRoot, targetFile.replace(".", "_"))

    oriArcPath = r"F:\TMP\cpk_output_workplace\ori-data\facility\pack\shop.arc"
    repackTargets = getArcFileNames(oriArcPath)
    repackedArcBytes = rebuildArcBytes(
        arcUnpackedPath,
        repackTargets,
    )
    writeBinFile(os.path.join(cpkRoot, targetFile),repackedArcBytes)
