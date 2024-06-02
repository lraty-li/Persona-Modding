import os, sys


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from msg_parser import MsgMapType, parseMsgFile, getMsgLines
from common import dumpJson


def collectMsg():
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
                blocksData = parseMsgFile(
                    os.path.join(evenRoot, event, file), joinMsgOneLine=False
                )
                msgMap[file] = blocksData

    jsonOutputPath = os.path.join(codeWorkplace, "msg.json")
    getMsgLines(jsonOutputPath, MsgMapType.EVENT)
    dumpJson(jsonOutputPath, msgMap)


codeWorkplace = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    collectMsg()
