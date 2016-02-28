import json
import math
import randomevent
########## First approach every meta has a value (No grouped)
def encoder(events,meta_not_used = ['date','time','response_size','response_time','ip_adress']):
	encoder_ = {}
	for e in events:
		for key in e:
			if key not in meta_not_used:
				if key not in encoder_:
					encoder_[key] = {e[key]:1}
				else:
					if e[key] not in encoder_[key]:
						encoder_[key][e[key]] = len(encoder_[key])+1
	return encoder_

events = randomevent.events(number=10000).evts()
print encoder(events)
