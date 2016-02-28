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
####################################################

events = randomevent.events(number=10000).evts()
data,encoder_ = encoder(events) 
km = unsupervised.kmeans(k=3,n=10)
print km.fit(data)
#print encoder_
