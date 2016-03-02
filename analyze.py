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
def tfidf_per_time(events,tronc='h',meta_not_used = ['date','time','response_size','response_time','ip_adress','user_agent']):
	df_tot = 0.0
	encoder_ = []
	tf_tot = 0.0
	df = {}
	def tfidf(table_event,tf_tot=tf_tot,df=df):
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
	per_date = {}
	for e in events:
		date_time = e['date']+'_'+ time_tronc(e['time'],tronc=tronc)
		if date_time not in per_date:
			per_date[date_time] = [e]
		else:
			per_date[date_time].append(e)
	per_date_tfidf = {}
	tf_date = {}
	for key in per_date:
		tfidf_,tf_tot,df = tfidf(per_date[key],tf_tot=tf_tot,df=df)
		tf_date[key] = tfidf_
		per_date_tfidf[key] = tfidf_
	#print tf_tot
	#print df_tot
	df_tot = len(per_date_tfidf)
	for date in per_date_tfidf:
		tmp = {}
		for key in per_date_tfidf[date]:
			tf_key = per_date_tfidf[date][key]
			tmp[key] = (tf_key/tf_tot)*math.log((df_tot/df[key])+1)
		per_date_tfidf[date] = tmp
	#print per_date_tfidf
	data = []
	localization = {}
	c = 0
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
	result = []
	for i in xrange(len(used)-1):
		if used[i] in event and used[i+1] in event:
			tmp = event[used[i]]+'_'+event[used[i+1]]
		else:
			tmp = '_'
		result.append(tmp)
	return result
		
####################################################
event = {"date":'r','time':'utioerutio'}
print bigram(event,used = ['date','time','response_size','response_time','ip_adress','user_agent'])
raw_input()
events = randomevent.events(number=10000).evts(M='Dec',d=31,h=23,m=59,s=58)
per_date_tfidf,df,data,encoder_,localization,tf_date = tfidf_per_time(events,tronc='h')
#raw_input()
#data,_ = grouped_per_event(events,tronc='m')

#print events[:10]
#raw_input()
#data,encoder_ = encoder_one(events) 
km = unsupervised.dbscan(eps=2,minpts=3)
clusters = km.fit(data)
for k in  clusters['NOISE']:
	print localization[k]
	print tf_date[localization[k]]
	print data[k]
	print encoder_
