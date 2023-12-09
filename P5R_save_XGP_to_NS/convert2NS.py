# 把XGP格式的P5R的存档转为NS形式文件名
import os, shutil

outPut = "./common_save"
systHex = [0x53, 0x00, 0x59, 0x53, 0x00, 0x54, 0x00]  # SYST

if os.path.exists(outPut):
    shutil.rmtree(outPut)
files = os.listdir(".")
os.mkdir(outPut)


class SaveFile:
    def __init__(self, data):  # 约定成俗这里应该使用r，它与self.r中的r同名
        containerIndex = 0
        saveIndex = containerIndex + 1
        if len(data) != 2:
            raise Exception
        if not data[containerIndex].startswith("container"):
            containerIndex = saveIndex
            saveIndex = 0
        self.containerFile = data[containerIndex]
        self.dataFile = data[saveIndex]


# DEBUG
# files = ["2D8AE9E086F548C89DD1D93A22D272AC"]
# DEBUG END
counter = 0
for file in files:
    counter += 1
    if os.path.isdir(file):
        dataFile = os.listdir(os.path.join(file))
        saveFile = SaveFile(dataFile)

        with open(os.path.join(file, saveFile.containerFile), "rb") as containerFile:
            containerFile.seek(8)
            data = containerFile.read(1)
            if systHex[0] != data[0]:
                newFolderName = "DATA{}".format(str(counter).rjust(2, "0"))
                newFolderPath = os.path.join(outPut, newFolderName)
                os.mkdir(newFolderPath)
                shutil.copy(os.path.join(file, saveFile.dataFile), os.path.join(newFolderPath, "DATA.DAT"))
                continue
            # is SYSTEM.DAT
            newFolderPath = os.path.join(outPut,'SYSTEM')
            os.mkdir(newFolderPath)
            shutil.copy(
                os.path.join(file, saveFile.dataFile),
                os.path.join(newFolderPath, "SYSTEM.DAT"),
            )

