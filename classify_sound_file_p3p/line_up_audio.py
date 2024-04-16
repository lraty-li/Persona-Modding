import json
import shutil
import subprocess
import os
from datetime import datetime, timedelta
import random
import re

# ===================================================================

# 以下编辑都要注意切换成英文输入法
# 希望生成视频的对象，这些名称来源于P5R_sound_classfied文件夹的文件夹名字，每一位以引号包住，之后以逗号分隔。
# 如果希望同时将多为对象生成为一个视频，例如武见_妙，穿朋克装的女性，为同一人，除了用引号各自包起来之外，再加多一层中括号。还是看看下面的例子吧。
speakers = [
    ["虎狼丸", "_毛的狗"],
    # "伊莉莎_",
    "_岸_风花",
    "埃癸斯",
    [
        "桐条_美鹤",
        "美鹤的声音",
    ],
    ["鸟海老师", "女老师"],
]

# 以上的例如 “['新岛_真', '真的声音', '(SE)新岛 ...” 的命名都会使用第一个对象的名字作为名字， "新岛_真"，生成 新岛_真.mp4, 新岛_真.srt 等

# 希望生成的视频的图片的位置，例如回到以下路径去寻找 新岛_真.png 生成视频，支持png.jpg
imgsRoot = r"D:\code\git\Persona-Modding\classify_sound_file_p3p\cache\img"
defaultImgPath = r"D:\code\git\Persona-Modding\classify_sound_file_p3p\cache\img\default.png"
# 解压分类好的文件后，能够看到各自语音的文件夹。
spksRoot = r"D:\code\git\Persona-Modding\classify_sound_file_p3p\cache\classified\classified-zh"

# soundMapSpeaker... json文件的路径
textMapPath = (
    r"D:\code\git\Persona-Modding\classify_sound_file_p3p\speaker_event_msg_map-zh.json"
)
# 次字幕
subTextMapPath = (
    r"D:\code\git\Persona-Modding\classify_sound_file_p3p\speaker_event_msg_map-jp.json"
)

# 生成的视频，字幕等的输出路径
outPutFolderRoot = r"cache"


vgmtool = r"D:\.bin\vgmstream-win64\vgmstream-cli.exe"
ffmpeg = r"D:\.bin\ffmpeg.exe"
ffprobe = r"D:\.bin\ffprobe.exe"
ADX_SUB_FIX = ".ADX"
# 是否将字幕文件嵌入mp4视频,False 为关闭
embedSubtitles = True

# ===================================================================

"""
import os
spksRoot = r'E:\Temp\p5r_sound_event-20230411\P5R_sound_classfied'
files = os.listdir(spksRoot)
keyword = '导航'
a = [b for b in files if keyword in b]
print(a)
"""

timeFormat = r"%H:%M:%S,%f"
zeroTimeFormat = "00:00:00,000"


def createFolder(folderPath):
    os.makedirs(folderPath, exist_ok=True, mode=0o777)


def loadJson(filePath):
    if not filePath[-5:] == ".json":
        filePath += ".json"
    with open(filePath, "r", encoding="utf8") as file:
        return json.load(file)


