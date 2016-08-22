import json
import math
import randomevent
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.decomposition import PCA, KernelPCA
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN

from sklearn.preprocessing import StandardScaler

import numpy as np
import matplotlib.pyplot as plt


def Vectorizer(events):
	ct = CountVectorizer()
	ct.fit(events)
	tfidf = TfidfTransformer()
	counters = ct.transform(events)
	tfidf.fit(counters)
	return tfidf.transform(counters).toarray()
def time_tronc(time,tronc='h'):
        """give the troncated time
                input:
                -----
                        time : XX:XX:XX (24h) 
                        tronc : h = hour , m = minutes , s = secondes
        """
        # h : hour
        # m : minutes
        # s : secondes
        tr = {"h":0,'m':1,'s':2}
        indices = tr[tronc]
        ti = ['00','00','00']
        spl = time.split(':')
        for i in xrange(indices+1):
                ti[i] = spl[i]
        return ':'.join([t for t in ti])
def get(ev,fields):
	d = {}
	for f in fields:
		d[f] = ev[f]
	return d

def datasplit(events,fields = ['action','code','device','user_agent'],tronc='h',time_fields = 'time'):
	data = {}
	for ev in events:
		time = time_tronc(ev[time_fields],tronc=tronc)
		
		if time not in data:
			data[time] = ' '.join([w for w in get(ev,fields).values()])
		else:
			data[time] += ' ' + ' '.join([w for w in get(ev,fields).values()])

	return data

events = randomevent.events(number=60*100+20).evts(M='Dec',d=31,h=23,m=59,s=58)
#['action', 'code', 'device', 'ip_adress', 'response_size', 'time', 'date', 'response_time', 'user_agent']

v = datasplit(events,tronc='h').values()
X =  Vectorizer(v)

X = StandardScaler().fit_transform(X)

kpca = KernelPCA(kernel="rbf", fit_inverse_transform=True, gamma=100)
X_kpca = kpca.fit_transform(X)
X_back = kpca.inverse_transform(X_kpca)
pca = PCA()
X_pca = pca.fit_transform(X)

model = TSNE(n_components=2, random_state=0)
X_tsne = model.fit_transform(X)

X_pca = StandardScaler().fit_transform(X_kpca)
db = DBSCAN(eps=0.52, min_samples=20).fit(X_pca)
X = X_pca
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_


n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


# Plot results
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
