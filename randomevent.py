import random
from random import randint
import json
class events: 
	
	def __init__(self,number=30): 
		self.number = number
		self.filename = 'data.json'
	def date(self):
		Months = {'Jan':31,'Feb':28,'Mar':31,'Apr':30,'May':31,'Jun':30,'Jul':31,'Aug':31,'Nov':30,'Oct':31,'Nov':30,'Dec':31}
		m = Months.keys()
		month = m[randint(0,len(m)-1)]
		return month+' '+str(randint(0,Months[month])+1) 
	def ip(self):
		r = randint
		return str(r(1,255)) +'.'+str(r(0,255))+'.'+str(r(0,255))+'.'+str(r(0,255)) 
	def action(self):
		actions= ['get','delete','post','getUrl','Na']
		return actions[randint(0,len(actions)-1)]
	def code(self):
		return str(randint(1,5)*100)
	def device(self):
		device = ['ios','android','Pc']
		return device[randint(0,len(device)-1)]
	def user_agent(self):
		user_agent = ['Opera','Firefox','IE','Chrome']
		return user_agent[randint(0,len(user_agent)-1)]
	def response_time(self):
		return random.uniform(0.0, 5.0)
	def response_size(self):
		return randint(0,256)
	def evts(self):
		log_event = []
		for i in xrange(self.number):
			e = events()
			tmp = {'Date':e.date(),'ip_adress':e.ip(),'action':e.action(),'code':e.code(),'device':e.device(),'user_agent':e.user_agent(),'response_time':e.response_time(),'response_size':e.response_size()}
			log_event.append(tmp)
		return log_event
	def write_log(self):
		with open(self.filename,'wb') as f:
			json.dump(events(self.number).evts(),f,indent=4)
event = events(number=50).write_log()
print event
