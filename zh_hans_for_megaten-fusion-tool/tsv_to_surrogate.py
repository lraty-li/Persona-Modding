# tsv from https://www.bilibili.com/read/cv21326949
def readTsv(filePath):
    # return chars list
    chars = []
    with open(filePath, "r", encoding='utf-8') as file:
        lines = file.read().splitlines()
        for line in lines:
            charsSlice = line.split("\t")
            chars += charsSlice

    return chars


# copy from https://github.com/lraty-li/Persona-Modding/blob/main/charset_for_atlus_script_tool/calc_surrogates.py,
# Offset from start of glyph range to start of the char table.
CHAR_TO_GLYPH_INDEX_OFFSET = 0x60

# Size of a single glyph table.
GLYPH_TABLE_SIZE = 0x80

# The range 0-based range of an ascii character index.
ASCII_RANGE = 0x7F

# The high bit serves as a marker for a table index.
GLYPH_TABLE_INDEX_MARKER = 0x80

class CodePoint:
    def __init__(self, high, low, tableIndex):
        self.tableIndex = tableIndex
        self.highSurrogate = high
        self.lowSurrogate = low

def genSurroagate(chars, fileName, outputFile=False):
    # mCharToCodePoint = {}
    mCodePointToChar = {}
    counter = 0
    for char in chars:
        charIndex_offseted = counter
        glyphIndex = charIndex_offseted + CHAR_TO_GLYPH_INDEX_OFFSET
        # glyphIndex = charIndex + CHAR_TO_GLYPH_INDEX_OFFSET
        # DEBUG END

        # 0X 9f  82

        # tableRelativeIndex = glyphIndex - (glyphIndex / GLYPH_TABLE_SIZE)* GLYPH_TABLE_SIZE +  GLYPH_TABLE_SIZE

        tableIndex = int((glyphIndex / GLYPH_TABLE_SIZE) - 1)
        tableRelativeIndex = glyphIndex - (tableIndex * GLYPH_TABLE_SIZE)
        # mCharToCodePoint[char] = CodePoint(
        #       (GLYPH_TABLE_INDEX_MARKER | tableIndex), (tableRelativeIndex), tableIndex = counter)

        mCodePointToChar["{}{}".format(
            hex((GLYPH_TABLE_INDEX_MARKER | tableIndex))[2:], hex(tableRelativeIndex)[2:])] = char
        counter += 1
    if(outputFile):
        with open(fileName, 'w', encoding='utf-8') as file:
            for code in mCodePointToChar:
                char = mCodePointToChar[code]
                file.write("{} {} \n".format(char, code))
    return mCodePointToChar





if __name__ == "__main__":
    tsvFilePath = "P4.tsv"
    chars = readTsv(tsvFilePath)
    genSurroagate(chars=chars, fileName="{}.txt".format(tsvFilePath))
