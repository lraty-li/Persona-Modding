import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

# Plot the elbow
pyplot.plot(K, distortions, 'bx-')
pyplot.xlabel('n_cluster')
pyplot.ylabel('Distortion')
pyplot.title('The Elbow Method showing the optimal k')
pyplot.show() 