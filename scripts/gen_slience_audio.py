import ffmpy3
import subprocess
import json
import os

targets = ['MOV084.USM', 'MOV085.USM', 'MOV086.USM',
 'MOV100.USM', 'MOV101.USM', 'MOV102.USM', 'MOV103.USM', 'MOV104.USM', 'MOV106.USM', 'MOV250.USM', 'MOV251.USM', 'MOV252.USM', 'MOV253.USM', 'MOV254.USM', 'MOV297.USM', 'MOV298.USM', 'MOV299.USM', 'MOV302.USM', 'MOV303.USM', 'MOV308.USM', 'MOV309.USM', 'MOV310.USM', 'MOV311.USM', 'MOV312.USM', 'MOV313.USM', 'MOV314.USM', 'MOV316.USM', 'MOV317.USM', 'MOV318.USM']





def get_duration_from_ffmpeg(url):
    tup_resp = ffmpy3.FFprobe(
        inputs={url: None},
        global_options=[
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams'
        ]
    ).run(stdout=subprocess.PIPE)

    meta = json.loads(tup_resp[0].decode('utf-8'))
    return meta['format']['duration']


for usm in targets:
  usmName = usm[:-4]
  length = get_duration_from_ffmpeg(usmName+".m2v")
  commandGenWav = "ffmpeg -y -f lavfi -i anullsrc -t {} {}.wav".format(length, usmName)
  # commandM2V2MKV = "ffmpeg -i {}.m2v -vcodec copy -acodec copy {}}.mkv".format(usmName, usmName)
  timeStampParam = "-fflags +genpts "
  commandMergeVA = "ffmpeg -y {} -i {}.m2v -i {}.wav -c copy {}.mkv".format(timeStampParam, usmName, usmName, usmName)
  os.system(commandGenWav)
  # os.system(commandM2V2MKV)
  os.system(commandMergeVA)



length = get_duration_from_ffmpeg('MOV100.m2v')
print(length)
