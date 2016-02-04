import numpy as np
from numpy.core import multiarray
# from sklearn import cluster
from k_medoids_ import KMedoids

from devidewindow import each_devide


def correlation(x_array, y_array):
    sum = x_array + 2*y_array
    n = [np.count_nonzero(sum==i) for i in range(0, 4)]
    s=float(n[3]*n[0]-n[1]*n[2])/np.sqrt((n[3]+n[1])*(n[2]+n[0])*(n[3]+n[2])*(n[1]+n[0]))
    return s

def f(X):
    n = X.shape[0]
    C = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            C[i, j] = correlation(X[i], X[j])
    return C

windowlist = each_devide()
for i in range(len(windowlist)):
        features = (np.array(windowlist[i]) > 0).astype(int)
        sample_num = features.shape[0]
        features = features.reshape(sample_num, -1)

        #print(features.shape)
        n_clusters = 8
        kclusterd = KMedoids(n_clusters=n_clusters, distance_metric=f, max_iter=200).fit(features)
        labels = kclusterd.labels_

        Xs = []
        for i in range(n_clusters):
            Xs.append([])
        for i in range(sample_num):
            # print(label, feature)
            Xs[labels[i]].append(features[i])

        Xs = [np.array(X) for X in Xs if len(X) > 0]
        us = np.array([np.mean(X,axis=0) for X in Xs])
        Xus = [x - u for x, u in zip(Xs, us)]
        Covs = [xu.dot(xu.T) for xu in Xus]
        Pcs = [float(X.shape[0]) / sample_num for X in Xs]

        for i in range(n_clusters):
             print(Pcs[i],Covs[i].shape,us[i].shape)
