# data/init/*.bmd
import os

# cmpConfigItem.ctd 游戏设置的文本在这里
# 010 editor 搜索 8f e3 89 ba "上下"

# cmpConfigHelp.ctd 右上角黄色字，解释cmpConfigItem 的选项

# decompile all bmd
atlusScriptCompiler = (
    r"F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"
)
workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init"
files = os.listdir(workplace)
bmdFiles = [i for i in files if i.endswith(".bmd")]

for bmdFile in bmdFiles:
    command = [
        atlusScriptCompiler,
        os.path.join(workplace, bmdFile),
        "--Decompile -Library pq2 -Encoding SJ",
    ]
    os.system(" ".join(command))
