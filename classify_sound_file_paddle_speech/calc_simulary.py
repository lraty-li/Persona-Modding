import audio_to_vector
from annoy import AnnoyIndex
from utils import reSample
from paddlespeech.cli.vector import VectorExecutor


wav1 = r"cache\all-wav\SPT02.AWB_1001.wav"
wav2 = r"cache\all-wav\SPT01.AWB_869.wav"
wav3 = r"cache\all-wav\SPT02.AWB_1012.wav"


VECTOR_DIM = 192
N_TREE = 20
vectorExecutor = VectorExecutor()
ann = AnnoyIndex(VECTOR_DIM, "angular")
audioVtct1 = audio_to_vector.audio2Vector(reSample(wav1), vectorExecutor)
audioVtct2 = audio_to_vector.audio2Vector(reSample(wav2), vectorExecutor)
audioVtct3 = audio_to_vector.audio2Vector(reSample(wav3), vectorExecutor)

ann.build(N_TREE)
ann.add_item(0, audioVtct1)
ann.add_item(1, audioVtct2)
ann.add_item(2, audioVtct3)

distance = ann.get_distance(0,1)
distance2 = ann.get_distance(0,2)

similarity = 1 - (pow(distance, 2)) / 2
score = vectorExecutor.get_embeddings_score(audioVtct1, audioVtct2)
score1 = vectorExecutor.get_embeddings_score(audioVtct3, audioVtct2)
# print(distance)
print(score)
print(score1)
# print(similarity)