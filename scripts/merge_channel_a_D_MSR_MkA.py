"""
T_dev009_main_a贴到T_dev009_main_D的透明通道
T_dev009_main_MSR的红色通道贴到T_dev009_main_MkA的绿色通道，然后用50%灰色填充T_dev009_main_MkA的蓝色通道

@I服了You 对的，还要把蓝通道用128 128 128的灰色填充
by sims
"""

import os
from PIL import Image

outputPrefix = "auto_merge_output"
files = os.listdir(".")
targetEndsMap = ["_a", "_D", "_MkA", "_MSR"]
targets = (
    {}
)  # {"T_dev009_main" : {flags:[_a, _D, _MkA, _MSR], extension: subfix} # ([0,0,0,0],'png')
supportedImgFormat = [
    "png",
    # 'jpg' #?
]

### create output folder
counter = 0
outputRoot = "{}_{}".format(outputPrefix, counter)
while os.path.exists(outputRoot):
    counter += 1
    outputRoot = "{}_{}".format(outputPrefix, counter)
os.mkdir(outputRoot)

### gather targets
for file in files:
    nameParts = file.split(".")
    extension = nameParts[-1]
    fileName = nameParts[0]
    if extension in supportedImgFormat:
        imgDistigNameIndex = fileName.rfind("_")
        imgUniqName = fileName[0:imgDistigNameIndex]
        imgEnd = fileName[imgDistigNameIndex:]  # _a _D ...
        if not imgUniqName in targets.keys():
            targets[imgUniqName] = {"flags": [0, 0, 0, 0], "extension": extension}
        if imgEnd in targetEndsMap:
            targets[imgUniqName]["flags"][
                targetEndsMap.index(imgEnd)
            ] = 1  # 记录找到了 _a，_D 之类的

### check if file missing
nameMayPop = []
for name in targets:
    # for index in range(targets[name]):
    for index in range(4):
        if targets[name]["flags"][index] != 1:
            print("{} 缺少 {} 文件".format(name, targetEndsMap[index]))
            if not name in nameMayPop:
                nameMayPop.append(name)
for name in nameMayPop:
    targets.pop(name)


def openImage(filePrefix, uniqName, fileExtension):
    return Image.open("{}{}.{}".format(filePrefix, uniqName, fileExtension))


counter = 0
targetSum = len(targets.keys())
for filePrefix in targets:
    counter += 1
    print("处理 {}:({}/{})".format(filePrefix, counter, targetSum))
    fileExtension = targets[filePrefix]["extension"]
    imgDashA = openImage(filePrefix, "_a", fileExtension)
    imgDashD = openImage(filePrefix, "_D", fileExtension)
    imgDashMSR = openImage(filePrefix, "_MSR", fileExtension)
    imgDashMkA = openImage(filePrefix, "_Mka", fileExtension)

    ### merge _a's(_a is grey image) value into _D's alpha channel 
    # imgDashA == imgDashD
    # TODO packed exe may too bug if using numpy ？
    dashARed = imgDashA.split()[0]  # get read channel value, TODO L mode, not get red channel?
    imgDashD = imgDashD.convert("RGBA")
    dashDRed, dashDGreen, dashDBlue, _ = imgDashD.split()  # get read channel value
    newdashD = Image.merge("RGBA", [dashDRed, dashDGreen, dashDBlue, dashARed])
    newdashD.save(
        os.path.join(outputRoot, "{}{}.{}".format(filePrefix, "_D", fileExtension))
    )

    ### merge _MSR's red channel into _MkA's green channel, and fill _MkA's blue channel with 128
    dashMSRRed = imgDashMSR.split()[0]  # get read channel value
    imgDashMkA = imgDashMkA.convert("RGBA")
    imgDashMkARed, _, _, dashMkAAlpha = imgDashMkA.split()  # get read channel value
    greyImg128 = Image.new("L", imgDashMkA.size)
    greyImg128.putdata([128] * imgDashMkA.width * imgDashMkA.height)
    newdashMka = Image.merge(
        "RGBA", [imgDashMkARed, dashMSRRed, greyImg128, dashMkAAlpha]
    )
    newdashMka.save(
        os.path.join(outputRoot, "{}{}.{}".format(filePrefix, "_Mka", fileExtension))
    )
# pack up：
# pyinstaller --upx-exclude=.\upx.exe -F .\read_img.py
# 并且使用pipenv
print("https://github.com/lraty-li/Persona-Modding/tree/main/scripts")
a = input("输出到 {} , 按回车关闭".format(outputRoot))
