import math
# Not necessary in future but recommand
import numpy as np
import random
#######################################
def distance(p,q,l=2):
	res = 0.0
	for i in xrange(len(p)):
		res += abs(p[i]-q[i])**l
	return math.sqrt(res)
#from __future__ import division
def mean(data):
	res = [0]*len(data[0])
	for d in data:
		for i in xrange(len(d)):
			res[i] += d[i]/float(len(data))
	return res
	#return np.mean(a)	
class kmeans:
	def __init__(self,k=2,n=100):
		self.k = k
		self.n_step = n
	def clusters_(self,data,indices):
		clusters = {}
		for key in indices:
			if key not in clusters:
				clusters[key] = []
			for i in indices[key]:
				clusters[key].append(data[i])
		centroids = {}
		for key in clusters:
			centroids[key] = mean(clusters[key])
		return clusters,centroids
	
	def fit(self,data):
		# from https://en.wikipedia.org/wiki/K-means_clustering
		k = self.k
		n_step = self.n_step
		centroids = random.sample(data,k)
		counter_ = 0
		indices_c = {}
		while counter_ < n_step:
			counter_ += 1
			indices_c = {}
			for j in xrange(len(data)):
				x_j = data[j]
				for i in xrange(len(centroids)):
					# compare the first centroid
					if i not in indices_c:
						indices_c[i] = []
					m_i = centroids[i]
					k_tmp = 0
					for i_s in xrange(len(centroids)):
						m_i_s = centroids[i_s]
						if i_s!=i:
							d_i = distance(m_i,x_j)
							d_i_s = distance(m_i_s,x_j)
							if d_i <= d_i_s:
								k_tmp += 1
					if k_tmp == k-1:
						indices_c[i].append(j)
			clusters,centroids = cl.clusters_(data,indices_c)
					
		return clusters,centroids
#k = kmeans(k=3)
#data = [[1,0],[1,1],[1,23],[2,1.2],[1,25]]
#print len(data)
#print k.fit(data)
