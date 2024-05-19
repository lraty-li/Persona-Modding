import os

import sys
sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import dumpJson,loadJson

os.chdir("D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin")

zhFiles = os.listdir("zh")
msgMap = {}
for zhFile in zhFiles:
    msgMap[zhFile] = []
    with open(
        os.path.join(
            "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin",
            "zh",
            zhFile,
        ),
        "r",
    ) as file:

        lines = file.read().splitlines()
        for lin in lines:
            msgMap[zhFile].append(lin)

#validate
data = loadJson("D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\ctd.json")
for key in data:
    if(not len(data[key]) == len(msgMap[key])):
        print(key)

dumpJson(
    "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\ctd-zh.json",
    msgMap,
)