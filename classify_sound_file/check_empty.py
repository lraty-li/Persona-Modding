from common import *

soundMap = loadJson("./soundMap-readable.json")

soundNoRef = []

counterSum = 0
counterEmpty = 0
for i in soundMap:
  for j in soundMap[i]:
    if(len(soundMap[i][j]) == 0):
      soundNoRef.append((i,j))
      counterEmpty += 1
    else:
      # shrink
      try:
        soundMap[i][j].pop('title')
        soundMap[i][j].pop('index')
      except Exception as e:
        pass
    counterSum += 1
      # print(i,j)

with open("soundMap_shrinked.json", 'w+', encoding='utf8') as file:
  file.write(json.dumps(soundMap, ensure_ascii=False))

# print(soundNoRef)
with open("empty.txt", 'w+', encoding='utf8') as file:
  file.writelines([str(i)+"\n" for i in soundNoRef])
print("{} {} {}" .format(counterEmpty, counterSum, counterEmpty/counterSum))
# all : 36654

print("DONE")
