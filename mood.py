#DeVonte' Applewhite
#02/25/15 CSE40YYY

import json,sys,datetime
sys.path.insert(0,"/afs/nd.edu/coursesp.15/cse/cse40437.01/dropbox/dapplewh/prac/PyHighcharts-master/highcharts")


from chart import Highchart

class mood():
	def __init__(self,interval=300):
		self.EXAMPLE_CONFIG = {"xAxis": {"gridLineWidth": 0,"lineWidth": 0,"tickLength": 0,},\
		"yAxis": {"gridLineWidth": 0,}}
		self.interval = interval #interval to govern certain functions
		self.moodwords = {}
		self.moodarray = [] #net mood at each data dump
		self.countarray = [] #number of tweets per data dump
		self.moodbin = {} #holds lists of good, bad, and neutral tweet counts
		self.moodbin['good'] = []
		self.moodbin['bad'] = []
		self.moodbin['neutral'] = []
		self.count = 0 #total tweets processed

		self.oldtime = None #holds the last timestamp
		self.scoredump = 0 #aggregate score between intervals
		self.goodcount = 0
		self.badcount = 0
		self.neutralcount = 0
		self.localcount = 0 #total tweets processed in an interval

	def makedate(self,datestring):
		try:
			tinfo = datestring.rstrip().split(' ')
			#tinfo contains [dayOfWeek,month,day,hour:min:sec,?,year]
			timeparts = tinfo[3].split(':')
			timestr = tinfo[5]+" "+tinfo[1]+" "+tinfo[2]+" "+tinfo[3]
			fmt = "%Y %b %d %H:%M:%S"
			t2 = datetime.datetime.strptime(timestr,fmt)
			return t2
		except KeyError:
			return None

	def load(self,posfile,negfile): #md is the mood dictionary
		f = open(posfile)
		for line in f:
			if line[0] not in ['',' ',';']: #valid data
				self.moodwords[line.rstrip().encode('utf-8')] = 1 #all positive words have a value of 1
		f.close()
		f = open(negfile)
		for line in f:
			if line[0] not in ['',' ',';']: #valid data
				self.moodwords[line.rstrip().encode('utf-8')] = -1 #all positive words have a value of 1
		f.close()
	#end def load

	def readNtweets(self,filename,N,tarray):
		count = 0;
		f = open(filename)
		for line in f:
			if count == N:
				break;
			a = json.loads(line.rstrip())
			tarray.append(a)
			count += 1
	#end def readNtweets

	def netmood(self,text):
		net = 0 #net mood starts at zero
		words = text.split() #split into an array of words
		for item in words: #go through each word
			if item in self.moodwords: #mood word detected
				net += self.moodwords[item]
		return net
	#end def netmood

	def processTweets(self,filename,companyname,func):
		self.clear() #reset stats for next dump interval

		f = open(filename)
		for line in f:
			self.add(line) 
			
		if self.oldtime != None: #dump leftover data that didn't reach the interval
			self.moodarray.append(self.scoredump) #add net score
			self.countarray.append(self.localcount)
			self.moodbin['good'].append(self.goodcount)
			self.moodbin['bad'].append(self.badcount)
			self.moodbin['neutral'].append(self.neutralcount)

		f.close() #close file

		print "Total Tweets: %d"%(self.count)

		if func == 'line':
			outfilename = companyname.lower()+"_line.html"
			self.linegraph(companyname,outfilename,1) #adds count data
		elif func == 'pie':
			outfilename = companyname.lower()+"_pie.html"
			self.piegraph(companyname,outfilename) #single pie

	def add(self,tweet): #process a tweet
		try:
			a = json.loads(tweet.rstrip())
		except ValueError:
			return 0
		try:
			s = a['text'] #just to check if the necessary keys are found
			c = a['created_at']
		except KeyError:
			return 0

		score = self.netmood(s.lower().encode('utf-8'))
		self.scoredump += score #aggregate net score

		if score > 0: #good tweet
			self.goodcount += 1
		elif score < 0: #bad tweet
			self.badcount += 1
		else: #neutral tweet
			self.neutralcount += 1

		self.localcount += 1
		self.count += 1 #bookkeeping for entire process

		if self.oldtime != None: #old time is initialized
			t = self.makedate(c) #make usable date
			diff = 0
			if t > self.oldtime: #get time difference
				diff = t - self.oldtime
			else:
				diff = self.oldtime - t
			if diff.seconds >= self.interval: #need to dump data
				self.moodarray.append(self.scoredump) #add net score
				self.countarray.append(self.localcount)
				self.moodbin['good'].append(self.goodcount)
				self.moodbin['bad'].append(self.badcount)
				self.moodbin['neutral'].append(self.neutralcount)

				self.clear() #reset stats

				return 1 #let listener know data has been dumped
		else:
			self.oldtime = self.makedate(c) #make the date
		return 0 #no data has been dumped yet

	def clear(self): #reset stats for next dump
		self.oldtime = None #reset all stats for next dump
		self.scoredump = 0
		self.goodcount = 0
		self.badcount = 0
		self.neutralcount = 0
		self.localcount = 0

	def set_interval(self,value):
		self.interval = value

	def piegraph(self,companyname,filename,multi=False):
		chart = Highchart()
		chart.title(companyname)

		good = 0
		bad = 0
		neutral = 0

		if multi == False:
			good = sum(self.moodbin['good'])
			bad = sum(self.moodbin['bad'])
			neutral = sum(self.moodbin['neutral'])
	
		chart.add_data_set([["Good Tweets", int(100*good/float(self.count))],
		    ["Bad Tweets", int(100*bad/float(self.count))],
	["Neutral Tweets", int(100*neutral/float(self.count))]],
		    series_type="pie",
		    name=companyname+" Impression Pie Chart",
		    startAngle=45)
		chart.colors(["#00FF00", "#FF0000", "#FFFF00"])
		chart.set_options(self.EXAMPLE_CONFIG)
		chart.show(filename)

	def linegraph(self,companyname,filename,countdata = None):
		chart = Highchart()
		chart.title(companyname)

		chart.add_data_set(self.moodarray, series_type="line", name=companyname+" raw net mood", index=1)

		if countdata != None: #add average mood
			moodtotal = [self.moodbin['good'][i]+self.moodbin['bad'][i] for i in range(len(self.moodbin['good']))] #count of nonzero mood scores
			averagemood = [float(self.moodarray[i])/moodtotal[i] for i in range(len(self.moodarray))]
			chart.add_data_set(averagemood, series_type="line", name=companyname+" average net mood", index=2)

		chart.colors(["#00FF00", "#FF0000", "#FFFF00"])
		chart.set_options(self.EXAMPLE_CONFIG)
		chart.show(filename)

if __name__ == "__main__":
	m = mood(120)
	m.load('positive-words.txt','negative-words.txt')
	m.processTweets('walmart.txt','Lolmart','pie')
#end main
