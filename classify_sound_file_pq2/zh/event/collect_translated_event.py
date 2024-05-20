import sys
from pathlib import Path


sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from common import (
    dumpJson,
)

translatedMsg = {}


def collectMsg(eventIndex, zhMsg):
    # collect msg
    global translatedMsg
    if eventIndex in translatedMsg.keys():
        if type(translatedMsg[eventIndex]) == list:
            translatedMsg[eventIndex].append(zhMsg)
        elif type(translatedMsg[eventIndex]) == str:
            translatedMsg[eventIndex] = [translatedMsg[eventIndex], zhMsg]
    else:
        translatedMsg[eventIndex] = zhMsg


if __name__ == "__main__":
    translatedFile = (
        "D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\event\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427.txt"
    )
    
    with open(translatedFile, "r") as file:
        while file.readable():
            line = file.readline()
            if len(line) <= 0:
                break
            if line[-1] == "\n":
                line = line[:-1]
            if line.startswith("=========="):
                continue
            elif line.startswith("e"):
                parts = line.split(" | ")
                eventIndex = parts[0]
                zhMsg = parts[2]
                collectMsg(eventIndex, zhMsg)

    transFileNoExte = Path(translatedFile).stem
    transFileFolder = Path(translatedFile).parent

    # dump data
    subFixs = [
        "-maped",
    ]
    targets = [
        translatedMsg,
    ]
    for index in range(len(subFixs)):
        replaceTo = subFixs[index]
        data = targets[index]
        replaceToExtension = "{}.json".format(replaceTo)
        dumpJson(
            str(Path().joinpath(transFileFolder, transFileNoExte + replaceToExtension)),
            data,
        )

    print("DONE")
