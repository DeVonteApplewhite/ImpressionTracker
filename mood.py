#DeVonte' Applewhite
#02/25/15 CSE40YYY

import json,sys,datetime
sys.path.insert(0,"/afs/nd.edu/coursesp.15/cse/cse40437.01/dropbox/dapplewh/prac/PyHighcharts-master/highcharts")


from chart import Highchart

class mood():
	def __init__(self):
		self.EXAMPLE_CONFIG = {"xAxis": {"gridLineWidth": 0,"lineWidth": 0,"tickLength": 0,},\
		"yAxis": {"gridLineWidth": 0,}}
		self.moodwords = {}
		self.moodarray = [] #net mood at each data dump
		self.countarray = [] #number of tweets per data dump
		self.count = 0
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

	def processTweets(self,filename,companyname):
		count = 0 #total tweets processed
		good_count = 0 #positive mood tweets
		bad_count = 0 #negative mood tweets
		neutral_count = 0 #no mood tweets
		f = open(filename)
		for line in f:
			try:
				a = json.loads(line.rstrip())
			except ValueError:
				continue
			try:
				s = a['text']
			except KeyError:
				continue
			score = netmood(a['text'].lower().encode('utf-8'))
			if score > 0: #good tweet
				good_count += 1
			elif score < 0: #bad tweet
				bad_count += 1
			else: #neutral tweet
				neutral_count += 1
			count += 1
		f.close() #close file
		print companyname
		print "Total Tweets: %d"%(count)
		print "Good Tweets: %d (%f)"%(good_count,good_count/float(count))
		print "Bad Tweets: %d (%f)"%(bad_count,bad_count/float(count))
		print "Neutral Tweets: %d (%f)"%(neutral_count,neutral_count/float(count))
		self.pie(companyname,"imp",count,good_count,bad_count,neutral_count)
	#end def processtweets

	def processTweets2(self,filename,companyname):
		count = 0 #total tweets processed
		moodarray = []
		interval = 120 #seconds which is 5 minutes
		oldtime = None #holds the last timestamp
		scoredump = 0 #aggregate score between intervals
		f = open(filename)
		for line in f:
			try:
				a = json.loads(line.rstrip())
			except ValueError:
				continue
			try:
				s = a['text']
			except KeyError:
				continue
			scoredump += self.netmood(a['text'].lower().encode('utf-8')) #accumilate a score
			if oldtime != None:
				t = self.makedate(a['created_at'])
				diff = 0
				if t > oldtime:
					diff = t - oldtime
				else:
					diff = oldtime - t
				if diff.seconds >= interval: #need to dump data
					moodarray.append(scoredump)
					scoredump = 0 #reset score
					oldtime = None #reset oldtime
			else:
				oldtime = self.makedate(a['created_at']) #make the date
			count += 1
		if oldtime != None:
			moodarray.append(scoredump)
		f.close() #close file
		#print moodarray
		print "Total Tweets: %d"%(count)

		self.linegraph(companyname,"prog",moodarray)
	#end def line

	def add(self,tweetscore,thecount = None):
		self.moodarray.append(tweetscore)
		if thecount != None:
			self.countarray.append(thecount) #add count if available
		self.count += 1

	def clear(self):
		self.countarray = []
		self.moodarray = []

	def pie(self,companyname,filename,count,good,bad,neutral):
		  #""" Basic Piechart Example """
		  chart = Highchart()
		  chart.title(companyname)
		  chart.add_data_set([["Good Tweets", int(100*good/float(count))],
		      ["Bad Tweets", int(100*bad/float(count))],
		["Neutral Tweets", int(100*neutral/float(count))]],
		      series_type="pie",
		      name="",
		      startAngle=45)
		  chart.colors(["#00FF00", "#FF0000", "#FFFF00"])
		  chart.set_options(self.EXAMPLE_CONFIG)
		  chart.show(filename)

	def linegraph(self,companyname,filename,mooddata,countdata = None):
		chart = Highchart()
		chart.title(companyname)
		#x = range(24)
		chart.add_data_set(mooddata, series_type="line", name=companyname+" raw net mood", index=1)

		if countdata != None:
			averagemood = [float(mooddata[i])/countdata[i] for i in range(len(mooddata))]
			chart.add_data_set(averagemood, series_type="line", name=companyname+" average net mood", index=2)

		chart.colors(["#00FF00", "#FF0000", "#FFFF00"])
		chart.set_options(self.EXAMPLE_CONFIG)
		chart.show(filename)

if __name__ == "__main__":
	m = mood()
	m.load('positive-words.txt','negative-words.txt')
	m.processTweets2('walmart.txt','Walmart')
#end main
