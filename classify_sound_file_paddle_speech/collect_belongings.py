from annoy import AnnoyIndex
from paddlespeech.cli.vector import VectorExecutor
import math
from utils import dumpJson, loadJson


SIMILARITY_THREADHOLD = 0.6
# SIMILARITY_THREADHOLD = 1 - (pow(distance, 2)) / 2
DISTANCE_THREADHOLD = math.sqrt(2*(1- SIMILARITY_THREADHOLD) )
N_TREE = 50
VECTOR_DIM = 192
SEARCH_K = -1
vectorExecutor = VectorExecutor()
ann = AnnoyIndex(VECTOR_DIM, "angular")
ann.load("all-wavs.ann")  # super fast, will just mmap the file
belongs = []  # index is speak id(unknow), [[2,3],[432,54]] is file2vetcorID.json id
sum = ann.get_n_items()
vector_executor = VectorExecutor()
gatherMap = {}  # voice vector id : speaker id

gatherMapKeys = gatherMap.keys()
speakerIdCounter = 0

def getValueis(value,mMap):
    items = []
    for i in mMap:
        if(mMap[i] == value):
            items.append(i)
    return items
for itemIndex in range(sum):
    if itemIndex in gatherMapKeys:
        continue
    theVector = ann.get_item_vector(itemIndex)
    # 暴力搜索
    for restIndex in range(itemIndex + 1, sum):
        # compareVect = ann.get_item_vector(restIndex)
        distance = ann.get_distance(itemIndex, restIndex)
        # similarity = 1 - (pow(distance, 2)) / 2
        if distance <= DISTANCE_THREADHOLD: 
        # too slow
        # score = vectorExecutor.get_embeddings_score(
        #     ann.get_item_vector(itemIndex), ann.get_item_vector(restIndex)
        # )
        # if score >= THEAD_HOLD:
            if itemIndex in gatherMapKeys:
                fit = True
                for i in getValueis(gatherMap[itemIndex], gatherMap):
                    distanceTemp = ann.get_distance(restIndex, i)
                    if(distanceTemp > DISTANCE_THREADHOLD):
                        fit = False
                        break
                if(fit):
                    gatherMap[restIndex] = gatherMap[itemIndex]
                continue
            if restIndex in gatherMapKeys:
                for i in getValueis(gatherMap[restIndex], gatherMap):
                    distanceTemp = ann.get_distance(itemIndex, i)
                    if(distanceTemp > DISTANCE_THREADHOLD):
                        fit = False
                        break
                if(fit):
                    gatherMap[itemIndex] = gatherMap[restIndex]
                continue
            else:
                gatherMap[itemIndex] = speakerIdCounter
                gatherMap[restIndex] = speakerIdCounter
                speakerIdCounter += 1

for i in range(speakerIdCounter):
    belongs.append([])
for wavId in gatherMapKeys:
    belongs[gatherMap[wavId]].append(wavId)
    # print()

speakerVoiceMap = {}
fileVecMap = loadJson("./file2vetcorID.json")
fileVecMapRevse = {}
# DEBUG
for i in fileVecMap.keys():
    fileVecMapRevse[fileVecMap[i]] = i
# DEBUG END
for index in range(len(belongs)):
    speakerVoiceMap[index] = []
    for i in belongs[index]:
        speakerVoiceMap[index].append(fileVecMapRevse[i])
        # speakerVoiceMap[index].append(fileVecMap[i])

dumpJson(speakerVoiceMap, "speakerVoiceMap-{}.json".format(SIMILARITY_THREADHOLD))
dumpJson(belongs, "belongs.json")
print("DONE")
