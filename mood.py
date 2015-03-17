#DeVonte' Applewhite
#02/25/15 CSE40YYY

import json,sys
sys.path.insert(0,"/afs/nd.edu/coursesp.15/cse/cse40437.01/dropbox/dapplewh/prac/PyHighcharts-master/highcharts")


from chart import Highchart

EXAMPLE_CONFIG = {
    "xAxis": {
        "gridLineWidth": 0,
        "lineWidth": 0,
        "tickLength": 0,
    },
    "yAxis": {
            "gridLineWidth": 0,
    }
}

def load(posfile,negfile,md): #md is the mood dictionary
	f = open(posfile)
	for line in f:
		if line[0] not in ['',' ',';']: #valid data
			md[line.rstrip().encode('utf-8')] = 1 #all positive words have a value of 1
			#print md[line.rstrip().encode('utf-8')]
	f.close()
	f = open(negfile)
	for line in f:
		if line[0] not in ['',' ',';']: #valid data
			md[line.rstrip().encode('utf-8')] = -1 #all positive words have a value of 1
			#print md[line.rstrip().encode('utf-8')]
	f.close()
#end def load

def readNtweets(filename,N,tarray):
	count = 0;
	f = open(filename)
	for line in f:
		if count == N:
			break;
		a = json.loads(line.rstrip())
		#print type(a)
		tarray.append(a)
		count += 1
#end def readNtweets

def netmood(text,md):
	net = 0 #net mood starts at zero
	words = text.split() #split into an array of words
	for item in words: #go through each word
		if item in md: #mood word detected
			net += md[item]
	return net
#end def netmood

def processTweets(filename,companyname,md):
	count = 0 #total tweets processed
	good_count = 0 #positive mood tweets
	bad_count = 0 #negative mood tweets
	neutral_count = 0 #no mood tweets
	f = open(filename)
	for line in f:
		a = json.loads(line.rstrip())
		try:
			s = a['text']
		except KeyError:
			continue
		score = netmood(a['text'].lower().encode('utf-8'),md)
		#print a['text']
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
	pie_example(companyname,"imp",count,good_count,bad_count,neutral_count)
#end def readNtweets

def pie_example(companyname,filename,count,good,bad,neutral):
    #""" Basic Piechart Example """
    chart = Highchart()
    chart.title(companyname)
    chart.add_data_set([["Good Tweets", int(100*good/float(count))],
        ["Bad Tweets", int(100*bad/float(count))],
	["Neutral Tweets", int(100*neutral/float(count))]],
        series_type="pie",
        name="",
        startAngle=45)
    chart.colors(["#00FF00", "#FF0000", "FFFF00"])
    chart.set_options(EXAMPLE_CONFIG)
    chart.show(filename)

if __name__ == "__main__":
	moodwords = {}
	load('positive-words.txt','negative-words.txt',moodwords)
	#s = "I mourn muddy men. But I like my cat.".lower().encode('utf-8')
	#print netmood(s,moodwords)
	#tlist = []
	#readNtweets('w.txt',23,tlist)
	#for tweet in tlist:
	#	print tweet['text']
	#	print netmood(tweet['text'].lower(),moodwords)
	processTweets('apple.txt','Apple',moodwords)
#end main
