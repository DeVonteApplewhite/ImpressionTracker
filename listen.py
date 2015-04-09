#/afs/nd.edu/user14/csesoft/new/bin/python
from tweepy import StreamListener
import json, time, sys, os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
from mood import mood
#TODO aggregate tweet scores and only call process when you want to dump a score
class CustomStreamListener(tweepy.StreamListener): #listens for incomming tweets
	def __init__(self):
		super(CustomStreamListener, self).__init__()
		self.count = 0 #count tweets
		self.impression = mood()
		self.impression.load('positive-words.txt','negative-words.txt')
		self.interval = 20
		self.start = None #start timestamp
		self.scoredump = 0
	def on_data(self, data):
		#print data
		outString = data.encode('utf-8')
		tweet = json.loads(outString.rstrip())
		try:
			self.scoredump += self.impression.netmood(tweet['text'].lower())
			self.count += 1
			if self.start == None:
				self.start = self.impression.makedate(tweet['created_at'])
			else:
				now = self.impression.makedate(tweet['created_at'])
				diff = 0
				if now > self.start:
					diff = now - self.start
				else:
					diff = self.start - now
				if diff.seconds >= self.interval: #need to dump data
					self.impression.add(self.scoredump,self.count)
					self.scoredump = 0 #reset score
					self.count = 0 #reset count
					self.start = None #reset oldtime
					self.impression.linegraph('Apple',"appleline",self.impression.moodarray,self.impression.countarray)
					os.system("./putinwww.sh appleline.html")
					#self.impression.clear()
					if len(sys.argv) == 2:
						print "OUT"
			if(len(sys.argv) != 2):
				print outString.rstrip()
		except KeyError:
			pass
		return True
	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream
	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream

if __name__ == "__main__":


	auth = tweepy.OAuthHandler("StBTJPvpNnlb7jxO7joCwt0GZ",
	"8M3ReVr2Knkmdci1zBGtfM4NUsLJH2NvQJbWorGRNg0o64rJfT")
	auth.set_access_token("3008646015-2ae2vykbLAT65ceJueytFDVkFaoOHjbmv8gELw6",
	"88sNWTJSx0VnSmEKeeJk1s2zJd1kB8VVB4NBSFkvpaHDO")
	api = tweepy.API(auth)
	sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
	#sapi.filter(track=['Walmart', 'Sam''s Club', 'Sams Club', 'rollback', 'roll-back'])
	sapi.filter(track=['Apple','iOS','OSX','iPad','iPhone'])
