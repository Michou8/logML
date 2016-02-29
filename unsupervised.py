import math
# Not necessary in future but recommand
import numpy as np
import random
import operator
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
			clusters,centroids = self.clusters_(data,indices_c)
					
		return clusters,centroids
########### DBSCAN	
class dbscan:
	#https://fr.wikipedia.org/wiki/DBSCAN
	def __init__(self,eps=10,minpts=10):
		self.eps = eps
		self.minpts = minpts
		self.clusters = {'NOISE':[]}
	"""def eps_near(self,data,i):
		eps = self.eps
		res = []
		for j in xrange(len(data)):
			if j!=i and distance(data[i],data[j])<=eps:
				res.append(j)
		return res
	"""
	def fit(self,data):
		visited = ['UNCLASSIFIED']*len(data)
		def union(U,V):
			res = []
			for i in U:
				if i not in V:
					res.append(i)
			for i in V:
				if i not in res:
					res.append(i)
			return res
		def clustered(clusters,P):
			for key in clusters:
				if P in clusters[key]:
					return True
			return False
		def eps_near(data,P,eps):
			res = []
			for i in xrange(len(data)):
				if P!=i and distance(data[i],data[P])<=eps:
                                	res.append(i)		
			return res
		def extend_cluster(data,P,neigbours,c_cluster,eps,minpts):
			if c_cluster not in self.clusters:
				self.clusters[c_cluster] = [P]
			else:
				self.clusters[c_cluster].append(P)
			for P_prime in neigbours:
				if visited[P_prime]!='VISIT':
					visited[P_prime] = 'VISIT'
					P_prrime_n = eps_near(data,P_prime,eps)
					if len(P_prrime_n) > minpts:
						neigbours = union(P_prrime_n,neigbours)
				if not clustered(self.clusters,P_prime):
					self.clusters[c_cluster].append(P_prime)
		c_clusters = 0
		eps = self.eps
		minpts = self.minpts
		cluster = {}
		for P in xrange(len(data)):
			#print visited
			if visited[P]!='VISIT':
				visited[P] = 'VISIT'
				eps_near_ = eps_near(data,P,eps)
				if len(eps_near_)< minpts:
					self.clusters['NOISE'].append(P)
				else:
					c_clusters += 1

					extend_cluster(data,P,eps_near_,c_clusters,eps,minpts)
		return self.clusters
###################### OPTICS
class optics:
	def __init__(self,eps,minpts,cluster_threshold = 50):
                self.eps = eps
                self.minpts = minpts
		self.cluster_threshold = cluster_threshold
	def fit(self,data):
		eps = self.eps
		minpts = self.minpts
		ordered = []
		visited = ['UNCLASSIFIED']*len(data)
		def n_eps(eps,P,data):
			res = []
			for i in xrange(len(data)):
				if distance(data[P],data[i])<=eps:
					res.append(i)
			return res
		def core_distance(eps,minpts,P,data):
			n_eps_ = n_eps(eps,P,data)
			d_min_pts_dist = eps
			if len(n_eps_)< minpts:
				return None
			else:
				for i in n_eps_:
					d = distance(data[i],data[P])
					if d < d_min_pts_dist:
						d_min_pts_dist = d
				return d_min_pts_dist
		def reachability_distance(data,eps,minpts,O,P):
			n_eps_ = n_eps(eps,P,data)
                        d_min_pts_dist = eps
                        if len(n_eps_)< minpts:
                                return None
			else:
				return max(core_distance(eps,minpts,P,data),distance(data[P],data[O]))
		def update(N,p,seeds,eps,minpts,data,reach):
			coredist = core_distance(eps,minpts,p,data)
			import operator
			for o in N:
				#print seeds
				#print reach
				if visited[o]=='UNCLASSIFIED':
					new_reach_dist = max(coredist,distance(data[o],data[p]))
					if o not in seeds:
						seeds[o] = None
					if reach[o] == None:
						reach[o] = new_reach_dist
						seeds[o] = new_reach_dist
					else:
						if new_reach_dist < reach[o]:
							reach[o] = new_reach_dist
							#seeds.pop(o)
							seeds[o] = new_reach_dist
			x = seeds
			return sorted(x.items(), key=operator.itemgetter(1))
		reach = {}
		for p in xrange(len(data)):
			reach[p] = None
		#print reach
		for p in xrange(len(data)):
			if visited[p] != 'VISIT':
				N = n_eps(eps,p,data)
				visited[p] = 'VISIT'
				ordered.append(p)
				if core_distance(eps,minpts,p,data) != None :
					seeds = {}#[None]*len(data)
					update(N,p,seeds,eps,minpts,data,reach)
					import operator
					x = seeds
					sorted_x = sorted(x.items(), key=operator.itemgetter(1))
					# remember sort seeds
					for d in xrange(len(sorted_x)):
						q = sorted_x[d][0]
						if visited[q] != 'VISIT':
							ordered.append(q)
							N_prime = n_eps(eps,q,data)
							visited[q] = 'VISIT'
							if core_distance(eps,minpts,q,data) != None:
								update(N,q,seeds,eps,minpts,data,reach)
		#def cluster(self,cluster_threshold,reach):
		separators = []
		clusters = {}
		cluster_threshold = self.cluster_threshold
		c = 0
		for i in xrange(len(ordered)):
			pt = i
			reach_d = reach[ordered[i]] if reach[ordered[i]] else float('infinity')
			if reach_d > cluster_threshold:
				separators.append(pt)
		separators.append(len(ordered))
		for i in xrange(len(separators)-1):
			start = separators[i]
			end = separators[i+1]
			if end - start >=  self.minpts:
				c+= 1
				clusters[c] = []
				for d in ordered[start:end]:
					clusters[c].append(d)
		print ordered			
		return clusters
db= optics(eps=100,minpts=2,cluster_threshold = 1)
data = [[0,0],[1,1],[1,23],[2,1.2],[1,25],[1,1],[1,1.01]]
print db.fit(data = data)
#print len(data)
#print k.fit(data)
