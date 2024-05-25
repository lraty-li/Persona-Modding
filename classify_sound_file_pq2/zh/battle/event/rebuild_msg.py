import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import rebuilAllMsg, RecompileType


# def rebuildBMDs():


if __name__ == "__main__":
    rawJson = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg.json"
    )
    zhJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg-parts-zh.json"
    reBuildRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\event"
    )
    reBuildBinRoot = r"F:\TMP\cpk_output_workplace\datacpk\battle\event"
    transedBmds = rebuilAllMsg(rawJson, zhJson, reBuildRoot, RecompileType.Tutorial_Scr_Bf)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bf.flow.bf", ".bf")
        )
        shutil.copy(bmdF, str(targetBmdf))

    rawJson = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg-bgm.json"
    )
    zhJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg-bgm-parts-zh.json"
    reBuildRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\event\bgm"
    )
    reBuildBinRoot = r"F:\TMP\cpk_output_workplace\datacpk\battle\event\bgm"
    transedBmds = rebuilAllMsg(rawJson, zhJson, reBuildRoot, RecompileType.Tutorial_Scr_Bf)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bf.flow.bf", ".bf")
        )
        shutil.copy(bmdF, str(targetBmdf))


    rawJson = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg-support.json"
    )
    zhJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\event\msg-support-parts-zh.json"
    reBuildRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\event\support"
    )
    reBuildBinRoot = r"F:\TMP\cpk_output_workplace\datacpk\battle\event\support"
    transedBmds = rebuilAllMsg(rawJson, zhJson, reBuildRoot, RecompileType.Tutorial_Scr_Bf)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bf.flow.bf", ".bf")
        )
        shutil.copy(bmdF, str(targetBmdf))
