import os, json, sys
from pathlib import Path
import unicodedata


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import *

charset2xllt = r"f:\modding\persona-tools\3dsfont\charset2xllt.exe"
charset2xlor = r"f:\modding\persona-tools\3dsfont\charset2xlor.exe"
translatedEventMsg = {}
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
    jpCharsKeepd = []
    zhChars = list(chars["zh"])
    # TODO 如何处理 else 类别的字符，理论上原本字符集应该包含了所有事件文本的字符
    # 原版的 "pq2_seurapro_13_13 比 pq2_seurapro_12_12 在12行多了一个∥，之后全部往后推"
    # 所以把bypass前推到11，不然因为原版字符图片的错位，新生成的字符图片会有错位，例如索引片假的时候。
    # 仝 是汉字，但放得很前，不知道啥原因，但按范围来说是日文汉字，会被替换 看看会不会有bug吧
    BYPASS_LINE_NUM = 11
    newCharSet = []
    fakeCharSet = []
    replacedLines = []
    rawLines = []
    zhCharIndex = 0
    zhCharsCount = len(zhChars)
    lineCounter = 1
    global zhChar2JpKanji, JpKanji2zhChar
    with open(jpCharSetFilePath, "r", encoding="utf-16le") as file:
        rawLines = file.read().splitlines()
    for lineIndex in range(len(rawLines)):
        jpLine = rawLines[lineIndex]
        if zhCharIndex >= zhCharsCount:
            break
        lineCounter += 1
        if lineCounter <= BYPASS_LINE_NUM:
            # 跳过前面部分
            continue

        replacedLine = ""
        for jpCharIndex in range(len(jpLine)):
            # 从原版字符集，逐个字符读取，如果是日文汉字，就替换成中文字符
            jpChar = jpLine[jpCharIndex]
            replacedChar = jpChar
            if zhCharIndex >= zhCharsCount:
                break
            if(jpChar == 'ガ'):
                print()
            if isJpKanjiChar(jpChar):
                zhChar = zhChars[zhCharIndex]
                zhChar2JpKanji[zhChar] = jpChar
                JpKanji2zhChar[jpChar] = zhChar
                replacedChar = zhChar
                zhCharIndex += 1
            else:
                # 非日文汉字，保留编码
                zhChar2JpKanji[jpChar] = jpChar
                JpKanji2zhChar[jpChar] = jpChar
                replacedChar = jpChar
                print("keep {}".format(jpChar))
                jpCharsKeepd.append(jpChar)
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
    joinedNewCharset = "".join(newCharSet)
    for char in otherChars:
        if not (char in joinedNewCharset or char in bypassedJpChars):
            print("not encoded char: {} ".format(char))
    # (qiē cuō zhuó mó) 这种注音不管了
    print('these jp chars was keeped in comparatable')
    print(jpCharsKeepd)
    return newCharSet, fakeCharSet


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
        #TODO BUG check if in shiftjis
        full = halfWidthToFullWidth[half]
        zhChar2JpKanji[half] = full
        JpKanji2zhChar[full] = half


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


def collectAllJsonTransFile(targets):

    for targ in targets:
        contenet = loadJson(targ)
        for mKey in contenet:
            line = contenet[mKey]
            for char in line:
                collectChar(char)


def writeCharsetData(outputPath, data):
    with open(
        outputPath,
        "w",
        encoding="utf-16le",
    ) as file:
        for line in data:
            file.write(line + "\n")


if __name__ == "__main__":
    targets = [
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-maped.json",
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\txt\bmd-parts-zh.json",
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\bmd-parts-zh.json",
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\cmptable_bin\ctd-zh.json",
    ]
    collectAllJsonTransFile(targets)

    addHalfFullWidth(halfWidthToFullWidth)

    originalJpCharsetPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data-extract\font\seurapro_13_13.txt"
    fakeZhCharset, fakeJpCharset = buildCompaTable(originalJpCharsetPath)


    # dump charset

    # dump data
    targets = [JpKanji2zhChar, zhChar2JpKanji]
    outputPaths = [JpKanji2zhCharPath, zhChar2JpKanjiPath]
    for index in range(len(targets)):
        outputPath = outputPaths[index]
        data = targets[index]
        dumpJson(
            str(outputPath),
            data,
        )

    writeCharsetData(str(zhcharsetOpPath), fakeZhCharset)
    writeCharsetData(str(jpCharsetOpPath), fakeJpCharset)

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
            str(jpXlorPath),
        )
    )
    print("DONE")
