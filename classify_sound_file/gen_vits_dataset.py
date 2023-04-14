import os
from common import loadJson
from xpinyin import Pinyin

classfyOutputRoot = 'E:\Temp\p5r_sound_event-20230411'
sndFilesOutputRoot = os.path.join(classfyOutputRoot, 'P5R_sound_classfied')
cacheFolderRoot = 'cache'
vgmtool = r'D:\Game\P5RModding\vgmstream-win64\vgmstream-cli.exe'
speakerMapZhJP = loadJson('E:\Temp\p5r_sound_event-20230411\speakerMapZhJp')
sndMapSpeakerTexts = 'soundMapSpeaker-jp-2023-04-11-15-25-34'

# keyword = '芳泽'
# folders = os.listdir(classfyOutputRoot)
# susFolders = [i for i in folders if keyword in i]

targets = ['芳泽_', '芳泽_堇', '芳泽_跋', '被称为芳泽的学生']

sndMap = loadJson(os.path.join(classfyOutputRoot, sndMapSpeakerTexts))
fileListLines = []

for speaker in targets:
  speakerEng = Pinyin().get_pinyin(speaker, splitter="", convert = 'capitalize')
  speakerSndFilesRoot = os.path.join(sndFilesOutputRoot, speaker)
  jPSpeaker = speakerMapZhJP[speaker]
  for adxName in os.listdir(speakerSndFilesRoot):
    wavName = "{}-{}.wav".format(speakerEng, adxName[:-4])
    wavOutputPath = os.path.join(cacheFolderRoot, "wav", wavName)
    text = sndMap[jPSpeaker][adxName]
    fileListLines.append("wav/{}|{}\n".format(wavName.replace('\\', '/'), text)) #TODO muti speaker
    adxPath = os.path.join(speakerSndFilesRoot, adxName)
    os.system("{} -o {} \"{} #h22050.txtp\"".format(vgmtool, wavOutputPath, adxPath))
with open('./cache/fileLists.txt', 'w+' , encoding='utf8') as file:
  file.writelines(fileListLines)
print('DONE')
