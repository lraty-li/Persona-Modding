# build cpk with compress take 12mins
# build cpk without compress take 7mins


import shutil, os
import subprocess


def rebuildCPK():

    buildedCpk = r"f:\TMP\cpk_output_workplace\datacpk.cpk"
    targetCpk = r"D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool\cci\cxi0\romfs\data.cpk"

    # rebuild cpk
    # -dir=
    cpkmakec = "F:\modding\persona-tools\CRI_File_System_Tools_v2.40.13.0\cpkmakec.exe"
    cpkCsv = "f:\TMP\cpk_output_workplace\ori-data.csv"
    outputCpk = "f:\TMP\cpk_output_workplace\datacpk.cpk"
    cpkFilesRoot = "F:\TMP\cpk_output_workplace\datacpk"
    command = [
        cpkmakec,
        cpkCsv,
        outputCpk,
        "-dir=" + cpkFilesRoot,
        "-align=2048 -mode=FILENAME -view",
    ]
    os.system(" ".join(command))

    # copy cpk
    shutil.copy(buildedCpk, targetCpk)

    # rebuild xci file
    os.chdir(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool")
    os.system("rebuilt_romfs_3ds.bat")
    os.system(
        "START {}".format(
            r"F:\Games\3ds\citra-windows-msys2-20240406-0c2f076\citra-qt.exe"
        )
    )


if __name__ == "__main__":
    rebuildCPK()
