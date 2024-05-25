# 把中文字符替换成字库的日文汉字
import os

import shutil
import sys


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import *


workPlaceRoot = (
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin"
)
cacheRoot = (
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\fcltable_bin"
)

os.chdir(workPlaceRoot)
rebuildFolder = "rebuild"
zhJson = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin\ftd-zh.json"
jpJson = (
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\init\fcltable_bin\ftd.json"
)
zhMsg = loadJson(zhJson)
jpMsg = loadJson(jpJson)
msgMap = {}


# keep the order of msg
ctdMsgCountMap = {}
for key in jpMsg:
    spliterIndex = key.rfind("_")
    ctdFile = key[:spliterIndex]
    lineIndexStr = key[spliterIndex + 1 :]
    lienIndex = int(lineIndexStr)

    if ctdFile in ctdMsgCountMap.keys():
        if lienIndex < ctdMsgCountMap[ctdFile]:
            continue
    ctdMsgCountMap[ctdFile] = lienIndex

rpMsgMap = {}
for ctdF in ctdMsgCountMap:
    replacedMsgs = []
    headerBytesList = jpMsg["{}_{}".format(ctdF, 0)][1][0]
    endOfFileBytesList = []
    eofBytesListlist = jpMsg["{}_{}".format(ctdF, ctdMsgCountMap[ctdF])][1]
    if(len(eofBytesListlist)>0):
        # 可能会没有文件尾
        endOfFileBytesList = eofBytesListlist[0]
    msgBytesList = []
    for index in range(1, ctdMsgCountMap[ctdF]):
        jpMapKey = "{}_{}".format(ctdF, index)
        line = zhMsg["{}_{}".format(ctdF, index)]
        jpLine = jpMsg[jpMapKey][0]
        replacedLine = replaceZhToJpKanji(line)
        # 目前是机翻，所以限制翻译后文本不得长于原始文本，
        # 实际上也不知道最多能多长，毕竟有那些意义不明的'分隔符'
        replacedLineBytes = replacedLine.encode("shiftjis")
        jpLineBytes = jpLine.encode("shiftjis")
        zhMinusJp = len(replacedLineBytes) - len(jpLineBytes)
        if zhMinusJp <= 0:
            # 如果长度不够，补足
            # zhMinusJp=0 不能放到else
            replacedLineBytes += b"\x00" * abs(zhMinusJp)
        else:
            replacedLineBytes = replacedLineBytes[:-zhMinusJp]
        # 回插消息块
        reJoinBytesList = jpMsg[jpMapKey][1]
        reJoinBytesList = [bytes(x) for x in reJoinBytesList]
        reJoinIndex = jpMsg[jpMapKey][2]
        reJoinBytesList.insert(reJoinIndex, replacedLineBytes)
        # flatten
        reJoinBytesList = [x for x in reJoinBytesList]
        reJoinBytes = b''.join(reJoinBytesList)
        msgBytesList.append(reJoinBytes)
        # 可以在这读下原文件头，检查reJoinBytes长度是不是msg block 大小
    msgBytes = b''.join(msgBytesList)
    # rebuild file
    fileBytes = bytes(headerBytesList) + msgBytes + bytes(endOfFileBytesList)
    with open(os.path.join(cacheRoot, ctdF), "wb") as file:
        file.write(fileBytes)


# repack bin
