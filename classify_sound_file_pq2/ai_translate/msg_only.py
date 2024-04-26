import os
import regex as re
import json


def splitIntoBlocks(text):
    blocks = []
    start = 0
    reFindIter = re.finditer("\n\n", text, flags=0)
    for matchedIndex in reFindIter:
        blocks.append(text[start : matchedIndex.start(0)])
        start = matchedIndex.end(0)
    return blocks


def parseSpeaker(text):
    speaker = re.findall(r"(?<=\[msg .* \[).*(?=\]\])", text)
    if len(speaker) >= 1:
        return speaker[0]
    else:
        return ""


def reJoinMsg(ctlStrs, msg):
    # 尝试缝合：
    reJoin = ""
    msgLength = len(msg)
    msgCtlStrsLength = len(ctlStrs)
    if msgCtlStrsLength > msgLength:
        for i in range(msgCtlStrsLength):
            reJoin += ctlStrs[i]
            if i < msgLength:
                reJoin += msg[i]
    else:
        raise Exception("control string more  than msg?")
    return reJoin



def textPreProgress(text):
    # DEBUG
    # text = "　"
    # DEBUG END
    text = text.replace("\u3000", "  ")
    # text = text.replace("…", "..")
    # matchEllipsis = re.findall(r"…+。", text)
    # if len(matchEllipsis) > 0:
    #     text = text.replace("…", "...")
    return text


def reJoinJustMsg(ctlStrs, msg):
    oriCtlStrs = list(ctlStrs)
    reJoin = ""
    msgLength = len(msg)
    msgCtlStrsLength = len(ctlStrs)
    ctlStrNeedRemove = []
    if msgCtlStrsLength > msgLength:
        for i in range(msgCtlStrsLength):
            if ctlStrs[i] == "[n]":
                removeIndex = i
                ctlStrNeedRemove.append(removeIndex)
                reJoin += ","
            if i < msgLength:
                reJoin += msg[i]
    else:
        raise Exception("control string more  than msg?")
    ctlStrNeedRemove.reverse()
    for index in ctlStrNeedRemove:
        ctlStrs.pop(index)
    return reJoin, ctlStrs


# 要记录原本控制字符得信息，回填。总之能拼出来跟结构一模一样的文本
# [n] 临时替换为句号?
def parseLine(text):
    reFindIter = re.finditer(r"\[.*?\]", text, flags=0)
    data = []
    msg = []
    preCtlStrStart = 0
    preCtlStrEnd = 0
    ctlStrs = []
    LastCtlStr = ""
    for matchedIndex in reFindIter:
        start = matchedIndex.start(0)
        end = matchedIndex.end(0)
        if preCtlStrEnd == start:
            # 合并控制字符
            LastCtlStr = text[preCtlStrStart:end]
            preCtlStrEnd = end
        else:
            # 遇到（跳过）了msg
            msg.append(text[preCtlStrEnd:start])
            ctlStrs.append(text[preCtlStrStart:preCtlStrEnd])
            preCtlStrStart = start
            preCtlStrEnd = end
            LastCtlStr = text[start:end]
            # 如果剩下的都是控制字符，无法再进入这个流程，就LastCtlStr吧
    ctlStrs.append(LastCtlStr)
    reJoin = reJoinMsg(ctlStrs, msg)
    if text != reJoin:
        print(text)
        print(reJoin)
        raise Exception("rejoin mismatch!")
    # 把[n] 合并掉，
    # TODO 之后拼回来的时候再手动添加
    joinedMsg, ctlStrsNoNewLine = reJoinJustMsg(ctlStrs, msg)

    msgNoU3000 = textPreProgress(joinedMsg)
    return [msgNoU3000, ctlStrsNoNewLine]  # use list for json


def progressBlock(block):
    lines = iter(block.split("\n"))
    header = next(lines)
    speaker = parseSpeaker(header)
    data = []
    for line in lines:
        lineInfo = parseLine(line)
        data.append(lineInfo)

    return {"header": header, "speaker": speaker, "linesInfo": data}


evenRoot = "cache/data-extract/event"
events = os.listdir(evenRoot)
msgMap = {}
for event in events:
    dirPath = os.path.join(evenRoot, event)
    if os.path.isfile(dirPath):
        continue
    files = os.listdir(dirPath)
    for file in files:
        if not file.endswith(".msg"):
            continue
        else:
            # eventId = re.findall(r"e\d*", file)[0]
            # eventSubId = re.findall(r"(?<=_)\d*(?=.bf)", file)[0]
            with open(os.path.join(evenRoot, event, file), "r") as msgFile:
                msgRaw = msgFile.read()
                msgBlocks = splitIntoBlocks(msgRaw)
                blocksData = []
                for block in msgBlocks:
                    data = progressBlock(block)
                    blocksData.append(data)
            msgMap[file] = blocksData

with open("msg_-{}.json".format("ai_transl"), "w+") as file:
    file.write(json.dumps(msgMap, ensure_ascii=False))

print("DONE")
