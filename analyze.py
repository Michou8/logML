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
	"""condider every log like a vector
		inputs:
		------
			events : set of data log
			meta_not_used : meta not used for vectorization e.g : it will be unique each event (not relevant)

	"""
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
def grouped_per_event(events,tronc='h',meta_not_used = ['date','time','response_size','response_time','ip_adress','user_agent']):
	"""grouped and vectorized event per tronc
		example: grouped each hour
		input:
		-----
			events: set of data log
			tronc : h = hour , m = minutes , s = secondes
			meta_not_used : meta not used for vectorization e.g : it will be unique each event (not relevant)
	"""
	encoder_ = []
	per_date = {}
	for e in events:
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
def tfidf_per_time(events,tronc='h',meta_not_used = ['date','time','response_size','response_time','ip_adress','user_agent']):
	""" gives tfidf vectorization per tronc
		input:
                -----
                        events: set of data log
                        tronc : h = hour , m = minutes , s = secondes
                        meta_not_used : meta not used for vectorization e.g : it will be unique each event (not relevant)
	"""
	df_tot = 0.0
	encoder_ = []
	tf_tot = 0.0
	df = {}
	def tfidf(table_event,tf_tot=tf_tot,df=df):
		"""simple tf descriptor
		"""
		tf = {}
		for e in table_event:
			for key in e:
				if key not in meta_not_used:
					m_data = e[key]
					tf_tot += 1
					if m_data not in tf:
						tf[m_data] = 1
					else:
						tf[m_data] += 1
		for key in tf:
			if key not in df:
				df[key] = 1
				encoder_.append(key)
			else:
				df[key] += 1
		return tf,tf_tot,df
	# filtered data by date_time. e.g : Jan 1 10:10:00
	per_date = {}
	for e in events:
		date_time = e['date']+'_'+ time_tronc(e['time'],tronc=tronc)
		if date_time not in per_date:
			per_date[date_time] = [e]
		else:
			per_date[date_time].append(e)
	#Calculated the tf for each date_time
	per_date_tfidf = {}
	#tf_date = all tf per date
	tf_date = {}
	for key in per_date:
		tfidf_,tf_tot,df = tfidf(per_date[key],tf_tot=tf_tot,df=df)
		tf_date[key] = tfidf_
		per_date_tfidf[key] = tfidf_
	df_tot = len(per_date_tfidf)
	
	#Calculated tfidf for each date
	for date in per_date_tfidf:
		tmp = {}
		for key in per_date_tfidf[date]:
			tf_key = per_date_tfidf[date][key]
			tmp[key] = (tf_key/tf_tot)*math.log((df_tot/df[key])+1)
		per_date_tfidf[date] = tmp

	data = []
	localization = {}
	c = 0
	#vectorized each date 
	for date in per_date_tfidf:
		tmp = [-1]*len(encoder_)
		for k in xrange(len(encoder_)):
			if encoder_[k] in per_date_tfidf[date]:
				tmp[k] = per_date_tfidf[date][encoder_[k]]
		data.append(tmp)
		localization[c] = date
		c += 1
		
	return per_date_tfidf,df,data,encoder_,localization,tf_date

def tfidf_(result,meta_not_used = ['date','time','response_size','response_time','ip_adress','user_agent']):
	###### Testing the tf idf
	df = {}
	df_tot = len(result)
	tf = {}
	for event in result:
		for key in event:
			if key not in meta_not_used:
				m_data = event[key]
				if m_data not in tf:
					tf[m_data] = 1
				else:
					tf[m_data] += 1
		for key in tf:
			if key in event.values():
				if key not in df:
					df[key] = 1
				else:
					df[key] += 1
	return tf,df
def bigram(event,used = ['date','time','response_size','response_time','ip_adress','user_agent']):
	""" give bigram of dict by used ordered
	"""
	result = []
	for i in xrange(len(used)-1):
		if used[i] in event and used[i+1] in event:
			tmp = event[used[i]]+'_'+event[used[i+1]]
		else:
			tmp = '_'
		result.append(tmp)
	return result


def create_json(data,localization,tf_date,clusters):
	all_json = {'nodes':[],'links':[]}
	def mean_(set_of_data):
		tmp = [0]*len(set_of_data[0])
		for event in set_of_data:
			for i in xrange(len(event)):
				tmp[i] += event[i]
		for i in xrange(len(tmp)):
			tmp[i] = tmp[i]/len(set_of_data)
		return tmp
	def getData(data,indices):
		result = []
		for i in indices:
			result.append(data[i])
		return result
	def dictance(p,q):
		res = 0.0
		for i in xrange(len(p)):
			tmp = p[i]-q[i]
			res += tmp**2
		return math.sqrt(res)
	id = 0
	cl = 0
	for cluster in clusters:
		centroids = mean_(getData(data,clusters[cluster]))
		centroids_id = id
		all_json['nodes'].append({"name":'Cluster_'+str(centroids_id),"group":cluster})
		for i in clusters[cluster]:
			value = dictance(data[i],centroids)
			print value
			# TO-DO add distance between centroids and data in cluster --> done
			all_json['nodes'].append({"name":str(tf_date[localization[i]]),"group":cluster})
			#{"source":19,"target":17,"value":4}
			id += 1
			all_json['links'].append({"source":id,"target":centroids_id,"value":1})
		id += 1
	with open("example/miserables.json",'wb') as f:
		json.dump(all_json,f,indent=4)
			
####################################################
event = {"date":'r','time':'utioerutio'}
#print bigram(event,used = ['date','time','response_size','response_time','ip_adress','user_agent'])
#raw_input()
events = randomevent.events(number=60*100).evts(M='Dec',d=31,h=23,m=59,s=58)
print events[0]
raw_input()
per_date_tfidf,df,data,encoder_,localization,tf_date = tfidf_per_time(events,tronc='m')
#raw_input()
#data,_ = grouped_per_event(events,tronc='m')

#print events[:10]
#raw_input()
#data,encoder_ = encoder_one(events) 
km = unsupervised.optics(eps=0.1,minpts=5)
clusters = km.fit(data)

create_json(data,localization,tf_date,clusters)
for k in  clusters['NOISE']:
	print localization[k]
	print tf_date[localization[k]]
	print data[k]
	print encoder_
