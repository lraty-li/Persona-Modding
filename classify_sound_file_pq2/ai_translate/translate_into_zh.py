import json
import time

from openai import OpenAI

from open_ai import translate
from openai_api_ket import API_KEY

msgMapPath = "D:\code\git\Persona-Modding\classify_sound_file_pq2\event_msg_map-for_ai_transl-parts.json"
msgMap = {}


def writeToFile(filePath, data):
    with open(filePath, "a") as file:
        file.write("{}\n".format(data))


if __name__ == "__main__":
    with open(msgMapPath, "r") as msgFile:
        msgMap = json.loads(msgFile.read())

    #TODO client 都由key那里创建
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://free.gpt.ge/v1/",
    )

    outputPath = msgMapPath.replace(".json", "-zh.json")
    writeToFile(
        outputPath,
        "========== {} ==========".format(time.asctime(time.localtime(time.time()))),
    )
    # DEBUG
    DEBUG = True
    if(DEBUG):
        jp = "\u3000格言シーン"
        zh = translate(client, jp)
        print(zh)
    # DEBUG END
    for index in msgMap:
        jpMsg = msgMap[index]
        zhMsg = translate(client, jpMsg)
        line = "{} | {} | {}".format(index, jpMsg, zhMsg)
        writeToFile(outputPath, line)
        print(line)
        time.sleep(1)
