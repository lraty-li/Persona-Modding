# -*- coding: UTF-8 -*-
import os
from common import loadJson

# https://github.com/tge-was-taken/Atlus-Script-Tools/tree/master/Source/AtlusScriptLibrary/Common/Text/Encodings

# Offset from start of glyph range to start of the char table.
CHAR_TO_GLYPH_INDEX_OFFSET = 0x60

# Size of a single glyph table.
GLYPH_TABLE_SIZE = 0x80

# The range 0-based range of an ascii character index.
ASCII_RANGE = 0x7F

# The high bit serves as a marker for a table index.
GLYPH_TABLE_INDEX_MARKER = 0x80

class CodePoint:
		def __init__(self, high, low ):
			self.highSurrogate = high
			self.lowSurrogate = low

def genCharSurrogates(numberingToChar, outputName, offset = 0x20):
  mCharToCodePoint = {}
  # translate chinese to Surrogates pairs only 
  # add extended characters, but don't re-include the ascii range

  # here -> origin code of atlus script tool
  # numbering -> charIndex
  # hex(ord(numberingToChar[numbering])) -> charTable[charIndex]	('我' -> \u6211 -> 6211)
  for numbering in numberingToChar:
    charIndex = int(numbering[0:-4]) # no ".png"
    # DEBUG BEGIN
    # 按 0x8681
    # charIndex = 1032
    charIndex_offseted = charIndex + offset
    glyphIndex = charIndex_offseted + CHAR_TO_GLYPH_INDEX_OFFSET
    # glyphIndex = charIndex + CHAR_TO_GLYPH_INDEX_OFFSET
    #DEBUG END
    tableIndex = int((glyphIndex / GLYPH_TABLE_SIZE) - 1)
    tableRelativeIndex = glyphIndex - (tableIndex * GLYPH_TABLE_SIZE)

    if (not numberingToChar[numbering] in mCharToCodePoint):
      # print("{} , highSug:{}, lowSug:{}".format(numberingToChar[numbering],hex((GLYPH_TABLE_INDEX_MARKER | tableIndex)),hex(tableRelativeIndex)))
  
      mCharToCodePoint[numberingToChar[numbering]] =	CodePoint((GLYPH_TABLE_INDEX_MARKER | tableIndex), (tableRelativeIndex))
  with open(outputName, 'w', encoding='utf-8') as file:
    for char in mCharToCodePoint:
      file.write("{} {} {}\n".format(char,hex(mCharToCodePoint[char].highSurrogate),hex(mCharToCodePoint[char].lowSurrogate)[2:]))


if __name__ == "__main__":
  font = "dfyuanlightbold.ttf"
  fontName = font[:-4]
  font_all_image = "font_img_{}".format(fontName)
  numberingToChar = loadJson('gameChar_Numbering2Char_{}.json'.format(fontName))
  genCharSurrogates(fontName, numberingToChar)
