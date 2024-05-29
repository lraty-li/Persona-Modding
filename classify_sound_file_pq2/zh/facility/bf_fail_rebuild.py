from pathlib import Path
import re, sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import rebuildFailBf
from common import writeBinFile



# test
def testRebuild():
    # targe = "e808_060.bf"
    # msgFileName = targe.replace(".bf", ".bf.msg")
    # cacheRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\event_test"
    # bmdFilePath = recompileMsg(msgFileName, cacheRoot, RecompileType.BMD)

    targ = "e000_015.bf"
    oriRoot = r"F:\TMP\cpk_output_workplace\ori-data\event\e000"
    cacheRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\event\e000"
    rebuildBytes = rebuildFailBf(targ, oriRoot, cacheRoot) 
    writeBinFile("{}_test_rebuild_unknow_func.bf".format(targ), rebuildBytes)
    return

def rebuilBf():
    targets = [
        "noffice.bf.flow.bf",
        "scrgotodungeon.bf.flow.bf",
        "townsupport.bf.flow.bf",
        "weapon.bf.flow.bf",
    ]
    targets = [i.replace(".bf.flow.bf", ".bf") for i in targets]

    oriRoot = r"F:\TMP\cpk_output_workplace\ori-data\facility"
    cacheRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\facility_cache"
    )
    repackRoot = r"F:\TMP\cpk_output_workplace\datacpk\facility"
    rawJsonPath = r'D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\facility\msg.json'
    for targ in targets:
        rebuildBytes = rebuildFailBf(targ, oriRoot, cacheRoot, rawJsonPath)
        # writeBinFile(str(Path().joinpath(repackRoot, targ)), rebuildBytes)

if __name__ == "__main__":
    rebuilBf()