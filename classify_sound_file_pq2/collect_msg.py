import os,json,shutil

#!/usr/bin/python3
deCompilerPath = "F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"

eventRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data\event"
outPutRoot = "./cache/all_msg"

# TODO 多线程
bfFiles = {}
for root, dirs, files in os.walk(eventRoot, topdown=False):
    for name in files:
        if name.endswith(".msg"):
            shutil.copy(os.path.join(root, name),os.path.join(outPutRoot, name))
