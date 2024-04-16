import os
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(
    use_angle_cls=True, lang="ch"
)  # need to run only once to download and load model into memory
imgsRoot = r"D:\code\git\Persona-Modding\classify_sound_file_p3p\cropped"
files = os.listdir(imgsRoot)
successCounter = 0
failCounter = 0
allCharCounter = 0
lineBreaker = 0
characters = []
failNames = []
for index in range(len(files)):
    file = "{}.png".format(index)
    # if file.endswith(".png"):
    imgPath = os.path.join(imgsRoot, file)
    result = ocr.ocr(imgPath, cls=True)
    char = "_"
    if result[0] == None:
        failNames.append(file)
        failCounter += 1
    elif result[0][0][1][1] > 0.9:
    # else:
        successCounter += 1
        char = result[0][0][1][0]
    characters.append(char[0]) # TODO 会把边旁识别出字，自己训练对应字体？
    lineBreaker += 1
    if lineBreaker == 16:  # tsv table width 0xF
        characters.append("\n")
        lineBreaker = 0
    else:
        characters.append("\t")


print("success " + str(successCounter))
print("failCounter " + str(failCounter))
with open("fail.txt", "w+") as file:
    file.writelines(failNames)
with open("p3p_ns_sc.tsv", "w+") as file:
    file.writelines(characters)


print('DONE')