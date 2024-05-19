import sys

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\zh")
from zh_common import unpackBin


if __name__ == "__main__":

    targets = [
        "D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\cmptable.bin",
        "D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\init\ori-cmptable.bin",
    ]
    for targ in targets:
        unpackBin(targ)
