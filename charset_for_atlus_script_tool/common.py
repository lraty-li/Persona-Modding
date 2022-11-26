# -*- coding: UTF-8 -*-
import json


def dumpJson(data, fileName):
  with open(fileName, 'w', encoding="utf8") as jsonTable:
    jsonStr = json.dumps(data)
    jsonTable.write(jsonStr)  

def loadJson(filePath):
  with open(filePath,'r', encoding="utf8") as load_f:
      return json.load(load_f)
