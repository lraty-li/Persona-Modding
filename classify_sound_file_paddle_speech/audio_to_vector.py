import subprocess
import paddle, os
from paddlespeech.cli.vector import VectorExecutor
from utils import subprocessCall,ffmpeg,createFolders,reSampledRoot,reSample



createFolders([reSampledRoot])


def audio2Vector(filepath,vector_executor = VectorExecutor()):
    # vector_executor = VectorExecutor()
    audio_emb = vector_executor(
        model="ecapatdnn_voxceleb12",
        sample_rate=16000,
        config=None,  # Set `config` and `ckpt_path` to None to use pretrained model.
        ckpt_path=None,
        audio_file=filepath,
        device=paddle.get_device(),
        force_yes=True
    )
    return audio_emb
    # result = vector_executor(audio_file=filepath)
    # return result


# # score range [0, 1]
# ec = VectorExecutor()
# score = ec.get_embeddings_score(audio_emb, test_emb)
# print(f"Eembeddings Score: {score}")

if __name__ == "__main__":
    path = reSample("cache\\testing.wav")
    embedding = audio2Vector(path)
    print(embedding)
