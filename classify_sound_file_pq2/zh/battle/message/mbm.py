from pathlib import Path
import sys


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import dumpJson
from mbm_common import decodeAllMbm,flattenTheMap


if __name__ == "__main__":
    # >>> [i for i in os.listdir('.') if i.endswith('.mbm')]
    targets = [
        "battlemessage.mbm",
        "skillburstexp.mbm",
        "skillcustom.mbm",
        "skillexpbattle.mbm",
        "skillexpbattle_enemy.mbm",
        "skillexpbattle_player.mbm",
    ]
    cacheRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\battle\message"
    )

    targets = [Path().joinpath(cacheRoot, i) for i in targets]
    msgMap = decodeAllMbm(targets)
    flattenMsgMap = flattenTheMap(msgMap)
    outputJpJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\battle\message\mbm.json"
    dumpJson(outputJpJson, msgMap)
    outputJpJsonP = Path(outputJpJson)
    dumpJson(Path().joinpath(outputJpJsonP.parent, outputJpJsonP.stem + '-parts.json'), flattenMsgMap)
    print()
