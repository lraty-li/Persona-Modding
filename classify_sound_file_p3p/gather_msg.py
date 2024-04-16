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


def removeCtlStr(line):
    start = 0
    line = line.replace("[n]", "\n")
    reFindIter = re.finditer("\[.*\]", line, flags=0)
    lineParts = []
    for matchedIndex in reFindIter:
        lineParts.append(line[start : matchedIndex.start(0)])
        start = matchedIndex.end(0)
    return "".join(lineParts)

def parseVoiceGroup(blocks):
    textMap = {}
    # f 3 1 1 0 0 编号
    for block in blocks:
        lines = iter(block.split("\n"))
        speaker = re.findall(r"(?<=\[msg .* \[).*(?=\]\])", next(lines))
        # speaker = re.findall(r"(?<=\[msg MSG_\d\d\d \[).*(?=\]\])", next(lines))
        if len(speaker) != 1:
            continue
        speaker = speaker[0]
        for line in lines:
            voiceTextNum = re.findall(r"(?<=\[f 3 1 1 0 0 )\d*(?=\])", line)
            if len(voiceTextNum) < 1:
                continue
            voiceTextNum = voiceTextNum[0]
            # look-behind requires fixed-width pattern
            # pip install regex
            voiceText = re.findall(r"(?<=\[f 3 1 1 0 0 \d*\]).*(?=\[e\])", line)[0]
            voiceText = removeCtlStr(voiceText)
            # if speaker.isspace():
            #     speaker = "_" * len(speaker)
            speaker = speaker.replace(" ", "_")
            if speaker in textMap.keys():
                textMap[voiceTextNum].append((speaker, voiceText))
            else:
                textMap[voiceTextNum] = (speaker, voiceText)

    return textMap


langs = ["jp", "zh"]
for lang in langs:
    evenRoot = "./cache/event-{}".format(lang)
    events = os.listdir(evenRoot)
    msgMap = {}
    for event in events:
        files = os.listdir(os.path.join(evenRoot, event))
        for file in files:
            if not file.endswith(".msg"):
                continue
            else:
                # DEBUG
                with open(os.path.join(evenRoot, event, file), "r") as msgFile:
                    # with open("cache/event-zh/e100/e109_301.bf.msg", "r") as msgFile:
                    # DEBUG END
                    eventId = re.findall(r"e\d*", file)[0]
                    eventSubId = re.findall(r"(?<=_)\d*(?=.bf)", file)[0]
                    msgRaw = msgFile.read()
                    msgBlocks = splitIntoBlocks(msgRaw)
                    msg = parseVoiceGroup(msgBlocks)
                    # if eventSubId == "301":
                    #     # TODO 女主线
                    #     pass
                    if (
                        lang == "zh"
                        and eventId == "e175"
                        and eventSubId == "301"
                        # and voiceLineIndex == "27"
                    ):
                        print()

                    for voiceLineIndex in msg:
                        msgMapKey = "{}{}_{}".format(
                            eventId, eventSubId, voiceLineIndex.zfill(5)
                        )
                        msgMap[msgMapKey] = msg[voiceLineIndex]
    with open("event_msg_map-{}.json".format(lang), "w+") as file:
        file.write(json.dumps(msgMap, ensure_ascii=False))
    print("DONE")
