import os, json

zhRoot = r"f:\modding\p5r\BATTLE\TABLE\NAME"
jpRoot = r"f:\modding\p5r\JP_CPK\BATTLE\TABLE\NAME"


def dumpJson(filePath, data):
    with open(
        filePath,
        "w",
    ) as file:
        file.write(json.dumps(data, ensure_ascii=False))


cmpMap = {}
files = os.listdir(jpRoot)
for fileName in files:
    skillJp = os.path.join(jpRoot, fileName)
    with open(skillJp, "r") as file:
        jpSkills = file.read().splitlines()

    skillZh = os.path.join(zhRoot, fileName)
    with open(skillZh, "r") as file:
        zhSkills = file.read().splitlines()

    assert len(jpSkills) == len(zhSkills)

    for index in range(len(jpSkills)):
        # 重复？
        cmpMap[jpSkills[index]] = zhSkills[index]

dumpJson("cmpMap.json", cmpMap)
print()
