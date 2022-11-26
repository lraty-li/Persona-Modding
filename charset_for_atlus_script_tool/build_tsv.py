# -*- coding: utf-8 -*-
# re fill the xlxs simplify Chinese charset to a current charset tsv

from common import loadJson

def buildTsv(charSum, comparisonTable, outputName, offset = 0x20):
  TableWidth = 0x0F
  Mask_Lowest_byte = 0x000F
  ASCII_RANGE = 0x7F
  EMPTY_PLACEHOLDER = "*"
  # charSum = 16 * 471 # how many characters in FONT0.png
  numberingToCharKeys = comparisonTable.keys()
  with open(outputName, 'w', encoding='utf-8') as file:

      #TODO shit handle
      # offset because image export from FONT0.fnt dont have \u0000	\u0001	~	\u001e	\u001f
      for i in range(offset):
        file.write("{}".format(EMPTY_PLACEHOLDER))
        if(i & Mask_Lowest_byte == TableWidth):
            file.write("\n")
        else:
            file.write("\t")

      line = ""
      for counter in range(charSum):
          fillerChar = EMPTY_PLACEHOLDER
          imgName = "{}.png".format(counter)
          if imgName in numberingToCharKeys:
              fillerChar = comparisonTable[imgName]
          line += "{}\t".format(fillerChar)

          if(counter & Mask_Lowest_byte == TableWidth):
              line = line[:-1] # remove last \t
              line += "\n"
              file.write(line)
              line = ""


if __name__ == "__main__":
    charSum = 16 * 471 # how many characters in FONT0.png
    font = "dfyuanlightbold.ttf"
    fontName = font[:-4]
    tablePath_chi = "cache/gameChar_Numbering2Char_{}.json".format(fontName)
    buildTsv(charSum, loadJson(tablePath_chi), "tsv_{}.tsv".format(fontName))
