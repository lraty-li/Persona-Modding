from sklearn.cluster import KMeans
from matplotlib import pyplot
from numpy import where,array
from sklearn.manifold import TSNE
from annoy import AnnoyIndex

VECTOR_DIM = 192

ann = AnnoyIndex(VECTOR_DIM, "angular")
ann.load("all-wavs.ann")  # super fast, will just mmap the file

X = []

for i in range(ann.get_n_items()):
    X.append(ann.get_item_vector(i))
X = array(X)
# tsne is only used to decrease dimension for visualization
tsne = TSNE(n_components=2, init='pca', random_state=0)
x = tsne.fit_transform(X)

def plot_clusters(X, cluster_ids):
    for class_value in range(3):
        row_ix = where(cluster_ids == class_value)
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    pyplot.show() 


kmeans_model = KMeans(n_clusters=3)
kmeans_model.fit(X)
yhat = kmeans_model.predict(X)
plot_clusters(x, yhat) 