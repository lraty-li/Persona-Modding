# https://github.com/tge-was-taken/Atlus-Script-Tools/blob/master/Source/AtlusScriptLibrary/Common/Text/Encodings/AtlusEncoding.cs
import struct
import os
from tsv_to_surrogate import readTsv, genSurroagate


if __name__ == '__main__':
  tsvFilePath = "P4_hanS.tsv"
  filepath = 'MSG_ENG.TBL'
  unknowPlaceHolder = " "


  chars = readTsv(tsvFilePath)
  charTable = genSurroagate(
      chars=chars, fileName="{}.txt".format(tsvFilePath), outputFile=True)

  reversedTable = []
  with open(filepath, 'rb') as file:
    size = os.path.getsize(filepath)  # 获得文件大小
    
    while file.tell() != size:
      # DEBUG FOR ENG
      # data = file.read(1)  # 每次输出一个字节
      # DEBUG END
      data0 = file.read(1)[0]
      if(data0 == 0x00):
        reversedTable.append(unknowPlaceHolder)
        continue
      data1 = file.read(1)[0]
      char = unknowPlaceHolder
      try:
        char = charTable["{}{}".format(
            hex(data0)[2:], hex(data1)[2:].zfill(2))]

        # DEBUG FOR ENG
        # char = chr(data[0])
        # if(data[0] == 0x00):
        #   char = "."
        
        # DEBUG END
      except Exception as e:
        pass
      reversedTable.append(char)
      continue
  with open("translated_{}.txt".format(filepath), "w", encoding='utf-8') as f:
    f.write("".join(reversedTable))
  # reg match \s+
  print('done')
