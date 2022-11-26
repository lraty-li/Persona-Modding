import json
from ocr_api import ocr_space_file
import os
import time


APIKEY = ""

imaegFolderBase = "cropped-preProgressed"
outputFolder = "ocr-oneline-output"

chi_sc = (749,7529)
lang_chi_sc = "chs"
# chi_sc = (749,751)

if(not os.path.exists(outputFolder)):
    os.mkdir(outputFolder)

def imageToString(charRange, lang):
  with open(os.path.join(outputFolder,"{}.txt".format(lang)), "w", encoding='utf-8') as resultFile:
    for numbering in range(charRange[0], charRange[-1]):
      startTime = time.time()
      result = ocr_space_file(os.path.join(imaegFolderBase, "{}.png".format(numbering)), api_key=APIKEY, language= lang)
      endTime = time.time()
      resultFile.write(",{} : {}".format(numbering, result) ,)
      # parsedResults = json.loads(result)
      # parsedResult = parsedResults["ParsedResults"][0]["ParsedText"]
      
      print("{} done, with {}s".format(numbering, int(endTime-startTime)))
  #todo 文件第一个都好换成 "{",文件尾插入 "}"

result = imageToString(chi_sc,lang_chi_sc)
