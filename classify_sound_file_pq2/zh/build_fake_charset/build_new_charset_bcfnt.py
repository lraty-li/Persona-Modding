# https://github.com/dnasdw/cbf_cj/blob/master/bin/make_cbf.bat

# copy dtd, or?
# f:\modding\persona-tools\3dsfont-master\bin\ctr_FontConverter\xlor\letter-order.dtd
import shutil,os

shutil.copy(
    r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\build_fake_charset\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-jp-charSet.xlor",
    r'F:\modding\persona-tools\3dsfont-master\bin\ctr_FontConverter\xlor\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-jp-charSet.xlor'
)
ctrFontConv = r"f:\modding\persona-tools\3dsfont-master\bin\ctr_FontConverter\ctr_FontConverterConsole.exe"

targets = ["seurapro_12_12", "seurapro_13_13"]

imgRoot  = r'D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\build_fake_charset\cropped'
rebuildCPKFont = r'F:\TMP\cpk_output_workplace\datacpk\font'
xlorPath = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh\build_fake_charset\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-jp-charSet.xlor"
cpXlorPath = r'F:\modding\persona-tools\3dsfont-master\bin\ctr_FontConverter\xlor\jp-charSet.xlor'
shutil.copy(xlorPath, cpXlorPath)
os.chdir(r'F:\modding\persona-tools\3dsfont-master\bin\ctr_FontConverter')
for fontName in targets:
    command = [
        "ctr_FontConverterConsole.exe -i image -if",
        os.path.join(imgRoot, fontName + '.bmp'),
        "-io",
        cpXlorPath
        ," -ic A8 -o bcfnt -oe sjis -of",
        os.path.join(rebuildCPKFont,"{}.bcfnt".format(fontName))
    ]
    os.system(" ".join(command))

# move to  F:\TMP\cpk_output_workplace\datacpk\font

# '''
# .\ctr_FontConverterConsole.exe -i image -if 
# "D:\code\git\Persona-Modding\classify_sound_file_pq2\build_fake_charset\cropped\seurapro_13_13.bmp" 
# -io "F:\modding\persona-tools\3dsfont-master\bin\ctr_FontConverter\xlor\pq2-event-msg-zhsc-gpt-3.5-turbo-0125-20240427-jp-charSet.xlor"
#  -ic A8 -o bcfnt -of test13.bcfnt
# '''