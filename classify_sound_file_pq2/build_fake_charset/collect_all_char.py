import os, json
from pathlib import Path
import unicodedata

# os.chdir("build_fake_font")

charset2xllt = r"f:\modding\persona-tools\3dsfont\charset2xllt.exe"
charset2xlor = r"f:\modding\persona-tools\3dsfont\charset2xlor.exe"
translatedMsg = {}
chars = {"zh": {}, "else": {}}
zhChar2JpKanji = {}
JpKanji2zhChar = {}


def isZhChar(char):
    if "\u4e00" <= char <= "\u9fff":
        return True
    else:
        return False


def isJpKanjiChar(char):
    # [(\x3400-\x4DB5\x4E00-\x9FCB\xF900-\xFA6A]
    kanjiRange = [["\u3400", "\u4DB5"], ["\u4E00", "\u9FCB"], ["\uF900", "\uFA6A"]]
    for kjRange in kanjiRange:
        if kjRange[0] <= char <= kjRange[1]:
            return True
    return False


def buildCompaTable(jpCharSetFilePath):
    global chars
    zhChars = list(chars["zh"])
    # TODO 如何处理 else 类别的字符，理论上原本字符集应该包含了所有事件文本的字符
    BYPASS_LINE_NUM = 48
    newCharSet = []
    fakeCharSet = []
    replacedLines = []
    rawLines = []
    zhCharIndex = 0
    zhCharsCount = len(zhChars)
    lineCounter = 1
    global zhChar2JpKanji, JpKanji2zhChar
    with open(jpCharSetFilePath, "r", encoding="utf-16le") as file:
        rawLines = file.readlines()
    for lineIndex in range(len(rawLines)):
        line = rawLines[lineIndex]
        if line[-1] == "\n":
            line = line[:-1]
            rawLines[lineIndex] = line
        if zhCharIndex >= zhCharsCount:
            break
        lineCounter += 1
        if lineCounter <= BYPASS_LINE_NUM:
            # 跳过前面部分
            continue

        replacedLine = ""
        for jpCharIndex in range(len(line)):
            jpChar = line[jpCharIndex]
            replacedChar = jpChar
            if zhCharIndex >= zhCharsCount:
                break
            if isJpKanjiChar(jpChar):
                zhChar = zhChars[zhCharIndex]
                zhChar2JpKanji[zhChar] = jpChar
                JpKanji2zhChar[jpChar] = zhChar
                replacedChar = zhChar
                zhCharIndex += 1
            replacedLine += replacedChar
        replacedLines.append(replacedLine)
    replacedLines = rawLines[: BYPASS_LINE_NUM - 1] + replacedLines
    fakeCharSet = rawLines[: lineCounter - 1]
    if zhCharIndex < zhCharsCount:
        print("More zh char than jp kanji")
        raise Exception("No implement")
    else:
        print("More jp kanji than zh char")
        # TODO 填充剩下的，免得重复？
        # 剩下的也填充进去，之后游戏是按照原本的xllt xlor 索引的，所以不会重复，
        # 但其实不管也没所谓，应该没地方会索引到哪些日文汉字？
        # p的招式名称等汉化就得看了
        newCharSet = replacedLines

    # check
    otherChars = chars["else"]
    bypassedJpChars = "".join(rawLines[: BYPASS_LINE_NUM - 1])
    for char in otherChars:
        if not char in bypassedJpChars:
            print("{} is not in bypassedJpChars".format(char))
    # (qiē cuō zhuó mó) 这种注音不管了
    return newCharSet, fakeCharSet


def collectChar(msgLine):
    global chars
    # collect char
    for char in msgLine:
        charType = "else"
        if isZhChar(char):
            charType = "zh"
        if char in chars.keys():
            chars[charType][char] += 1
            pass
        else:
            chars[charType][char] = 1


