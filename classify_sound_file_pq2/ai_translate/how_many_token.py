# import os
# msgRoot = 'D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\pq2_日文文本_event_20240416'

# msgs = os.listdir(msgRoot)

# length = 0
# for msg in msgs:
#     with open(os.path.join(msgRoot,msg),'r') as msgFile:
#         length += len(msgFile.read())
# print(length)


import json
msgMapPath = 'D:\code\git\Persona-Modding\classify_sound_file_pq2\event_msg_map-for_ai_transl.json'
msgMap = {}
with open(msgMapPath,'r') as msgFile:
    msgMap = json.loads(msgFile.read())

count = 0
lines = 0
for event in msgMap.keys():
    blocks = msgMap[event]
    for block in blocks:
        for lineInfo in block["linesInfo"]:
            count+= len("。".join(lineInfo[0]))
print(count)
print(lines)
