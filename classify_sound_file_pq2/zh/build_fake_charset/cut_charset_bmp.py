# -*- coding: UTF-8 -*-
import os
from PIL import Image
from PIL import ImageOps
from pathlib import Path


def cutImage(
    filePath,
    outputFolder,
    charWidth,
    charHeight,
):
    img = Image.open(filePath)

    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)

    print(img.size)
    columns = img.width / charWidth
    rows = img.height / charHeight

    counter = 0
    for row in range(int(rows)):
        for column in range(int(columns)):
            # print(row, column)
            LeftTopX = charWidth * column
            LeftTopY = charHeight * row
            # RightBotX = (GLYPH_SIZE-1)*(column+1)
            # RightBotY = (GLYPH_SIZE-1)*(row+1)
            cropped = img.crop(
                (LeftTopX, LeftTopY, LeftTopX + charWidth, LeftTopY + charHeight)
            )  # (left, upper, right, lower)

            cropped.save(os.path.join(outputFolder, "{}.bmp".format(counter)))
            counter += 1


if __name__ == "__main__":
    outPutRoot = (
        r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\build_fake_charset\cropped"
    )
    seurapro12Bmp = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data-extract\font\seurapro_12_12.bmp"
    seurapro13Bmp = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data-extract\font\seurapro_13_13.bmp"
    targets = [seurapro12Bmp, seurapro13Bmp]
    targetOutputs = [
        os.path.join(outPutRoot, Path(seurapro12Bmp).stem),
        os.path.join(outPutRoot, Path(seurapro13Bmp).stem),
    ]
    charSize = [(17, 20), (18, 21)]

    for index in range(len(targets)):
        cutImage(
            targets[index], targetOutputs[index], charSize[index][0], charSize[index][1]
        )

print('DONE')