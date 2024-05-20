import json
from pathlib import Path

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