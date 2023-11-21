import paddle
from paddlespeech.cli.vector import VectorExecutor

vector_executor = VectorExecutor()
audio_emb = vector_executor(
    model='ecapatdnn_voxceleb12',
    sample_rate=16000,
    config=None,  # Set `config` and `ckpt_path` to None to use pretrained model.
    ckpt_path=None,
    audio_file='./85236145389.wav',
    device=paddle.get_device())
print('Audio embedding Result: \n{}'.format(audio_emb))

test_emb = vector_executor(
    model='ecapatdnn_voxceleb12',
    sample_rate=16000,
    config=None,  # Set `config` and `ckpt_path` to None to use pretrained model.
    ckpt_path=None,
    audio_file='./123456789.wav',
    device=paddle.get_device())
print('Test embedding Result: \n{}'.format(test_emb))

# score range [0, 1]
score = vector_executor.get_embeddings_score(audio_emb, test_emb)
print(f"Eembeddings Score: {score}")