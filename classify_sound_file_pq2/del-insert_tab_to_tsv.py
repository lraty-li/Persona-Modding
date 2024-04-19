import os


tsvFiles = [
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data\font\pq2_seurapro_12_12.tsv",
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\data\font\pq2_seurapro_13_13.tsv",
]


BYTES_OF_CHAR = 2
for tsv in tsvFiles:
    with open(tsv, "r",encoding='utf-16') as file:
        newData = []
        chars = file.read()
        for char in chars:
            if(char != '\n'):
                newData.append(char)
                newData.append('\t')
            else:
                newData.pop()
                newData.append(char)
        print()

        # newData = bytearray()
        # fileSize = os.path.getsize(tsv)
        # lineBreakCounter = 0
        # fileHeader = file.read(2)
        # for i in range(2,int(fileSize / BYTES_OF_CHAR)):
        #     data = file.read(BYTES_OF_CHAR)
        #     newData.extend(data)
        #     #TODO 文件头，utf16: FF FE, 
        #     if not (data == b'\x0d\x00' or data == b'\x0a\x00'):
        #         newData.extend(b'\x09')
        with open(os.path.split(tsv)[1], "w",encoding='utf-8') as outputFile:
            outputFile.write("".join(newData))
        print()
print('DONE')
