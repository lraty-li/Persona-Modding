# -*- coding: UTF-8 -*-
import os
from gen_all_hash import imageTopHash, loadJson
from hash_compare.image_compare import cmpHash
import time

target_images_path = "D:\Game\P5RModding\pyScript\ocr\cropped"

charToNumbering = loadJson("./ttf_comparison_table_charToNumbering.json")
charToHash = loadJson("ttf_charToPHash.json")
THREADHOLD = 0.85
imgNameToChar = {}

# for img in os.listdir(target_images_path):
for img in range(749, 752):
  hash = imageTopHash(os.path.join(target_images_path, "{}.png".format(img)))
  #todo vgg
  sTime = time.time()
  mostMaybePair = {"char":"", "distance" : 64}
  for char in charToHash:
    distance = cmpHash(hash, charToHash[char])
    if(distance < mostMaybePair["distance"]):
      mostMaybePair["char"] = char
      mostMaybePair["distance"] = distance
  imgNameToChar[img] = mostMaybePair
  endTime = time.time()
  print("takes:{}".format(endTime - sTime))

  print("{} : {}".format(img, mostMaybePair['char']))



  
