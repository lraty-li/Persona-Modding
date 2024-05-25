import shutil, os, sys
from pathlib import Path

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import repackBin

rebldCpkInintRoot = r"F:\TMP\cpk_output_workplace\datacpk\init"

repackFolder = r'D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\fcltable_bin'
outputBinPath = repackBin(repackFolder)
shutil.copy(outputBinPath, os.path.join(rebldCpkInintRoot, Path(outputBinPath).name))


#rebuild xci
sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool")
import rebuild_cpk