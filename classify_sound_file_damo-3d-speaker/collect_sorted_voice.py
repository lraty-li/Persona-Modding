import os, shutil

from utils import loadJson

# clusers : [filePath, filePath, ...]
file2cluser = loadJson("file2Cluser-damo-speech_eres2net_large_sv_zh-cn_3dspeaker_16k.json")
outPutRoot = "cache/output"
wavRoot= r"D:\code\git\Persona-Modding\classify_sound_file_paddle_speech\cache\all_wav\\"


if not os.path.exists(outPutRoot):
        os.mkdir(outPutRoot)
else:
    shutil.rmtree(outPutRoot)
    os.mkdir(outPutRoot)
     
for belongId in file2cluser:
    files = file2cluser[belongId]
    targetPathRoot = os.path.join(outPutRoot, str(belongId))
    if not os.path.exists(targetPathRoot):
        os.mkdir(targetPathRoot)
    for file in files:
        # D:\code\git\Persona-Modding\classify_sound_file_paddle_speech\cache\all_wav
        fileName = file.split('\\')[-1].replace('-16000','')
        shutil.copy(wavRoot+fileName, os.path.join(targetPathRoot, fileName))
    
print('DONE')