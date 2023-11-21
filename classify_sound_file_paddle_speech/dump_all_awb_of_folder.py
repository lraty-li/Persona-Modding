# ./vgmstream-cli.exe -s 0 -S 50 -o ./temp/temp_?s.wav 'F:/Game/p4g/sound/adx2/v070501.awb'
# the '-S 50' from output of  ./vgmstream-cli.exe 'F:/Game/p4g/sound/adx2/v070501.awb'

from utils import subprocessCall,vgmstream
import re,os
outputRoot ='cache/all_wav'
awbRoot = 'E:\modding\p5r\SOUND_JP\SOUND\BATTLE'

def getStreamCount(awbFilePath):
    command = [
        # "cmd",
        vgmstream,
        awbFilePath
    ]
    result = subprocessCall(command)
    streamCount = re.findall("(?<=stream count: )(\d+)",str(result))[0]
    
    return int(streamCount)

def dumpAwb(awbFilePath,outputRoot):
    awbFileName = awbFilePath.split('\\')[-1].replace('.awb','')
    steamCount = getStreamCount(awbFilePath)
    command = [
        vgmstream,
        '-s',
        0,
        '-S',
        steamCount,
        '-o',
        '{}/{}_{}'.format(outputRoot,awbFileName,'?s.wav'),
        awbFilePath,
    ]
    result = subprocessCall(command)
    return result

def dumpAllAwb(awbRoot):
    streamSum = 0
    files = os.listdir(awbRoot)
    awbs = [i for i in files if(i.endswith('.AWB'))]
    for awb in awbs:
        awbFilPath = os.path.join(awbRoot, awb)
        streamSum += getStreamCount(awbFilPath)
        dumpAwb(awbFilPath,outputRoot)
    print(streamSum)

# testAwb = "E:\\modding\\p5r\\SOUND_JP\\SOUND\\BATTLE\\BE_BOSS_0745.AWB"
# dumpAwb(testAwb,"cache/all_wav")

dumpAllAwb(awbRoot)