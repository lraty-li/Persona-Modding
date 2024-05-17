#build cpk with compress take 12mins
#build cpk without compress take 7mins


import shutil,os

buildedCpk = r'f:\TMP\cpk_output_workplace\datacpk.cpk'
targetCpk = r'D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool\cci\cxi0\romfs\data.cpk'

#copy cpk
shutil.copy(buildedCpk, targetCpk)

# rebuild xci file
os.chdir(r'D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool')
os.system('rebuilt_romfs_3ds.bat')