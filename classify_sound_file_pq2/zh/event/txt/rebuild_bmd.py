import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import rebuilAllMsg, RecompileType

# def rebuildBMDs():


if __name__ == "__main__":
    rawJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt\bmd.json"
    zhJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt\bmd-parts-zh.json"
    reBuildRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\event\txt_cache"
    reBuildBinRoot = (
        r"F:\TMP\cpk_output_workplace\datacpk\event\txt"
    )
    transedBmds = rebuilAllMsg(rawJson, zhJson, reBuildRoot, RecompileType.BMD)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bmd.msg.bmd", ".bmd")
        )
        shutil.copy(bmdF, targetBmdf)
    # rebuildBin()