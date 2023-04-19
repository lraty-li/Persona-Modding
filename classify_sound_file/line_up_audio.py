import subprocess
import os
from datetime import datetime, timedelta
from common import loadJson, createFolder
import random
import re

# ===================================================================

# 以下编辑都要注意切换成英文输入法
# 希望生成视频的对象，这些名称来源于P5R_sound_classfied文件夹的文件夹名字，每一位以引号包住，之后以逗号分隔。
# 如果希望同时将多为对象生成为一个视频，例如武见_妙，穿朋克装的女性，为同一人，除了用引号各自包起来之外，再加多一层中括号。还是看看下面的例子吧。
speakers = [
    '艾丝卡鲁格•拉拉',  # BUG '艾丝卡鲁格•拉拉', '•' invalidate
    '米莱迪',
    ["武见_妙", "穿朋克装的女性"],
    ['拉雯妲', '诗(拉雯妲)'],
    ['芳泽_堇', '芳泽_跋', '芳泽_'],
    ['新岛_真', '真的声音', '(SE)新岛_真', '(通信)少女的声音(新岛_真)'],
    '约瑟',
    ['佐仓_双叶', '(NAVI)佐仓_双叶', '(SE)佐仓_双叶', '(通信)少女的声音(佐仓_双叶)', '暗影双叶'],
    ['导航App语音', '导航的声音', '异世界导航App'],
]

# 以上的例如 “['新岛_真', '真的声音', '(SE)新岛 ...” 的命名都会使用第一个对象的名字作为名字， "新岛_真"，生成 新岛_真.mp4, 新岛_真.srt 等

# 希望生成的视频的图片的位置，例如回到以下路径去寻找 新岛_真.png 生成视频，支持png.jpg
imgsRoot = r'E:\Code\Git\Persona-Modding\classify_sound_file\cache'

# 解压分类好的文件后，能够看到各自语音的文件夹。
spksRoot = r'E:\Temp\p5r_sound_event-20230414\P5R_sound_classfied'

# soundMapSpeaker... json文件的路径
textMapPath = r'E:\Code\Git\Persona-Modding\classify_sound_file\soundMapSpeaker-2023-04-14-13-11-02.json'

# 生成的视频，字幕等的输出路径
outPutFolderRoot = r'E:\Code\Git\Persona-Modding\classify_sound_file\cache'


vgmtool = r'D:\Game\P5RModding\vgmstream-win64\vgmstream-cli.exe'
ffmpeg = r'D:\.bin\ffmpeg.exe'
ffprobe = r'D:\.bin\ffprobe.exe'

# 是否将字幕文件嵌入mp4视频,False 为关闭
embedSubtitles = True

# ===================================================================

'''
import os
spksRoot = r'E:\Temp\p5r_sound_event-20230411\P5R_sound_classfied'
files = os.listdir(spksRoot)
keyword = '导航'
a = [b for b in files if keyword in b]
print(a)
'''

timeFormat = r'%H:%M:%S,%f'
zeroTimeFormat = '00:00:00,000'


