import json,time,os
import regex as re


import openai 

from open_ai import translate
# from sakura13b import translate
from openai_api_ket import API_KEY

msgMapPath = "D:\code\git\Persona-Modding\classify_sound_file_pq2\msg_-ai_transl-parts.json"
msgMap = {}


def writeToFile(filePath, data):
    with open(filePath, "a") as file:
        file.write("{}\n".format(data))
def readLastIndex(outPutPath):
    line = ''
    if(not os.path.exists(outPutPath)):
        return ''
    with open(outPutPath, 'r') as file:
        lines = file.readlines()
        if(len(lines) == 0):
            return ''
        line  = re.findall(r'e.*.bf.msg.*?(?= \|)', lines[-1])
    if(len(line)<1):
        return ''
    return line[0]

def shuildBypass(text):
    #DEBUG
    #text = "　"
    #DEBUG END
    if(text.isspace()):
        return text.replace('\u3000','  ')
    matchEllipsis = re.findall(r'…+。',text)
    if(len(matchEllipsis) >0):
        return text
    return ''

if __name__ == "__main__":
    with open(msgMapPath, "r") as msgFile:
        msgMap = json.loads(msgFile.read())

    client = openai.OpenAI(
        api_key=API_KEY,
        base_url="https://api.v36.cm/v1/",
        # base_url="http://localhost:5000/v1",

    )

    outputPath = msgMapPath.replace(".json", "-zh.json")
    # outputPath = msgMapPath.replace(".json", "-zh-sakura7b.json")
    lastIndex = readLastIndex(outputPath)
    if(len(lastIndex) == 0):
        # file not exist
        pass
    writeToFile(
        outputPath,
        "========== {} ==========".format(time.asctime(time.localtime(time.time()))),
    )
    # DEBUG
    DEBUG = False
    if(DEBUG):
        jp = "\u3000格言シーン"
        zh = translate(client, jp)
        print(zh)
    # DEBUG END
    msgMapKyes = msgMap.keys()
    if(len(lastIndex) >=1):
        msgMapKyes = list(msgMapKyes)[list(msgMapKyes).index(lastIndex)+1:]
        pass
    for index in msgMapKyes:
        jpMsg = msgMap[index]
        retryThisOne = True
        while( retryThisOne):
            try:
                    sShuildBypass = shuildBypass(jpMsg)
                    # jpMsg = "オイオイ、しっかりしろよ。,ヘンな夢でもみたのか？"
                    if(len(sShuildBypass) > 0):
                        zhMsg = sShuildBypass
                    else:
                        zhMsg = translate(client, jpMsg)
                    retryThisOne = False
            except openai.error.InvalidRequestError as e:
                if e.error.code == "content_filter" and e.error.innererror:
                    retryThisOne = True
                    content_filter_result = e.error.innererror.content_filter_result

        
        line = "{} | {} | {}".format(index, jpMsg, zhMsg)
        writeToFile(outputPath, line)
        print(line)
        #time.sleep(1)
