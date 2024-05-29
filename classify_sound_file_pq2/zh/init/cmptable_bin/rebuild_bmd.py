import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import rebuilAllMsg, RecompileType




def somthing():
    rebuilAllMsg()
    failTargets = []

    try:
        shutil.copy(
            outPutBFname,
            os.path.join(reBuildCPKroot, eventFolder, msgFile.replace(".msg", "")),
        )
        pass
    except FileNotFoundError as e:
        # recompile fail
        # TODO just bypass now
        # but the way to insert zh msg into bf file need still
        failTargets.append(msgFile)

    print("fails to recompile:")
    print(failTargets)


def rebuildBMDs():


    rawJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\bmd.json"
    zhJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\bmd-parts-zh.json"
    reBuildRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\cmptable_bin_cache"
    reBuildBinRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\cmptable_bin"
    )
    transedBmds = rebuilAllMsg(rawJson, zhJson, reBuildRoot, RecompileType.BMD)
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bmd.msg.bmd", ".bmd")
        )
        shutil.copy(bmdF, targetBmdf)
    # rebuildBin()
if __name__ == "__main__":
    rebuildBMDs()