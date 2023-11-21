# -*- coding: UTF-8 -*-
import json
import os
import audio_to_vector
from annoy import AnnoyIndex
from paddlespeech.cli.vector import VectorExecutor
import math
from scipy import spatial
from utils import dumpJson, reSample

WAV_ROOT = ["cache\\all_wav"]

# https://github.com/currentslab/awesome-vector-search

file2vetcorID = {}
if __name__ == "__main__":
    VECTOR_DIM = 192
    N_TREE = 20

    ann = AnnoyIndex(VECTOR_DIM, "angular")
    vectorExecutor = VectorExecutor()

    counter = 0
    for folder in WAV_ROOT:
        wavs = os.listdir(folder)
        sum = len(wavs)

        # DEBUG
        # vect1 = audio_to_vector.audio2Vector('cache/reSampled/Dm_ED_0007_Text_038_b-16000.wav', vectorExecutor)
        # vect2 = audio_to_vector.audio2Vector('cache/reSampled/Dm_RT_0022_Text_004_c-16000.wav', vectorExecutor)
        # vect3 = audio_to_vector.audio2Vector('cache/reSampled/Dm_RT_0022_Text_004_b-16000.wav', vectorExecutor)
        # print(vect1)
        # print(vect2)
        # score = vectorExecutor.get_embeddings_score(vect1, vect1)
        # score1 = vectorExecutor.get_embeddings_score(vect1, vect2)
        # result = 1 - spatial.distance.cosine(vect1, vect2)
        # DEBUG END

        for wav in wavs:
            # Elasticsearch？
            wavPath = os.path.join(folder, wav)
            newAudioPath = reSample(wavPath)
            audioVtct = audio_to_vector.audio2Vector(newAudioPath, vectorExecutor)
            
            ann.add_item(counter, audioVtct)
            file2vetcorID[counter] = wavPath
            # file2vetcorID[wavPath] = counter
            counter += 1
            # print("{} / {}".format(counter, sum))
        # build annoy index
        ann.build(N_TREE)
        ann.save("all-wavs.ann".format(folder))
        dumpJson(file2vetcorID, "./file2vetcorID.json")

print('DONE')