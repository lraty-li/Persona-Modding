from sklearn.cluster import KMeans
import pandas as pd
data=pd.read_csv("kmeanstest.csv",sep=",")
print(data)

X =data["score"].to_numpy().reshape(-1,1)
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
y=kmeans.labels_
print(y)
kc=kmeans.cluster_centers_
print(kc)
kc_list=sorted([i for i in kc[:,0]])
print(kc_list)

data["cluster_center"]=kc[y]
def my(x):
    if x==kc_list[0]:
        return "差"
    elif x==kc_list[1]:
        return "中"
    elif x==kc_list[2]:
        return "良"
    else:
        return "优"
data["level"]=[my(x) for x in kc[y]]
print(data)
