# https://github.com/tge-was-taken/Atlus-Script-Tools/blob/master/Source/AtlusScriptLibrary/Common/Text/Encodings/AtlusEncoding.cs
import struct
import os
from tsv_to_surrogate import readTsv, genSurroagate

UNKNOW_PLACE_HOLDER = "|"

#TODO 1. class ByteHandler
# 2. separate all with 0x00


def handleSingleByte(data, charTable, file):
  # data: 1 byte
  return chr(data)


def handleDoubleByte(data, charTable, file):
  char = UNKNOW_PLACE_HOLDER
  nextByte = file.read(1)[0]
  try:
    char = charTable["{}{}".format(hex(data)[2:], hex(nextByte)[2:].zfill(2))]
  except Exception as e:
    pass
  return char


switch = {
    1: handleSingleByte,
    2: handleDoubleByte
}


def decodeTBL(charTable, bytesCount=2):
  reversedTable = []
  with open(filepath, 'rb') as file:
    size = os.path.getsize(filepath)  # 获得文件大小

    while file.tell() != size:
      data0 = file.read(1)[0]
      if(data0 == 0x00):
        reversedTable.append(UNKNOW_PLACE_HOLDER)
        continue
      reversedTable.append(switch[bytesCount](data0, charTable, file))

  return reversedTable


if __name__ == '__main__':
  tsvFilePath = "P5R_EFIGS.tsv"
  filepath = 'NAME_P5R_SC.TBL'

  chars = readTsv(tsvFilePath)
  charTable = genSurroagate(
      chars=chars, fileName="{}.txt".format(tsvFilePath), outputFile=True)

  reversedTable = decodeTBL(charTable, bytesCount=2)
  with open("translated_{}.txt".format(filepath), "w", encoding='utf-8') as f:
    f.write("".join(reversedTable))
  # reg match \s+
  print('done')
