from ctd_commom import targets
import shutil, os, sys
from pathlib import Path
from ctd_commom import unpackedBin

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import repackBin

rebldCpkInintRoot = r"F:\TMP\cpk_output_workplace\datacpk\init"


unPath = Path(unpackedBin)
outputBinPath = Path().joinpath(unPath.parent, unPath.name.replace("_", "."))
repackBin(unpackedBin)
shutil.copy(outputBinPath, os.path.join(rebldCpkInintRoot, Path(outputBinPath).name))


#rebuild xci
sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool")
import rebuild_cpk