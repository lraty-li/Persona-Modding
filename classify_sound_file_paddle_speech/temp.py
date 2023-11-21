from utils import loadJson

data = loadJson('./speakerVoiceMap.json')

sum = 0
for i in data:
    sum+= len(data[i])

print(sum)