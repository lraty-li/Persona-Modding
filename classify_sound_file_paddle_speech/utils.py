import subprocess,os,json
ffprobe = "ffprobe"
ffmpeg = "ffmpeg"
vgmstream = 'D:/.bin/vgmstream-win64/vgmstream-cli.exe'
cacheRoot = "cache"
reSampledRoot = "cache\\reSampled"

def loadJson(filePath):
    with open(filePath,'r',encoding='utf8') as file:
        data = json.loads(file.read())
        return data


def dumpJson(data, filePath):
    with open(filePath,'w+',encoding='utf8') as file:
        file.write(json.dumps(data,ensure_ascii=False))
        

def createFolders(paths):
    for path in paths:
        if(not os.path.exists(path)):
            os.mkdir(path)

def subprocessCall(command):
    temp = []
    for i in command:
        if((type(i) == str)):
            temp.append(i)
        else:
            temp.append(str(i))
    command = temp
    ffprobeCall = subprocess.Popen(
        command, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    out, err = ffprobeCall.communicate()
    if len(err)!= 0:
        #? ffmpeg output as err?
        # raise Exception(err)
        pass
    return out

def genSampleRate(filePath):
    # ffprobe -v error -select_streams a -of default=noprint_wrappers=1:nokey=1 -show_entries stream=sample_rate
    command = [
        ffmpeg,
        "-y",
        "-v",
        "error",
        "-select_streams",
        "a",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        "-show_entries",
        "stream=sample_rate",
        filePath,
    ]
    result = subprocessCall(command)
    return int(result)


def reSample(filepath, newSampleRate="16000",audioSubfix = '.wav'):
    # ffmpeg -i in.m4a -ac 1 -ar 22050 -c:a libmp3lame -q:a 9 out.mp3
    #TODO path spliter \\ /
    newFileAPath = os.path.join(reSampledRoot, filepath.split('\\')[-1].replace('{}'.format(audioSubfix),'-{}{}'.format(newSampleRate, audioSubfix)))
    command = [ffmpeg, "-i", filepath, "-ar", newSampleRate, "-y", newFileAPath]
    result = subprocessCall(command)
    return newFileAPath

