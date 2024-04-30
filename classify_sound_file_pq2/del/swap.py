import json

mMap = {}
mMapR = {}
with open("build_fake_charset/temp.json", "r") as file:
    mMap = json.loads(file.read())
for i in mMap:
    mMapR[mMap[i]] = i
with open("./tempR.json", "w") as file:
    file.write(json.dumps(mMapR, ensure_ascii=False))
