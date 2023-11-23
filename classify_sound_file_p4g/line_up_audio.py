import subprocess
import os
from datetime import datetime, timedelta
from common import loadJson, createFolder
import random
import re

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


def lineUpAudioOfSpks(speakers, outPutFolderRoot, textMapPath, spksRoot, vgmtool='./vgmstream-cli.exe', ffmpeg='./ffmpeg.exe', ffprobe='./ffprobe.exe', embedSubtitles=True):
  textMap = loadJson(textMapPath)

  for sSpeaker in speakers:
    if (type(sSpeaker) != list):
      sSpeaker = [sSpeaker]
    lineUpAudioOfSpk(sSpeaker, outPutFolderRoot, textMap, spksRoot,vgmtool, ffmpeg, ffprobe, embedSubtitles=embedSubtitles)


def lineUpAudioOfSpk(speakers, outPutFolderRoot, textMap, spksRoot, vgmtool='vgmstream-cli.exe', ffmpeg='ffmpeg.exe', ffprobe='ffprobe.exe', embedSubtitles=True):
  if (len(speakers) == 0):
    return
  firstSpeaker = speakers[0]
  firstSpeakerWavsRoot = os.path.join(spksRoot, firstSpeaker)
  firstSpeakerRoot = os.path.join(outPutFolderRoot, firstSpeaker)
  createFolder(firstSpeakerRoot)
  concatFileListName = os.path.join(firstSpeakerRoot, '{}.txt'.format(firstSpeaker))
  outPutAudioPath = os.path.join(firstSpeakerRoot, '{}.wav'.format(firstSpeaker))
  srtOutPutPath = os.path.join(firstSpeakerRoot, '{}.srt'.format(firstSpeaker))
  srtLines = []
  inputAudiosFileNames = []

  wavs = []
  subTextMap = {}

  for speaker in speakers:
    spkSrcRoot = os.path.join(spksRoot, speaker)
    # wavs += converAdx2Wav(spkSrcRoot, firstSpeakerWavsRoot, vgmtool)
    wavs = os.listdir(spkSrcRoot)
    subTextMap.update(textMap[speaker])

  srtLines, inputAudiosFileNames = lineUpWavs(firstSpeakerWavsRoot, wavs, subTextMap, ffprobe)

  with open(srtOutPutPath, 'w', encoding='utf8') as file:
    file.writelines(srtLines)

  with open(concatFileListName, 'w', encoding='utf8') as file:
    file.writelines(inputAudiosFileNames)
  os.system('{} -y -f concat -safe 0 -i {} -c copy {}'.format(ffmpeg, concatFileListName, outPutAudioPath))
  # ffmpeg.input(concatFileListName, format='concat', safe=0,).output(outPutAudioPath, c='copy').run()

  # imgsRoot = outPutFolderRoot
  vdoImg = "{}".format(os.path.join(imgsRoot, '{}.png'.format(firstSpeaker)))
  if not os.path.exists(vdoImg):
    vdoImg = "{}".format(os.path.join(imgsRoot, '{}.jpg'.format(firstSpeaker)))
    if not os.path.exists(vdoImg):
      vdoImg = '../img/default.png'  # default img
  outPutVdoPath = outPutAudioPath.replace('.wav', '.mp4')

  # -vf subtitles= '\\' problem
  # https://stackoverflow.com/questions/71597897/unable-to-parse-option-value-xxx-srt-as-image-size-in-ffmpeg
  # http://underpop.online.fr/f/ffmpeg/help/notes-on-filtergraph-escaping.htm.gz

  if (embedSubtitles):
    os.system("{4} -y -loop 1 -i {0} -i {1} -vf subtitles=\'{2}\'  -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {3}".format(vdoImg, outPutAudioPath, srtOutPutPath.replace('\\', '\\\\').replace(r':', r'\:'), outPutVdoPath, ffmpeg))
  else:
    os.system("{4} -y -loop 1 -i {0} -i {1} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {3}".format(vdoImg, outPutAudioPath, srtOutPutPath.replace('\\', '\\\\').replace(r':', r'\:'), outPutVdoPath, ffmpeg))


def lineUpWavs(wavsRoot, wavs, textMap, ffprobe):

  srtLines = []
  inputAudiosFileNames = []

  startTime = datetime.strptime(zeroTimeFormat, timeFormat)
  endTime = datetime.strptime(zeroTimeFormat, timeFormat)

  counter = 1
  for sfile in wavs:
    filePath = os.path.join(wavsRoot, sfile)
    audioDuration = getDurationSeconds(filePath, ffprobe)
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


def getDurationSeconds(filePath, ffprobe):
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
  if (err):
    print('error', err)
    return None
  return out


def converAdx2Wav(srcFolderRoot, wavOutputRoot, vgmtool):
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

  speakers = [
      # '暗影理世',
      # '白钟直斗_',
      # '玛丽',
      # '久慈川理世_',
      # '里中千枝_',
      # '玛格丽特',
      # '天城雪子_',
      '柏木老师',
  ]

  imgsRoot = r'cache'

  # 解压分类好的文件后，能够看到各自语音的文件夹。
  spksRoot = r'D:\Temp\cache\classfied'

  # soundMapSpeaker... json文件的路径
  textMapPath = r'soundMapSpeaker.json'

  # 生成的视频，字幕等的输出路径
  outPutFolderRoot = r'D:\Temp\cache\videos'

  vgmtool = r'.\bins\vgmstream-cli.exe'
  ffmpeg = r'.\bins\ffmpeg.exe'
  ffprobe = r'.\bins\ffprobe.exe'

  embedSubtitles = True

  os.system('chcp 65001')
  lineUpAudioOfSpks(speakers, outPutFolderRoot, textMapPath, spksRoot, vgmtool, ffmpeg, ffprobe)
  print('DONE')