def lineUpAudioOfSpk(speakers, outPutFolderRoot, textMap):
  if(len(speakers) == 0):
    return
  firstSpeaker = speakers[0]
  firstSpeakerRoot = os.path.join(outPutFolderRoot, firstSpeaker)
  firstSpeakerWavsRoot = os.path.join(firstSpeakerRoot, 'wavs')
  createFolder(firstSpeakerWavsRoot)
  concatFileListName = os.path.join(firstSpeakerRoot, '{}.txt'.format(firstSpeaker))
  outPutAudioPath = os.path.join(firstSpeakerRoot, '{}.wav'.format(firstSpeaker))
  srtOutPutPath = os.path.join(firstSpeakerRoot, '{}.srt'.format(firstSpeaker))
  srtLines = []
  inputAudiosFileNames = []

  wavs = []
  subTextMap = {}

  for speaker in speakers:
    spkSrcRoot = os.path.join(spksRoot, speaker)
    wavs += converAdx2Wav(spkSrcRoot, firstSpeakerWavsRoot)
    subTextMap.update(textMap[speaker])

  srtLines, inputAudiosFileNames = lineUpWavs(firstSpeakerWavsRoot, wavs, subTextMap)

  with open(srtOutPutPath, 'w', encoding='utf8') as file:
    file.writelines(srtLines)

  with open(concatFileListName, 'w', encoding='utf8') as file:
    file.writelines(inputAudiosFileNames)
  os.system('ffmpeg -y -f concat -safe 0 -i {} -c copy {}'.format(concatFileListName, outPutAudioPath))
  # ffmpeg.input(concatFileListName, format='concat', safe=0,).output(outPutAudioPath, c='copy').run()

  vdoImg = "{}".format(os.path.join(imgsRoot, '{}.png'.format(firstSpeaker)))
  if not os.path.exists(vdoImg):
    vdoImg = "{}".format(os.path.join(imgsRoot, '{}.jpg'.format(firstSpeaker)))
    if not os.path.exists(vdoImg):
      vdoImg = './img/default.png'  # default img
  outPutVdoPath = outPutAudioPath.replace('.wav', '.mp4')

  # -vf subtitles= '\\' problem
  # https://stackoverflow.com/questions/71597897/unable-to-parse-option-value-xxx-srt-as-image-size-in-ffmpeg
  # http://underpop.online.fr/f/ffmpeg/help/notes-on-filtergraph-escaping.htm.gz

  if(embedSubtitles):
    os.system("ffmpeg -y -loop 1 -i {0} -i {1} -vf subtitles=\'{2}\'  -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {3}".format(vdoImg, outPutAudioPath, srtOutPutPath.replace('\\', '\\\\').replace(r':', r'\:'), outPutVdoPath))
  else:
    os.system("ffmpeg -y -loop 1 -i {0} -i {1} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {3}".format(vdoImg, outPutAudioPath, srtOutPutPath.replace('\\', '\\\\').replace(r':', r'\:'), outPutVdoPath))


def lineUpWavs(wavsRoot, wavs, textMap):

  srtLines = []
  inputAudiosFileNames = []

  startTime = datetime.strptime(zeroTimeFormat, timeFormat)
  endTime = datetime.strptime(zeroTimeFormat, timeFormat)

  counter = 1
  for sfile in wavs:
    filePath = os.path.join(wavsRoot, sfile)
    audioDuration = getDurationSeconds(filePath)
    startTime = endTime
    endTime = startTime + timedelta(seconds=float(audioDuration))
    startTimeStr = datetime.strftime(startTime, timeFormat)
    endTimeStr = datetime.strftime(endTime, timeFormat)
    text = textMap[re.sub('-random[0-9]+.wav', '.adx', sfile)]
    srtLine = '{}\n{} --> {}\n{}\n\n'.format(str(counter), startTimeStr[:-3], endTimeStr[:-3], text)
    counter += 1
    srtLines.append(srtLine)
    inputAudiosFileNames.append("file '{}'\n".format(filePath.replace('\\', '/')))
  return srtLines, inputAudiosFileNames


def getDurationSeconds(filePath):
  # https://gist.github.com/hiwonjoon/035a1ead72a767add4b87afe03d0dd7b
  command = [ffprobe,
             '-v', 'fatal',
             '-show_entries',
             'format=duration',
             '-of',
             'default=noprint_wrappers=1:nokey=1',
             filePath,
             ]
  # ffmpeg.probe(filePath)["format"]["duration"]
  ffprobeCall = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  out, err = ffprobeCall.communicate()
  if(err):
    print('error', err)
    return None
  return out


def converAdx2Wav(srcFolderRoot, wavOutputRoot):
  sfiles = os.listdir(srcFolderRoot)
  files = [sfile for sfile in sfiles if sfile.endswith('.adx')]
  wavs = []
  for adxFile in files:
    adxPath = os.path.join(srcFolderRoot, adxFile)
    outputFileName = adxFile.replace('.adx', '-random{}.wav'.format(str(random.randint(0, 1000))))
    os.system("{} -o {} \"{}\"".format(vgmtool, os.path.join(wavOutputRoot, outputFileName), adxPath))
    wavs.append(outputFileName)
  return wavs


if __name__ == '__main__':
  os.system('chcp 65001')
  textMap = loadJson(textMapPath)
  for speaker in speakers:

    if(not type(speaker) == list):
      speaker = [speaker]

    lineUpAudioOfSpk(speaker, outPutFolderRoot, textMap)
