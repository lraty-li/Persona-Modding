#!/usr/bin/python3
deCompilerPath = "F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"

import os,json
eventRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data\event"

# TODO 多线程
bfFiles = {}
for root, dirs, files in os.walk(eventRoot, topdown=False):
    for name in files:
        if name.endswith(".bf"):
            if(root not in bfFiles.keys()):
                bfFiles[root] = [name]
            bfFiles[root].append(name)
            os.system(deCompilerPath + " " + os.path.join(root, name).replace("\\", "/")+ " " + "-Decompile -Library pq2 -Encoding SJ")
            #print(os.path.join(root, name))


print(len(bfFiles))