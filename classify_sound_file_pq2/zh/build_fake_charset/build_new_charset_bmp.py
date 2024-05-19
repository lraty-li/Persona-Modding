# -*- coding: UTF-8 -*-
import os, json
from PIL import Image
from PIL import ImageOps
from pathlib import Path

# -*- coding: UTF-8 -*-
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import shutil

CHARS_PER_LINE = 16


def get_char_list_from_ttf(font_file):
    "给定font_file,获取它的中文字符"
    f_obj = TTFont(font_file)
    m_dict = f_obj.getBestCmap()

    unicode_list = []
    for key, _ in m_dict.items():
        unicode_list.append(key)

    char_list = []
    for ch_unicode in unicode_list:
        # https://unicode-table.com/cn/blocks/private-use-area/
        # filter out \uE000—\uF8FF
        # charUniCode = hex(ch_unicode)
        if 0xE000 <= ch_unicode and ch_unicode <= 0xF8FF:
            continue
        char_list.append(chr(ch_unicode))

    # filter out control charater for dfyuanlightbold
    # char_list = char_list[32:126] + char_list[127:-1]

    return char_list


def drawChar(char, font, charImgWidth, charImgHeight, drawOffsetX, drawOffsetY):
    image = Image.new(mode="RGB", size=(charImgWidth, charImgHeight), color="#FFFFFFFF")
    drawTable = ImageDraw.Draw(im=image)
    drawTable.text(
        xy=(drawOffsetX, drawOffsetY), text=char, fill="#00000000", font=font
    )
    return image


def getChatImgSize(font):
    """
    seurapro_13_13 :
    宽18 长21 共246行
    ResourceHanRoundedCN-Medium 字号13px 生成： 宽18 长23

    seurapro_12_12 :
    宽17 长20 共246行
    ResourceHanRoundedCN-Medium 字号12px 生成： 宽17 长22
    """
    testChar = "我"
    fontSize = font.size
    x1, y1, x2, y2 = font.getbbox(testChar)
    #TODO should draw margin/border, help debug when building bcfnt
    marginX = 5  # 17-12, 18-13
    marginY = 8  # 20 - 12, 21-13
    # marginY = 10  # 20 - 12, 21-13
    charImgWidth = fontSize + marginX
    charImgHeight = fontSize + marginY
    drawOffsetX = abs(marginX / 2 - x1)
    drawOffsetY = abs(marginY / 2 - y1)
    return charImgWidth, charImgHeight, drawOffsetX, drawOffsetY - 1
    # return charImgWidth, charImgHeight, drawOffsetX + 1, drawOffsetY + 1


def getCorpedIndex(row, column):
    return row * CHARS_PER_LINE + column


def buildImage(chatset, fontName, charImgRoot, charSize, fontPath):
    font = ImageFont.truetype(fontPath, charSize)
    charImgWidth, charImgHeight, drawOffsetX, drawOffsetY = getChatImgSize(font)
    image = Image.new(
        mode="RGB",
        size=(CHARS_PER_LINE * charImgWidth, len(charset) * charImgHeight),
        color="#FFFFFFFF",
    )
    # 原版的 "pq2_seurapro_13_13 比 pq2_seurapro_12_12 在12行多了一个∥，之后全部往后推"
    # 所以把bypass前推到11，不然因为原版字符图片的错位，新生成的字符图片会有错位，例如索引片假的时候。    
    BYPASS_LINE_NUM = 9
    lineIndex = 0
    for lineIndex in range(len(charset)):
        line = charset[lineIndex]

        charIndex = 0
        for charIndex in range(len(line)):
            charImg = None
            if lineIndex <= BYPASS_LINE_NUM:
                # 从文件夹取图片
                imgIndex = getCorpedIndex(lineIndex, charIndex)
                charImg = Image.open(
                    os.path.join(charImgRoot, "{}.bmp".format(imgIndex))
                )
            else:
                # 生成图片
                char = line[charIndex]
                charImg = drawChar(
                    char, font, charImgWidth, charImgHeight, drawOffsetX, drawOffsetY
                )
            image.paste(charImg, (charIndex * charImgWidth, lineIndex * charImgHeight))
            # image.show()
    charImgPathLib = Path(charImgRoot)
    charsetImgOutputPath = os.path.join(
        charImgPathLib.parent, "{}.bmp".format(charImgPathLib.stem)
    )
    image.save(charsetImgOutputPath)


if __name__ == "__main__":

    charSetPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\build_fake_charset\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-charSet.txt"
    fontPath = r"cache/RHR-CN-0.990/ResourceHanRoundedCN-Medium.ttf"
    charset = []
    with open(charSetPath, "r", encoding="utf-16le") as file:
        line = file.readline()
        while len(line) > 0:
            charset.append(line[:-1])  # remove \n
            line = file.readline()

    outPutRoot = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\build_fake_charset\cropped"

    targets = [
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data-extract\font\seurapro_12_12.bmp",
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data-extract\font\seurapro_13_13.bmp",
    ]
    charSize = [12, 13]
    # charImgSize = [(17, 20), (18, 21)]

    fontName = [Path(i).stem for i in targets]
    targetOutputs = [os.path.join(outPutRoot, i) for i in fontName]

    for index in range(len(targets)):
        buildImage(
            charset, fontName[index], targetOutputs[index], charSize[index], fontPath
        )

print("DONE")
