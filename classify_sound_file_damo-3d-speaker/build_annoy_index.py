# Copyright 3D-Speaker (https://github.com/alibaba-damo-academy/3D-Speaker). All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

"""
This script will download pretrained models from modelscope (https://www.modelscope.cn/models)
based on the given model id, and extract embeddings from input audio. 
Please pre-install "modelscope".
Usage:
    1. extract the embedding from the wav file.
        `python infer_sv.py --model_id $model_id --wavs $wav_path `
    2. extract embeddings from two wav files and compute the similarity score.
        `python infer_sv.py --model_id $model_id --wavs $wav_path1 $wav_path2 `
    3. extract embeddings from the wav list.
        `python infer_sv.py --model_id $model_id --wavs $wav_list `
"""

import json
import os
import sys
import re
import pathlib
import numpy as np
import argparse
import torch
import torchaudio
from annoy import AnnoyIndex
try:
    from speakerlab.process.processor import FBank
except ImportError:
    sys.path.append("%s/../.." % os.path.dirname(__file__))
    from speakerlab.process.processor import FBank

from speakerlab.utils.builder import dynamic_import

from modelscope.hub.snapshot_download import snapshot_download
from modelscope.pipelines.util import is_official_hub_path

# define model id here ,pay attension to embedding shape
# modelId = "damo/speech_campplus_sv_zh-cn_16k-common"
# VECTOR_DIM = 192
modelId = "damo/speech_eres2net_large_sv_zh-cn_3dspeaker_16k"
VECTOR_DIM = 512

argsStr = "--model_id {}".format(modelId)

parser = argparse.ArgumentParser(description='Extract speaker embeddings.')
parser.add_argument('--model_id', default='', type=str, help='Model id in modelscope')
parser.add_argument('--wavs', nargs='+', type=str, help='Wavs')
parser.add_argument('--local_model_dir', default='pretrained', type=str, help='Local model dir')
feature_extractor = FBank(80, sample_rate=16000, mean_nor=True)
CAMPPLUS_COMMON = {
    'obj': 'speakerlab.models.campplus.DTDNN.CAMPPlus',
    'args': {
        'feat_dim': 80,
        'embedding_size': 192,
    },
}
ERes2Net_Large_3D_Speaker = {
    'obj': 'speakerlab.models.eres2net.ResNet.ERes2Net',
    'args': {
        'feat_dim': 80,
        'embedding_size': 512,
        'm_channels': 64,
    },
}

supports = {
    "damo/speech_eres2net_large_sv_zh-cn_3dspeaker_16k": {
        "revision": "v1.0.0",
        "model": ERes2Net_Large_3D_Speaker,
        "model_pt": "eres2net_large_model.ckpt",
    },
    "damo/speech_campplus_sv_zh-cn_16k-common": {
        "revision": "v1.0.0",
        "model": CAMPPLUS_COMMON,
        "model_pt": "campplus_cn_common.bin",
    },
}


args = parser.parse_args(argsStr.split(' '))
assert isinstance(args.model_id, str) and \
    is_official_hub_path(args.model_id), "Invalid modelscope model id."
assert args.model_id in supports, "Model id not currently supported."
save_dir = os.path.join(args.local_model_dir, args.model_id.split('/')[1])
save_dir =  pathlib.Path(save_dir)
save_dir.mkdir(exist_ok=True, parents=True)

conf = supports[args.model_id]
# download models from modelscope according to model_id
cache_dir = snapshot_download(
            args.model_id,
            revision=conf['revision'],
            )
cache_dir = pathlib.Path(cache_dir)

embedding_dir = save_dir / 'embeddings'
embedding_dir.mkdir(exist_ok=True, parents=True)

# link
download_files = ['examples', conf['model_pt']]
for src in cache_dir.glob('*'):
    if re.search('|'.join(download_files), src.name):
        dst = save_dir / src.name
        try:
            dst.unlink()
        except FileNotFoundError:
            pass
        dst.symlink_to(src)

pretrained_model = save_dir / conf['model_pt']
pretrained_state = torch.load(pretrained_model, map_location='cpu')

conf = supports[args.model_id]
model = conf["model"]
embedding_model = dynamic_import(model["obj"])(**model["args"])
embedding_model.load_state_dict(pretrained_state)
embedding_model.eval()


def load_wav(wav_file, obj_fs=16000):
    wav, fs = torchaudio.load(wav_file)
    if fs != obj_fs:
        print(f"[INFO]: The sample rate of {wav_file} is not {obj_fs}, resample it.")
        wav, fs = torchaudio.sox_effects.apply_effects_tensor(
            wav, fs, effects=[["rate", str(obj_fs)]]
        )
        if wav.shape[0] > 1:
            wav = wav[0, :].unsqueeze(0)
    return wav


def compute_embedding(wav_file):
    # load wav
    wav = load_wav(wav_file)
    # compute feat
    feat = feature_extractor(wav).unsqueeze(0)
    # compute embedding
    with torch.no_grad():
        embedding = embedding_model(feat).detach().cpu().numpy()

    return embedding

def dumpJson(data, filePath):
    with open(filePath,'w+',encoding='utf8') as file:
        file.write(json.dumps(data,ensure_ascii=False))
    

wavRoot = r"D:\code\git\Persona-Modding\classify_sound_file_paddle_speech\cache\reSampled"  # have convert to 16k
# wavRoot = r"E:\modding\p5r\p5r_sound_event-20230411\make_dataset\reSampled"  # have convert to 16k


N_TREE = 20
counter = 0
file2vetcorID = {}
ann = AnnoyIndex(VECTOR_DIM, "angular")
wavs = os.listdir(wavRoot)
for wav in wavs:
    embedding = compute_embedding(os.path.join(wavRoot, wav))
    ann.add_item(counter, embedding[0])
    file2vetcorID[counter] = os.path.join(wavRoot, wav)
    # file2vetcorID[wavRoot] = counter
    counter += 1
    # print("{} / {}".format(counter, sum))
# build annoy index
ann.build(N_TREE)
ann.save("all-wavs{}.ann".format(modelId.replace('/','-')))
dumpJson(file2vetcorID, "./file2vetcorID{}.json".format(modelId.replace('/','-')))

print('DONE')