# TODO 如果没有次字幕
def lineUpAudioOfSpk(speakers, outPutFolderRoot, textMap, subTextMap):
    if len(speakers) == 0:
        return
    hasSubSubTiltle = False
    if len(subTextMap) != 0:
        hasSubSubTiltle = True
    firstSpeaker = speakers[0]
    firstSpeakerRoot = os.path.join(outPutFolderRoot, firstSpeaker)
    firstSpeakerWavsRoot = os.path.join(firstSpeakerRoot, "wavs")
    if os.path.exists(firstSpeakerRoot):
        shutil.rmtree(firstSpeakerRoot)
    createFolder(firstSpeakerWavsRoot)
    concatFileListName = os.path.join(firstSpeakerRoot, "{}.txt".format(firstSpeaker))
    outPutAudioPath = os.path.join(firstSpeakerRoot, "{}.wav".format(firstSpeaker))
    srtOutPutPath = os.path.join(firstSpeakerRoot, "{}.srt".format(firstSpeaker))
    subSrtOutPutPath = os.path.join(firstSpeakerRoot, "{}-sub.srt".format(firstSpeaker))
    srtLines = []
    inputAudiosFileNames = []

    wavs = []
    subTitleMap = {}
    subSubTitleMap = {}

    speakerCacheMap = {}  # main subtitle speaker name :  sub subtitle speaker name :
    for speaker in speakers:  # TODO fuck 怎么这份代码没分开
        # speaker = speaker.replace('_','?') # 当初把？作为未知字符，但是不能用问号创建文件夹，屎山的伊始
        spkSrcRoot = os.path.join(spksRoot, speaker)
        wavs += converAdx2Wav(spkSrcRoot, firstSpeakerWavsRoot)
        subTitleMap.update(textMap[speaker])
        if hasSubSubTiltle:
            if speaker not in speakerCacheMap.keys():
                # 用一个adx的名字搜索到对应的日文名称并缓存
                # 超级面条代码啊
                testAdx = list(textMap[speaker].keys())[0]
                for subTitleSpeaker in subTextMap:
                    if testAdx in subTextMap[subTitleSpeaker]:
                        speakerCacheMap[speaker] = subTitleSpeaker
            subSpeaker = speakerCacheMap[speaker]
            # speaker 来自主字幕的textMap，例如中文名称却要获得日文文本
            subSubTitleMap.update(subTextMap[subSpeaker])

    srtLines, inputAudiosFileNames = lineUpWavs(firstSpeakerWavsRoot, wavs, subTitleMap)
    subSrtLines, _ = lineUpWavs(
        # TODO 不拆分的下场
        firstSpeakerWavsRoot,
        wavs,
        subSubTitleMap,
    )

    with open(srtOutPutPath, "w", encoding="utf8") as file:
        file.writelines(srtLines)

    with open(subSrtOutPutPath, "w", encoding="utf8") as file:
        file.writelines(subSrtLines)

    with open(concatFileListName, "w", encoding="utf8") as file:
        file.writelines(inputAudiosFileNames)
    # concat audios
    # wtf,如果concat txt内记录的是相对路径，会以concat txt的路径为基础按文件内的路径去寻找音频
    os.system(
        "ffmpeg -y -f concat -safe 0 -i {} -c copy {}".format(
            concatFileListName, outPutAudioPath
        )
    )
    # ffmpeg.input(concatFileListName, format='concat', safe=0,).output(outPutAudioPath, c='copy').run()

    supportedSubFix = ["png", "jpg"]
    vdoImg = defaultImgPath  # default img
    foundImg = False
    for imgSubFix in supportedSubFix:
        tmpVdoImg = "{}".format(
            os.path.join(imgsRoot, "{}.{}".format(firstSpeaker, imgSubFix))
        )
        if os.path.exists(tmpVdoImg):
            foundImg = True
            vdoImg = tmpVdoImg
            break

    outPutVdoPath = outPutAudioPath.replace(".wav", ".mp4")

    # -vf subtitles= '\\' problem
    # https://stackoverflow.com/questions/71597897/unable-to-parse-option-value-xxx-srt-as-image-size-in-ffmpeg
    # http://underpop.online.fr/f/ffmpeg/help/notes-on-filtergraph-escaping.htm.gz

    if embedSubtitles:
        # TODO 20240416/00:04 字幕的位置，如何调整，以及根据img的尺寸调整？
        if hasSubSubTiltle:
            command = [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                '"{}"'.format(vdoImg),
                "-i",
                '"{}"'.format(outPutAudioPath),
                "-vf",
                "subtitles='{}:force_style='Alignment=2'',subtitles='{}:force_style='Alignment=6''".format(
                    srtOutPutPath.replace("\\", "\\\\").replace(r":", r"\:"),
                    subSrtOutPutPath.replace("\\", "\\\\").replace(r":", r"\:"),
                ),
                "-c:v",
                "libx264",
                "-tune",
                "stillimage",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-pix_fmt",
                "yuv420p",
                "-shortest",
                '"{}"'.format(outPutVdoPath),
            ]

            os.system(" ".join(command))

        else:
            os.system(
                "ffmpeg -y -loop 1 -i {0} -i {1} -vf subtitles='{2}'  -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {3}".format(
                    vdoImg,
                    outPutAudioPath,
                    srtOutPutPath.replace("\\", "\\\\").replace(r":", r"\:"),
                    outPutVdoPath,
                )
            )
    else:
        os.system(
            "ffmpeg -y -loop 1 -i {0} -i {1} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {3}".format(
                vdoImg,
                outPutAudioPath,
                srtOutPutPath.replace("\\", "\\\\").replace(r":", r"\:"),
                outPutVdoPath,
            )
        )


