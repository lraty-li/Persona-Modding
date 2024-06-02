import sys, os

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import readBinFile, valueToLittleBytes, fillToBytes, getReveBinValue

NEXT_BLOCK_SIZE_SIZE = 4
FILE_NAME_SIZE = 0x20


def getArcFileNames(arcFilePath, arcHeader):
    # keep the order
    fileBytes = readBinFile(arcFilePath)
    index = 0
    index += len(arcHeader)
    fileNames = []
    while index < len(fileBytes):
        nameBytes = fileBytes[index : index + FILE_NAME_SIZE]
        nameBytes = nameBytes.replace(b"\00", b"")
        name = nameBytes.decode("shiftjis")
        fileNames.append(name)
        index += FILE_NAME_SIZE
        nextBlockSize = getReveBinValue(fileBytes[index : index + NEXT_BLOCK_SIZE_SIZE])
        index += NEXT_BLOCK_SIZE_SIZE
        index += nextBlockSize
    return fileNames


def rebuildArcBytes(folderRoot, targets,arcHeader):
    arcBytes = b""
    arcBytes += arcHeader
    for targ in targets:
        fileNameTemplate = [0] * FILE_NAME_SIZE
        fileNameTemplate = fillToBytes(0, fileNameTemplate, targ.encode("shiftjis"))
        filePath = os.path.join(folderRoot, targ)
        fileBytes = readBinFile(filePath)
        nextBlockfileSizeBytes = valueToLittleBytes(len(fileBytes), width=4)
        arcBytes += bytes(fileNameTemplate)
        arcBytes += nextBlockfileSizeBytes
        arcBytes += fileBytes
    return arcBytes