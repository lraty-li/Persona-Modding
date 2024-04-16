import json, os

voiceRoot = "./cache/voice"

langs = ["jp", "zh"]
for lang in langs:
    msgMapPath = "event_msg_map-{}.json".format(lang)
    voiceMsgMap = {}
    speakerMsgMap = {}
    files = os.listdir(voiceRoot)
    with open(msgMapPath, "r") as jsonFile:
        msgMap = json.loads(jsonFile.read())
    for file in files:
        if file.endswith(".ADX"):
            matched = False
            msgMapKey = "e{}".format(file[1:-4])
            # 搜索300 + 偏移
            femcOffset = int(file[4:7])
            msgMapKeyFemc = "e{}{}_{}".format(
                file[1:4], str(300 + femcOffset), file[8:-4]
            )
            msgMapKeys = [msgMapKey, msgMapKeyFemc]
            text = ""
            speaker = "_"
            for key in msgMapKeys:
                if key in msgMap.keys():
                    speaker = msgMap[key][0]
                    text = msgMap[key][1]
                    matched = True
                    voiceMsgMap[file] = msgMap[key]
                    break
            # not found
            if not matched:
                voiceMsgMap[file] = ""
                pass

            if speaker in speakerMsgMap.keys():
                speakerMsgMap[speaker][file] = text
            else:
                speakerMsgMap[speaker] = {file: text}

    with open("speaker_" + msgMapPath, "w+") as file:
        file.write(json.dumps(speakerMsgMap, ensure_ascii=False))
    with open("voice_" + msgMapPath, "w+") as file:
        file.write(json.dumps(voiceMsgMap, ensure_ascii=False))
    print("DONE")