def lineUpWavs(wavsRoot, wavs, textMap):
    absWavsRoot = os.path.abspath(wavsRoot)
    srtLines = []
    inputAudiosFileNames = []

    startTime = datetime.strptime(zeroTimeFormat, timeFormat)
    endTime = datetime.strptime(zeroTimeFormat, timeFormat)

    counter = 1
    for sfile in wavs:
        filePath = os.path.join(absWavsRoot, sfile)
        audioDuration = getDurationSeconds(filePath)
        startTime = endTime
        endTime = startTime + timedelta(seconds=float(audioDuration))
        startTimeStr = datetime.strftime(startTime, timeFormat)
        endTimeStr = datetime.strftime(endTime, timeFormat)
        text = textMap[re.sub("-random[0-9]+.wav", ADX_SUB_FIX, sfile)]
        srtLine = "{}\n{} --> {}\n{}\n\n".format(
            str(counter), startTimeStr[:-3], endTimeStr[:-3], text
        )
        counter += 1
        srtLines.append(srtLine)
        inputAudiosFileNames.append("file '{}'\n".format(filePath.replace("\\", "/")))
    return srtLines, inputAudiosFileNames


def getDurationSeconds(filePath):
    # https://gist.github.com/hiwonjoon/035a1ead72a767add4b87afe03d0dd7b
    command = [
        ffprobe,
        "-v",
        "fatal",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        filePath,
    ]
    # ffmpeg.probe(filePath)["format"]["duration"]
    ffprobeCall = subprocess.Popen(
        command, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    out, err = ffprobeCall.communicate()
    if err:
        print("error", err)
        return None
    return out


def converAdx2Wav(srcFolderRoot, wavOutputRoot):
    # if os.path.exists(wavOutputRoot):
    #     shutil.rmtree(os.path.join(wavOutputRoot))
    #     os.makedirs(wavOutputRoot)
    sfiles = os.listdir(srcFolderRoot)
    files = [sfile for sfile in sfiles if sfile.endswith(ADX_SUB_FIX)]
    wavs = []
    for adxFile in files:
        adxPath = os.path.join(srcFolderRoot, adxFile)
        outputFileName = adxFile.replace(
            ADX_SUB_FIX, "-random{}.wav".format(str(random.randint(0, 1000)))
        )
        os.system(
            '{} -o "{}" "{}"'.format(
                vgmtool, os.path.join(wavOutputRoot, outputFileName), adxPath
            )
        )
        wavs.append(outputFileName)
    return wavs


if __name__ == "__main__":
    os.system("chcp 65001")
    textMap = loadJson(textMapPath)
    subTextMap = loadJson(subTextMapPath)
    for speaker in speakers:

        if not type(speaker) == list:
            speaker = [speaker]

        lineUpAudioOfSpk(speaker, outPutFolderRoot, textMap, subTextMap)
