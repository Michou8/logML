import json
import math
import randomevent
import unsupervised
########## First approach every meta has a value (No grouped)
def encoder(events,meta_not_used = ['date','time','response_size','response_time','ip_adress']):
	# It was not really efficient because we don't have any distance between two categories. What is the distance between 'get' and 'post'?
	# ????? Not really relevant for me
	encoder_ = {}
	transform = []
	order = events[0].keys()
	for e in events:
		tmp = []
		for key in e:
			if key not in meta_not_used:
				if key not in encoder_:
					encoder_[key] = {e[key]:1}
				else:
					if e[key] not in encoder_[key]:
						encoder_[key][e[key]] = len(encoder_[key])+1
		for key in order:
			if key not in meta_not_used:
				tmp.append(encoder_[key][e[key]])
		transform.append(tmp)	
	return transform,encoder_
def encoder_one(events,meta_not_used = ['date','time','response_size','response_time','ip_adress']):
	encoder_ = {}
	for e in events:
                for key in e:
                        if key not in meta_not_used:
				t = key+'_'+e[key]
				if t not in encoder_:
                                        encoder_[t] = 1
                                else:
					encoder_[t] += 1
	keys = encoder_.keys()
	tranform = []
	for e in events:
		tmp = []
		for k in xrange(len(keys)):
			spl = keys[k].split('_')
			if spl[0] in e and spl[1] in e.values():
				tmp.append(1)
			else:
				tmp.append(0)
		tranform.append(tmp)
	return tranform,keys
def time_tronc(time,tronc='h'):
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
def grouped_per_event(events,tronc='h',meta_not_used = ['date','time','response_size','response_time','ip_adress','user_agent']):
	encoder_ = []
	per_date = {}
	for e in events:
		#print e
		#event = '_'.join([str(w)+':'+str(e[w]) for w in e if w not in meta_not_used])
		#print event
		tmp = {}
		for key in e:
			if key not in meta_not_used:
				tmp[key] = e[key]
		if tmp not in encoder_:
			#encoder_[event] = 1
			encoder_.append(tmp)
	for e in events:
		time = time_tronc(e['time'],tronc=tronc)
		if time not in per_date:
			per_date[time] = [0]*len(encoder_)
		c = 0
		tmp = {}
                for key in e:
                        if key not in meta_not_used:
                                tmp[key] = e[key]
		for i in xrange(len(encoder_)):
			if encoder_[i] == tmp:
				per_date[time][i] += 1
		#print per_date[time]
		#raw_input()
	result = []
	date = {}
	i = 0
	for key in per_date:
		result.append(per_date[key])
		if key not in date:
			date[key] = [i]
			i += 1
		else:
			date[key].append(i)
			i += 1
	return result,date
def create_force(result,clusters):
	nodes = {"nodes":[]}
	links = {"links":[]}
	for key in result:
		
####################################################

events = randomevent.events(number=1000).evts()
data = grouped_per_event(events)
#data,encoder_ = encoder_one(events) 
km = unsupervised.kmeans(k=2,n=20)
clusters,centroids = km.fit(data)
#print encoder_
