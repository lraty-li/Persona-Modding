

#need hcakey still  https://discord.com/channels/746211612981198989/1032755521624748132/1033208896438943854

import os
cridModExePath = r"D:\Game\P5RModding\unpackMovie\MOVIE_JE\MOVIE\crid_mod.exe" 
cridParams = "-b 00234168 -a 3D2FDBA6 -v -x"
folderRoot = r"D:\Game\P5RModding\unpackMovie\MOVIE_JE\MOVIE\USM"

#ffmpeg.exe -i .\MOV000.m2v -i MOV000_40534641.wav -c copy MOV000.mkv
ffmpeg = "ffmpeg.exe"



def gatherUSMs(files, extension):
  targets = []
  for file in files:
    if file.endswith(extension):
      targets.append(file)
  return targets



def cridUsm(usms):

  for usm in usms:
    os.system(cridModExePath +" "+ cridParams +" " + os.path.join(folderRoot, usm))

def mergeMovie(usms):
  # 40534641 ENG #0
  # 41534641 JPN audio #1
  for usm in usms:
    usmName = usm[:-4]
    os.system("{} -i {}.m2v -i {}_41534641.wav -c copy {}.mkv".format(ffmpeg, usmName,usmName,usmName))

def renameBins(bins):

  for bin in bins:
    newName = "{}.hca".format(bin[:-4])
    os.rename(os.path.join(folderRoot,bin), os.path.join(folderRoot,newName),)

if __name__ == '__main__':
  files = os.listdir(folderRoot)
  usms = gatherUSMs(files, ".USM")
  bins = gatherUSMs(files, ".bin")
  # renameBins(bins)
  mergeMovie(usms)