def collectMsg(eventIndex, zhMsg):
    # collect msg
    global translatedMsg
    if eventIndex in translatedMsg.keys():
        if type(translatedMsg[eventIndex]) == list:
            translatedMsg[eventIndex].append(zhMsg)
        elif type(translatedMsg[eventIndex]) == str:
            translatedMsg[eventIndex] = [translatedMsg[eventIndex], zhMsg]
    else:
        translatedMsg[eventIndex] = zhMsg


def dumpJson(filePath, data):
    with open(
        filePath,
        "w",
    ) as file:
        file.write(json.dumps(data, ensure_ascii=False))


def addHalfFullWidth(halfWidthToFullWidthPath):
    # 把半角符号转为全角符号，避开留给游戏的区域
    # bypassed chars
    """
    !"#$%&'()*+,-./
    0123456789:;<=>?
    @ABCDEFGHIJKLMNO
    PQRSTUVWXYZ[\]^_
    `abcdefghijklmno
    pqrstuvwxyz{|}~｡
    ｢｣､･ｦｧｨｩｪｫｬｭｮｯｰｱ
    ｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁ
    ﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑ
    ﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝﾞﾟ　、
    """
    # TMD 什么参数，什么乱用全局，屎山啊
    global zhChar2JpKanji, JpKanji2zhChar
    halfWidthToFullWidth = {}
    with open(halfWidthToFullWidthPath, "r") as file:
        halfWidthToFullWidth = json.loads(file.read())
    for half in halfWidthToFullWidth:
        full = halfWidthToFullWidth[half]
        zhChar2JpKanji[half] = full
        JpKanji2zhChar[full] = half


if __name__ == "__main__":
    translatedFile = (
        "build_fake_charset/pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427.txt"
    )
    jpCharsetPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data-extract\font\seurapro_13_13.txt"
    halfWidthToFullWidth = "build_fake_charset/half_width_to_full_width.json"
    with open(translatedFile, "r") as file:
        while file.readable():
            line = file.readline()
            if len(line) <= 0:
                break
            if line[-1] == "\n":
                line = line[:-1]
            if line.startswith("=========="):
                continue
            elif line.startswith("e"):
                parts = line.split(" | ")
                eventIndex = parts[0]
                zhMsg = parts[2]
                collectChar(zhMsg)
                collectMsg(eventIndex, zhMsg)

    fakeZhCharset, fakeJpCharset = buildCompaTable(jpCharsetPath)
    transFileNoExte = Path(translatedFile).stem
    transFileFolder = Path(translatedFile).parent

    addHalfFullWidth(halfWidthToFullWidth)

    # dump data
    subFixs = ["-maped", "-JpKanji2zhChar", "-zhChar2JpKanji"]
    targets = [translatedMsg, JpKanji2zhChar, zhChar2JpKanji]
    for index in range(len(subFixs)):
        replaceTo = subFixs[index]
        data = targets[index]
        replaceToExtension = "{}.json".format(replaceTo)
        dumpJson(
            os.path.join(transFileFolder, transFileNoExte + replaceToExtension),
            data,
        )
    # dump charset
    zhcharsetOpPath = os.path.join(transFileFolder, transFileNoExte + "-charSet.txt")
    with open(
        zhcharsetOpPath,
        "w",
        encoding="utf-16le",
    ) as file:
        for line in fakeZhCharset:
            file.write(line + "\n")
    jpCharsetSubFix = "-jp-charSet"
    jpCharsetOpPath = os.path.join(
        transFileFolder, transFileNoExte + jpCharsetSubFix + ".txt"
    )
    with open(
        jpCharsetOpPath,
        "w",
        encoding="utf-16le",
    ) as file:
        for line in fakeJpCharset:
            file.write(line + "\n")

    # build fake xllt xlor
    # os.system(
    #     "{} {} {}".format(
    #         charset2xllt,
    #         jpCharsetOpPath,
    #         os.path.join(transFileFolder, transFileNoExte + jpCharsetSubFix + ".xllt"),
    #     )
    # )
    os.system(
        "{} {} {}".format(
            charset2xlor,
            jpCharsetOpPath,
            os.path.join(transFileFolder, transFileNoExte + jpCharsetSubFix + ".xlor"),
        )
    )
    print("DONE")
