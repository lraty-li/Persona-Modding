import os, shutil, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import rebuilAllMsg, RecompileType

def rebuilBf():
    failTargets = []
    workplaceRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility"
    os.chdir(workplaceRoot)
    rawJson = "msg.json"
    zhJson = "msg-parts-zh.json"
    # 被移动到cache了
    reBuildRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\facility_cache"
    reBuildBinRoot = r"F:\TMP\cpk_output_workplace\datacpk\facility"
    transedBmds = rebuilAllMsg(
        rawJson, zhJson, reBuildRoot, RecompileType.Tutorial_Scr_Bf
    )
    for bmdF in transedBmds:
        targetBmdf = Path().joinpath(
            reBuildBinRoot, Path(bmdF).name.replace(".bf.flow.bf", ".bf")
        )
        try:
            shutil.copy(bmdF, str(targetBmdf))
        except FileNotFoundError:
            failTargets.append(Path(bmdF).name)
    
    # ['noffice.bf.flow.bf', 'scrgotodungeon.bf.flow.bf', 'townsupport.bf.flow.bf', 'weapon.bf.flow.bf']
    print("failTargets")
    print(failTargets)


if __name__ == "__main__":
    rebuilBf()