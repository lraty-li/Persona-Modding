#!/usr/bin/python3
deCompilerPath = "F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"

import os,json

# TODO 多线程
bfFiles = {}
for root, dirs, files in os.walk("cache/event-zh", topdown=False):
    for name in files:
        if name.endswith(".bf"):
            if(root not in bfFiles.keys()):
                bfFiles[root] = [name]
            bfFiles[root].append(name)
            os.system(deCompilerPath + " " + os.path.join(root, name).replace("\\", "/")+ " " + "-Decompile -Library p3p -Encoding p3p_ns_sc")
            #print(os.path.join(root, name))

with open("bfFiles-zh.json",'w+') as file:
    file.write(json.dumps(bfFiles))
print(len(bfFiles))