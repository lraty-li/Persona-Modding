import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import rebuilAllMsg, RecompileType


# def rebuildBMDs():


if __name__ == "__main__":
    rawJson = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\tutorial\scr\msg.json"
    )
    zhJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\tutorial\scr\msg-parts-zh.json"
    reBuildRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\tutorial\scr"
    )
    reBuildBinRoot = r"F:\TMP\cpk_output_workplace\datacpk\tutorial\scr"
    transedBmds = rebuilAllMsg(rawJson, zhJson, reBuildRoot, RecompileType.Tutorial_Scr_Bf)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bf.flow.bf", ".bf")
        )
        shutil.copy(bmdF, str(targetBmdf))
