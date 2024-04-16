import json, os, shutil

langs = ["jp","zh"]
for lang in langs:
    voiceMapFile = "speaker_event_msg_map-{}.json".format(lang)
    speakerMsgMap = {}
    voiceRoot = "./cache/voice/"
    outPutRoot = "./cache/classified/classified-{}".format(lang)
    if(os.path.exists(outPutRoot)):
        shutil.rmtree(outPutRoot)
        os.makedirs(outPutRoot)

    if(os.path.exists(outPutRoot)):
        shutil.rmtree(outPutRoot)

    with open(voiceMapFile, "r") as file:
        speakerMsgMap = json.loads(file.read())

    for speaker in speakerMsgMap:
        
        speakerRoot = os.path.join(outPutRoot, speaker,)
        os.makedirs(speakerRoot, exist_ok=True)
        for adx in speakerMsgMap[speaker]:
            # voiceText = speakerMsgMap[speaker][adx]
            shutil.copyfile(
                os.path.join(voiceRoot, adx), os.path.join(speakerRoot, adx)
            )
