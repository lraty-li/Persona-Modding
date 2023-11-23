import os
import subprocess
import re
awbsRoot = r'E:\Temp\p4g_sound\sound\adx2'
vgmExe = r'D:\Game\P5RModding\vgmstream-win64\vgmstream-cli.exe'

outPutPath = r'./cache'

if not os.path.exists(outPutPath):
  os.mkdir(outPutPath)


def dunmAwb(filepath, steamCount):
  # ./vgmstream-cli.exe -s 0 -S 50 -o ./temp/temp_?s.wav 'F:/Game/p4g/sound/adx2/v070501.awb'

  prefix = re.search('(?<=v)(\d+)(?=.awb)', filepath)
  if (prefix == None):
    print('dumAwb error')
    return
  prefix = prefix.group(0)
  # TODO 音频从0开始，0没声音
  command = "{} -s 0 -S {} -o {}/{}_?s.wav {}".format(vgmExe, steamCount, outPutPath, prefix, filepath)
  os.system(command)


def getStreamCount(filePath):
  command = [vgmExe,
             '-m',
             filePath,
             ]
  subCall = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  out, err = subCall.communicate()
  if (err):
    print('error', err)
    return -1
  outStr = str(out)
  streamCount = re.search(r'(?<=stream count: )(\d+)', outStr)
  if (streamCount == None):
    return -1
  streamCount = int(streamCount.group(0))
  return streamCount


def dunmpAllAwb():
  files = os.listdir(awbsRoot)

  awbs = [i for i in files if i.startswith('v')]  # TODO rematch

  for awb in awbs:
    awbPath = os.path.join(awbsRoot, awb)
    steamCount = getStreamCount(awbPath)
    dunmAwb(awbPath, steamCount)


if __name__ == '__main__':
  dunmpAllAwb()

  print('DONE')
