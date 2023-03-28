import ffmpeg
import os
import datetime
from common import loadJson

speaker = '武见_妙'
wavsRoot = os.path.join(r'E:\Temp\P5R_sound_classfied', speaker, 'wavs')
outPutFolderRoot = 'cache'
files = os.listdir(wavsRoot)
files = [sfile for sfile in files if sfile.endswith('.wav')]
textMap = loadJson('./soundMapSpeaker.json.json')
textMap = textMap[speaker]
# files = files[:10]
concatFileListName = os.path.join(outPutFolderRoot, '{}.txt'.format(speaker))
outPutAudioPath = os.path.join(outPutFolderRoot, '{}.wav'.format(speaker))
srtOutPutPath = os.path.join(outPutFolderRoot, '{}.srt'.format(speaker))

srtLines = []
inputAudiosFileNames = []
timeFormat = r'%H:%M:%S,%f'
zeroTimeFormat = r'00:00:00,000'
startTime = datetime.datetime.strptime(zeroTimeFormat, timeFormat)
endTime = datetime.datetime.strptime(zeroTimeFormat, timeFormat)

counter = 1
for sfile in files:
  filePath = os.path.join(wavsRoot, sfile)
  audioDuration = ffmpeg.probe(filePath)["format"]["duration"]
  startTime = endTime
  endTime = startTime + datetime.timedelta(seconds=float(audioDuration))
  startTimeStr = datetime.datetime.strftime(startTime, timeFormat)
  endTimeStr = datetime.datetime.strftime(endTime, timeFormat)
  text = textMap[sfile.replace('.wav', '.adx')]
  srtLine = '{}\n{} --> {}\n{}\n\n'.format(str(counter), startTimeStr[:-3], endTimeStr[:-3], text)
  counter += 1
  srtLines.append(srtLine)
  inputAudiosFileNames.append("file '{}'\n".format(filePath.replace('\\', '/')))

with open(srtOutPutPath, 'w', encoding='utf8') as file:
  file.writelines(srtLines)


with open(concatFileListName, 'w', encoding='utf8') as file:
  file.writelines(inputAudiosFileNames)

ffmpeg.input(concatFileListName, format='concat', safe=0).output(outPutAudioPath, c='copy').run()

os.system("ffmpeg -y -r 1 -loop 1 -i {1}/{0}.png -i {1}/{0}.wav -vf subtitles={1}/{0}.srt -c:v libx264 -tune stillimage  -shortest -r 1 {1}/{0}.mp4".format(speaker, outPutFolderRoot))

# imgFileName = "女神异闻录5皇家版 2022_11_20 19_44_07.png"
# input_still = ffmpeg.input()
# input_audio = ffmpeg.input(outPutAudioPath)
# (
#     ffmpeg
#     .concat(input_still, input_audio, v=1, a=1)
#     .filter("subtitles", srtOutPutPath)
#     .output(os.path.join(outPutFolderRoot, '{}.mkv'.format(speaker)))
#     .run(overwrite_output=True)
# )
