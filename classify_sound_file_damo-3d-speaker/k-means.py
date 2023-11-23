from sklearn.cluster import KMeans
from matplotlib import pyplot
from numpy import where,array
from sklearn.manifold import TSNE
from annoy import AnnoyIndex
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.metrics import silhouette_score
from utils import dumpJson, loadJson

# speech_eres2net_large_sv_zh-cn_3dspeaker_16k
modelName = "damo-speech_eres2net_large_sv_zh-cn_3dspeaker_16k"
# VECTOR_DIM = 192
VECTOR_DIM = 512
ann = AnnoyIndex(VECTOR_DIM, "angular")
# ann.load(r"all-wavs-damo-speech_campplus_sv_zh-cn_16k-common.ann")  # super fast, will just mmap the file
ann.load("all-wavs{}.ann".format(modelName))  # super fast, will just mmap the file
file2Vector = loadJson("file2vetcorID{}.json".format(modelName))
X = []

for i in range(ann.get_n_items()):
    X.append(ann.get_item_vector(i))
X = array(X)
# tsne is only used to decrease dimension for visualization
tsne = TSNE(n_components=2, init='pca', random_state=0)
x = tsne.fit_transform(X)

N_CLUSTERS = 30
def plot_clusters(X, cluster_ids):
    for class_value in range(N_CLUSTERS):
        row_ix = where(cluster_ids == class_value)
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    pyplot.show() 


kmeans_model = KMeans(n_clusters=N_CLUSTERS)
kmeans_model.fit(X)
labels = kmeans_model.labels_
file2cluser = {}
for i in range(N_CLUSTERS):
    file2cluser[str(i)] = []
for i in range(len(X)):
    file2cluser[str(labels[i])].append(file2Vector[str(i)])
dumpJson(file2cluser, "file2Cluser-{}.json".format(modelName))
# yhat = kmeans_model.predict(X)

# plot_clusters(x, yhat) 

# from sklearn.cluster import MeanShift
# model = MeanShift()
# yhat = model.fit_predict(X)
# plot_clusters(x, yhat) 



# from sklearn.cluster import AgglomerativeClustering
# model = AgglomerativeClustering(n_clusters=N_CLUSTERS)
# yhat = model.fit_predict(X)
# plot_clusters(x, yhat) 


# from sklearn.mixture import GaussianMixture
# model = GaussianMixture(n_components=N_CLUSTERS)
# model.fit(X)
# yhat = model.predict(X)
# plot_clusters(x, yhat) 



# paint n-clusters with elbow
# distortions = []
# silhouette_avg = []
# K = range(2,50)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k).fit(X)
#     kmeanModel.fit(X)
#     # distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
#     silhouette_avg.append(silhouette_score(X, kmeanModel.labels_)) # 14 or 16?
# # Plot the elbow
# # pyplot.plot(K, distortions, 'bx-')
# pyplot.plot(K, silhouette_avg, 'bx-')
# pyplot.xlabel('n_cluster')
# pyplot.ylabel('Distortion')
# pyplot.title('The Elbow Method showing the optimal k')
# pyplot.show() 

print('DONE')