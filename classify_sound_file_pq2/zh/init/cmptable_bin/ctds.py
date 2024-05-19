# cmpConfigItem.ctd 游戏设置的文本在这里
# 010 editor 搜索 8f e3 89 ba "上下"

# cmpConfigHelp.ctd 右上角黄色字，解释cmpConfigItem 的选项
import os,shutil

import sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import dumpJson,unpackBin

sys.path.append(
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin"
)
from ctd_commom import targets, BLOCK_SIZE, HEADER_SIZE


workplace = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\cmptable_bin"

# [i for i in os.listdir('.') if i.endswith('ctd')]


os.chdir("D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin")


def parseCtd(filePath):
    msgs = []
    with open(filePath, "rb") as file:
        header = file.read(HEADER_SIZE)
        content = file.read(BLOCK_SIZE)
        while len(content) == BLOCK_SIZE:
            msgLine = ""
            byteIndex = 0
            while byteIndex < BLOCK_SIZE:
                byte1 = content[byteIndex]
                byte2 = content[byteIndex + 1]
                if byte1 == 0 and byte2 == 0:
                    break
                if byte1 <= 0x7F and byte2 > 0x7F:
                    # byte1 ASCII, byte2 is high byte of shifjis
                    char = bytes([byte1]).decode("shiftjis")
                    msgLine += char
                    byte3 = content[byteIndex + 2]
                    char = bytes([byte2, byte3]).decode("shiftjis")
                    msgLine += char
                    byteIndex += 3
                    continue
                if byte1 <= 0x7F and byte2 == 0x00:
                    # byte1 ASCII, byte2 ends
                    # TODO merge the byte1 <= 0x7F logic
                    char = bytes([byte1]).decode("shiftjis")
                    msgLine += char
                    byteIndex += 1
                    continue

                char = content[byteIndex : byteIndex + 2].decode("shiftjis")
                msgLine += char
                byteIndex += 2
            msgs.append(msgLine)
            content = file.read(64)
        return msgs


if __name__ == "__main__":
    msgMap = {}
    for target in targets:
        # if target == "cmpDifficultItem.ctd":
        #     print()
        msgs = []
        # 复制原版的.bin文件到cache，免得读取到已经替换文字后的文件
        originalBin = r'F:\TMP\cpk_output_workplace\ori-data\init\cmptable.bin'
        cacheBin = r'D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\cmptable.bin'
        shutil.copy(originalBin, cacheBin)
        unpackBin(cacheBin)
        ctdLines = parseCtd(os.path.join(workplace, target))
        for lineIndex in range(len(ctdLines)):
            msgMap["{}_{}".format(target, lineIndex)] = ctdLines[lineIndex]

    dumpJson("ctd.json", msgMap)
    print("DONE")
