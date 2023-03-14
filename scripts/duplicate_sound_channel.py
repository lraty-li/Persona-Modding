
import soundfile as sf
import numpy as np
import os
def gatherExtensions(files, extension):
  targets = []
  for file in files:
    if file.endswith(extension):
      targets.append(file)
  return targets

folderRoot = r"F:\Game\p5r_cpk\MOVIE"
files = os.listdir(folderRoot)
wavs = gatherExtensions(files, '.wav')

misSoundChannel = []
sum = len(wavs)


targets = ['000out.wav', 'MOV050_40534641 [1].wav', 'MOV050_THE_40534641 [1].wav', 'MOV058_40534641 [1].wav', 'MOV059_40534641 [1].wav', 'MOV060_40534641 [1].wav', 'MOV060_41534641 [1].wav', 'MOV061_40534641 [1].wav', 'MOV061_41534641 [1].wav', 'MOV063_40534641 [1].wav', 'MOV063_41534641 [1].wav', 'MOV064_40534641 [1].wav', 'MOV064_41534641 [1].wav', 'MOV065_40534641 [1].wav', 'MOV065_41534641 [1].wav', 'MOV066_40534641 [1].wav', 'MOV066_41534641 [1].wav', 'MOV068_40534641 [1].wav', 'MOV068_41534641 [1].wav', 'MOV069_40534641 [1].wav', 'MOV069_41534641 [1].wav', 'MOV070_40534641 [1].wav', 'MOV072_40534641 [1].wav', 'MOV073_40534641 [1].wav', 'MOV074_40534641 [1].wav', 'MOV075_40534641 [1].wav', 'MOV076_40534641 [1].wav', 'MOV077_40534641 [1].wav', 'MOV078_40534641 [1].wav', 'MOV079_40534641 [1].wav', 'MOV080_40534641 [1].wav', 'MOV091_40534641 [1].wav', 'MOV091_J_40534641 [1].wav', 'MOV093_40534641 [1].wav', 'MOV093_J_40534641 [1].wav', 'MOV096_40534641 [1].wav', 'MOV096_J_40534641 [1].wav']
for wav in targets:
  print(wavs.index(wav),"/" ,sum)
  sig, sample_rate = sf.read(wav)
  if(sig.shape[1] != 6):
    misSoundChannel.append((wav, sig.shape[1]))
    continue
  #data =  np.repeat(sig, (1, 1, 1, 1, 2, 2), axis=1)
  #sf.write(wav, data, sample_rate, subtype='PCM_16')

print("sound channel not equ 6 :" ,misSoundChannel)

"""
sound channel not equ 6 : [('000out.wav', 8), ('MOV050_40534641 [1].wav', 2), ('MOV050_THE_40534641 [1].wav', 2), ('MOV058_40534641 [1].wav', 2), ('MOV059_40534641 [1].wav', 2), ('MOV060_40534641 [1].wav', 2), ('MOV060_41534641 [1].wav', 2), ('MOV061_40534641 [1].wav', 2), ('MOV061_41534641 [1].wav', 2), ('MOV063_40534641 [1].wav', 2), ('MOV063_41534641 [1].wav', 2), ('MOV064_40534641 [1].wav', 2), ('MOV064_41534641 [1].wav', 2), ('MOV065_40534641 [1].wav', 2), ('MOV065_41534641 [1].wav', 2), ('MOV066_40534641 [1].wav', 2), ('MOV066_41534641 [1].wav', 2), ('MOV068_40534641 [1].wav', 2), ('MOV068_41534641 [1].wav', 2), ('MOV069_40534641 [1].wav', 2), ('MOV069_41534641 [1].wav', 2), ('MOV070_40534641 [1].wav', 2), ('MOV072_40534641 [1].wav', 2), ('MOV073_40534641 [1].wav', 2), ('MOV074_40534641 [1].wav', 2), ('MOV075_40534641 [1].wav', 2), ('MOV076_40534641 [1].wav', 2), 
('MOV077_40534641 [1].wav', 2), ('MOV078_40534641 [1].wav', 2), ('MOV079_40534641 [1].wav', 2), ('MOV080_40534641 [1].wav', 2), ('MOV091_40534641 [1].wav', 2), ('MOV091_J_40534641 [1].wav', 2), ('MOV093_40534641 [1].wav', 2), ('MOV093_J_40534641 [1].wav', 2), ('MOV096_40534641 [1].wav', 2), ('MOV096_J_40534641 [1].wav', 2)]
"""
