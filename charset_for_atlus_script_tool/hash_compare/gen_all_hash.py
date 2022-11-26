
import json
from hash_compare.image_compare import pHash
import cv2
import os
font_all_image = "font_img"

def imageTopHash(imagePath):
  return pHash(cv2.imread(imagePath))

def dumpJson(data, fileName):
  with open(fileName, 'w', encoding="utf8") as jsonTable:
    jsonStr = json.dumps(data)
    jsonTable.write(jsonStr) 

def loadJson(filePath):
  with open(filePath,'r') as load_f:
      return json.load(load_f)
      

if __name__ == "__main__":

  numberingToChar = loadJson("./ttf_comparison_table_numberingToChar.json")
  charToNumbering = loadJson("./ttf_comparison_table_charToNumbering.json")

  images = os.listdir(font_all_image)
  charToPHash = {}
  for img in images:
    imgName = img[0:-4] #".png"

    # Elasticsearch？
    hash = imageTopHash(os.path.join(font_all_image, img))
    charToPHash[numberingToChar[imgName]] = hash
  dumpJson(charToPHash, "ttf_charToPHash.json")

    
