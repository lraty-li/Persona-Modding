import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import rebuilAllMsg, RecompileType


def rebuildBMDs():
    workplaceRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\support\message"
    )
    rawJson = os.path.join(workplaceRoot, "bmd.json")
    zhJson = os.path.join(workplaceRoot, "bmd-parts-zh.json")
    workplacePath = Path(workplaceRoot)
    #TODO make commom
    cacheRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache"
    cacheFolder = Path().joinpath(
        cacheRoot, "battle", "support", workplacePath.stem + "_cache"
    )
    reBuildBinRoot = r"F:\TMP\cpk_output_workplace\datacpk\battle\support\message"
    transedBmds = rebuilAllMsg(rawJson, zhJson, cacheFolder, RecompileType.BMD)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bmd.msg.bmd", ".bmd")
        )
        shutil.copy(bmdF, targetBmdf)


if __name__ == "__main__":
    rebuildBMDs()
