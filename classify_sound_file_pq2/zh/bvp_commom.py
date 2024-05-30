from pathlib import Path
import os

bvpTool = r"f:\modding\persona-tools\Amicitia-1.9.6\netcoreapp3.0\bvptool.exe"


def unapckBvp(filePath):
    # can only unapack to same path of filepath
    # it will dump to 'current path'...
    workplackGoBack = os.getcwd()
    filePathLib = Path(filePath)
    os.chdir(str(filePathLib.parent))
    command = [bvpTool, filePath]
    os.system(" ".join(command))
    os.chdir(workplackGoBack)
    return Path().joinpath(filePathLib.parent, filePathLib.stem)


def repackBvp(folderPath):
    workplackGoBack = os.getcwd()
    folderPathlib = Path(folderPath)
    os.chdir(str(folderPathlib.parent))
    # 打包也是输出到当前目录，难绷...
    command = [bvpTool, str(folderPath)]
    os.system(" ".join(command))
    outputBvpFilePath = Path().joinpath(
        folderPathlib.parent, folderPathlib.stem + ".bvp"
    )
    os.chdir(workplackGoBack)
    return outputBvpFilePath
