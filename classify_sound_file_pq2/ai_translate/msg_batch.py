import json

msgMapPath = "D:\code\git\Persona-Modding\classify_sound_file_pq2\event_msg_map-for_ai_transl.json"
msgMap = {}
msgPartsMap = {}
with open(msgMapPath, "r") as msgFile:
    msgMap = json.loads(msgFile.read())
spliter = "|"
msgBatchedMap = {}
for event in msgMap.keys():
    blocks = msgMap[event]
    msgs = []
    for blockIndex in range(len(blocks)):
        block = blocks[blockIndex]
        for lineInfoIndex in range(len(block["linesInfo"])):
            lineInfo = block["linesInfo"][lineInfoIndex]
            for msgInnerLineIndex in range(len(lineInfo[0])):
                # if(spliter in msg):
                #     raise Exception("{} is in msg".format(spliter))
                msgPartsMap[
                    "{}_{}_{}_{}".format(
                        event, blockIndex, lineInfoIndex, msgInnerLineIndex
                    )
                ] = lineInfo[0][msgInnerLineIndex]



# G, 翻译会去掉分隔符，不如直接来吧
with open(msgMapPath.replace('.json','-parts.json'), "w") as msgFile:
    msgFile.write(json.dumps(msgPartsMap,ensure_ascii=False))
print()
