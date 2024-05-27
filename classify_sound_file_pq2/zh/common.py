import json
from pathlib import Path

atlusScriptCompiler = (
    r"F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe"
)

halfWidthToFullWidth = "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\charset\half_width_to_full_width.json"

charsetOutRoot = "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\charset"
charsetVersion = "20240520"
zhcharsetOpPath = Path().joinpath(charsetOutRoot, charsetVersion + "-charSet.txt")
jpCharsetOpPath = Path().joinpath(
    charsetOutRoot, charsetVersion + "-jp-charSet.txt"
)

zhChar2JpKanjiPath = Path().joinpath(charsetOutRoot, charsetVersion + "-zhChar2JpKanji.json")
JpKanji2zhCharPath = Path().joinpath(charsetOutRoot, charsetVersion + "-JpKanji2zhChar.json")

jpXlorPath = Path().joinpath(jpCharsetOpPath.parent, jpCharsetOpPath.stem + ".xlor")

rebuildCPKRoot = r'F:\TMP\cpk_output_workplace\datacpk'


def loadJson(filePath):
    with open(filePath, "r") as file:
        return json.loads(file.read())


def dumpJson(filePath, data):
    with open(
        filePath,
        "w",
    ) as file:
        file.write(json.dumps(data, ensure_ascii=False))

def readBinFile(filePath):
    data = []
    with open(filePath, "rb") as file:
        data = file.read()
    return data


def writeBinFile(filepaht, data):
    with open(filepaht, "wb") as file:
        file.write(bytes(data))

def valueToLittleBytes(value,width = 4):
    # reverd
    # input : 19,088,743
    # output 67 45 23 01
    return value.to_bytes(width, "little")

def getReveBinValue(bBytes):
    # bBytes = list(reversed(bBytes))
    # little-endian
    sum = 0
    for bByteIndex in range(len(bBytes)):
        sum += bBytes[bByteIndex] << (8 * bByteIndex)
    return int(sum)

def fillToBytes(start, container, bBytes):
    if len(bBytes) > len(container):
        raise
    else:
        for bbyte in bBytes:
            container[start] = bbyte
            start += 1
    return container