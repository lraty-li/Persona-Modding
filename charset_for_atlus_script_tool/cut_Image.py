# -*- coding: UTF-8 -*-
import os
from PIL import Image
from PIL import ImageOps


def cutImage(filePath, outputFolder, GLYPH_SIZE = 96, binarization = False, colorInversion = False):
  img = Image.open(filePath)
  binarize_threshold = 127

  if(not os.path.exists(outputFolder)):
      os.mkdir(outputFolder)

  print(img.size)
  columns = img.width/GLYPH_SIZE
  rows = img.height/GLYPH_SIZE

  counter = 0
  for row in range(int(rows)):
      for column in range(int(columns)):
          print(row,column)
          LeftTopX = GLYPH_SIZE*column
          GLYPH_SIZE*column - column + GLYPH_SIZE - 1
          LeftTopY = GLYPH_SIZE*row
          # RightBotX = (GLYPH_SIZE-1)*(column+1)
          # RightBotY = (GLYPH_SIZE-1)*(row+1)
          cropped = img.crop((LeftTopX, LeftTopY, LeftTopX+GLYPH_SIZE, LeftTopY+GLYPH_SIZE))  # (left, upper, right, lower)

          #反转
          if (colorInversion):
            cropped = ImageOps.invert(cropped)
          # 二值化
          # Threshold
          if (binarization):
            cropped = cropped.point( lambda p: 255 if p > binarize_threshold else 0 )
            cropped = cropped.convert('1')
          cropped.save(os.path.join(outputFolder,"{}.png".format(counter)))
          counter += 1

if __name__ == "__main__":
  FONT0 = 'FONT0.PNG'
  GLYPH_SIZE = 96
  croppedOutputFolder = "cropped"

  cutImage(FONT0, croppedOutputFolder)
